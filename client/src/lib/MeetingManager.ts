import { backendBaseUrl } from "./api";

/** milliseconds between sending chunks of audio */
const AUDIO_CHUNK_PERIOD = 3000;

export type Manager = {
  kill(): void;
  screenShare(enable: boolean): Promise<void>;
};

export async function makeManager(
  webcamPreview: HTMLVideoElement,
  screenPreview: HTMLVideoElement
): Promise<Manager> {
  const audioContext = new AudioContext();

  const ws = new WebSocket(`${backendBaseUrl?.replace("http", "ws")}/ws`);
  ws.binaryType = "arraybuffer";
  ws.addEventListener("message", async (e: MessageEvent<ArrayBuffer>) => {
    const audioBuffer = await audioContext.decodeAudioData(e.data);
    const source = audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(audioContext.destination);
    source.start();
  });

  const audioStream = await navigator.mediaDevices.getUserMedia({
    audio: true,
  });
  const videoStream = await navigator.mediaDevices.getUserMedia({
    video: true,
  });
  let screenStream: MediaStream | null = null;

  webcamPreview.srcObject = videoStream;
  webcamPreview.play();
  screenPreview.srcObject = screenStream;
  screenPreview.play();

  const audioRecorder = new MediaRecorder(audioStream);
  audioRecorder.ondataavailable = (event) => {
    if (event.data.size > 0) {
      ws.send(event.data);
    }
  };
  audioRecorder.start(AUDIO_CHUNK_PERIOD); // Send audio every PERIOD ms

  return {
    kill: () => {
      ws.close();
      audioRecorder.stop();
      killStream(audioStream);
      killStream(videoStream);
      if (screenStream) {
        killStream(screenStream);
      }
    },

    screenShare: async (enable) => {
      if (screenStream) {
        killStream(screenStream);
      }
      if (enable) {
        screenStream = await navigator.mediaDevices.getDisplayMedia({
          video: true,
        });
        screenPreview.srcObject = screenStream;
        screenPreview.play();
      } else {
        screenStream = null;
        screenPreview.pause();
      }
    },
  };
}

function killStream(stream: MediaStream): void {
  for (const track of stream.getTracks()) {
    track.stop();
  }
}

import { Personality, WebSocketJsonMessage } from "./api";
import { encodeWav } from "./wav-encoder";

/** milliseconds between sending chunks of audio */
const AUDIO_CHUNK_PERIOD = 5000;

export type Manager = {
  kill(): void;
  screenShare(enable: boolean): Promise<void>;
};

export async function makeManager(
  webcamPreview: HTMLVideoElement,
  screenPreview: HTMLVideoElement,
  onClose: () => void,
  onStudents: (students: [string, string, Personality][]) => void,
  onSpeak: (studentName: string, speaking: boolean) => void
): Promise<Manager> {
  const audioContext = new AudioContext();

  const websocket_url = `${process.env.NEXT_PUBLIC_BACKEND_URL?.replace(
    "http",
    "ws"
  )}/ws`;
  const ws = new WebSocket(websocket_url);
  ws.binaryType = "arraybuffer";

  // Add error and close handlers
  ws.addEventListener("error", (error) => {
    console.error("WebSocket error:", error);
  });

  ws.addEventListener("close", (event) => {
    console.log("WebSocket closed:", event.code, event.reason);
    onClose();
  });

  const gainNode = audioContext.createGain();
  gainNode.gain.value = 10;
  gainNode.connect(audioContext.destination);

  let lastSpeaker = "";
  ws.addEventListener(
    "message",
    async (e: MessageEvent<ArrayBuffer | string>) => {
      if (typeof e.data === "string") {
        const message: WebSocketJsonMessage = JSON.parse(e.data);
        switch (message.type) {
          case "students":
            onStudents(message.students);
            break;
          case "about-to-speak":
            lastSpeaker = message.studentName;
            break;
          default:
            console.warn("unknown msg", message);
        }
      } else {
        const audioBuffer = await audioContext.decodeAudioData(e.data);
        const source = audioContext.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(gainNode);
        source.addEventListener("ended", () => {
          onSpeak(lastSpeaker, false);
        });
        source.start();
        onSpeak(lastSpeaker, true);
      }
    }
  );

  const audioStream = await navigator.mediaDevices.getUserMedia({
    audio: true,
  });
  const videoStream = await navigator.mediaDevices.getUserMedia({
    video: true,
  });
  let screenStream: MediaStream | null = null;

  webcamPreview.srcObject = videoStream;
  webcamPreview.play().catch(() => {});
  screenPreview.srcObject = screenStream;
  screenPreview.play().catch(() => {});

  let buffers: Float32Array[] = [];
  const mediaStreamSource = audioContext.createMediaStreamSource(audioStream);
  const scriptProcessorNode = audioContext.createScriptProcessor(8192, 2, 2);
  scriptProcessorNode.addEventListener("audioprocess", (processEvent) => {
    buffers.push(new Float32Array(processEvent.inputBuffer.getChannelData(0)));
  });
  mediaStreamSource.connect(scriptProcessorNode);
  scriptProcessorNode.connect(audioContext.destination);

  // const audioRecorder = new MediaRecorder(audioStream);
  // audioRecorder.ondataavailable = (event) => {
  //   if (event.data.size > 0) {
  //     // Check WebSocket state before sending
  //     if (ws.readyState === WebSocket.OPEN) {
  //       ws.send(event.data);
  //     } else if (ws.readyState === WebSocket.CONNECTING) {
  //       console.warn("WebSocket still connecting, data not sent");
  //     } else if (ws.readyState === WebSocket.CLOSING) {
  //       console.warn("WebSocket is closing, data not sent");
  //     } else if (ws.readyState === WebSocket.CLOSED) {
  //       console.error("WebSocket is closed, data not sent");
  //       // Optionally attempt to reconnect here
  //     }
  //   }
  // };
  // audioRecorder.start(AUDIO_CHUNK_PERIOD); // Send audio every PERIOD ms

  let intervalId = setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
      const blob = encodeWav(buffers, audioContext.sampleRate);
      ws.send(blob);
    }
    buffers = [];
  }, AUDIO_CHUNK_PERIOD);

  return {
    kill: () => {
      ws.close();
      // audioRecorder.stop();
      clearInterval(intervalId);
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
        screenPreview.play().catch(() => {});
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

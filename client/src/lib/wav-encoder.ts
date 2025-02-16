// https://github.com/SheepTester/sheeptester.github.io/blob/master/javascripts/audio-editor/wav-encoder/index.js

const encoder = new TextEncoder();
function header(byteCount: number, sampleRate: number, channelCount = 1) {
  // https://isip.piconepress.com/projects/speech/software/tutorials/production/fundamentals/v1.0/section_02/s02_01_p05.html
  // https://github.com/higuma/wav-audio-encoder-js/blob/master/lib/WavAudioEncoder.js
  // wav files are little endian
  const header = new DataView(new ArrayBuffer(44));
  const byteView = new Uint8Array(header.buffer);
  byteView.set(encoder.encode("RIFF"), 0);
  header.setUint32(4, byteCount + 36, true);
  byteView.set(encoder.encode("WAVE"), 8);
  byteView.set(encoder.encode("fmt "), 12);
  header.setUint32(16, 16, true);
  header.setUint16(20, 1, true);
  header.setUint16(22, channelCount, true);
  header.setUint32(24, sampleRate, true);
  header.setUint32(28, sampleRate * 4, true);
  header.setUint16(32, channelCount * 2, true);
  header.setUint16(34, 16, true);
  byteView.set(encoder.encode("data"), 36);
  header.setUint32(40, byteCount, true);
  return header;
}

export function encodeWav(buffers: Float32Array[], sampleRate: number): Blob {
  const view = new DataView(
    new ArrayBuffer(buffers.reduce((cum, curr) => cum + curr.length, 0) * 2)
  );
  let i = 0;
  for (const buffer of buffers) {
    for (const float of buffer) {
      view.setInt16(i * 2, Math.min(Math.max(float, -1), 1) * 0x7fff, true);
      i++;
    }
  }
  return new Blob([header(view.byteLength, sampleRate), view], {
    type: "audio/wav",
  });
}

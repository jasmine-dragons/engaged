"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import styles from "./page.module.css";

export default function Start() {
  const searchParams = useSearchParams();

  const [started, setStarted] = useState(false);

  const webcamPreviewRef = useRef<HTMLVideoElement>(null);
  const screenPreviewRef = useRef<HTMLVideoElement>(null);

  async function startZoom() {
    setStarted(true);

    const audioStream = await navigator.mediaDevices.getUserMedia({
      audio: true,
    });
    const videoStream = await navigator.mediaDevices.getUserMedia({
      video: true,
    });
    const screenStream = await navigator.mediaDevices.getDisplayMedia({
      video: true,
    });

    if (webcamPreviewRef.current) {
      webcamPreviewRef.current.srcObject = videoStream;
      webcamPreviewRef.current.play();
    }
    if (screenPreviewRef.current) {
      screenPreviewRef.current.srcObject = screenStream;
      screenPreviewRef.current.play();
    }

    const audioRecorder = new MediaRecorder(audioStream);

    audioRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        // TODO: send audio chunk
        console.log(event.data);
      }
    };

    audioRecorder.start(3000); // Send audio every 3 seconds

    setInterval(() => captureFrame(screenStream, "screen"), 5000);
    setInterval(() => captureFrame(videoStream, "webcam"), 5000);

    function captureFrame(stream: MediaStream, type: "screen" | "webcam") {
      const track = stream.getVideoTracks()[0];
      if (!track) return;

      const imageCapture = new ImageCapture(track);
      imageCapture.grabFrame().then((bitmap) => {
        const canvas = document.createElement("canvas");
        canvas.width = bitmap.width;
        canvas.height = bitmap.height;
        const ctx = canvas.getContext("2d");
        if (!ctx) {
          throw new TypeError("no context :(");
        }
        ctx.drawImage(bitmap, 0, 0);

        canvas.toBlob((blob) => {
          if (blob) {
            // TODO: send video frame
            console.log(URL.createObjectURL(blob));
          }
        }, "image/jpeg");
      });
    }
  }

  return (
    <div className="container">
      <h1 className="heading">Your experience is ready.</h1>
      <p>Click the link below to join your simulated classroom experience.</p>
      {!started ? (
        <button
          style={{ alignSelf: "flex-start" }}
          type="button"
          className="button"
          onClick={startZoom}
        >
          Begin Class
        </button>
      ) : null}
      <div className={styles.videos} style={{ display: started ? "" : "none" }}>
        <video
          className={styles.video}
          ref={webcamPreviewRef}
          playsInline
        ></video>
        <video
          className={styles.video}
          ref={screenPreviewRef}
          playsInline
        ></video>
      </div>
    </div>
  );
}

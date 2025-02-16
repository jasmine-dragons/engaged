"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import styles from "./page.module.css";
import { makeManager, Manager } from "@/lib/MeetingManager";

export default function Start() {
  const searchParams = useSearchParams();

  const [started, setStarted] = useState(false);
  const [sharing, setSharing] = useState(false);

  const webcamPreviewRef = useRef<HTMLVideoElement>(null);
  const screenPreviewRef = useRef<HTMLVideoElement>(null);

  const managerRef = useRef<Manager>(null);
  useEffect(() => {
    return () => {
      managerRef.current?.kill();
    };
  }, []);

  async function startZoom() {
    if (webcamPreviewRef.current && screenPreviewRef.current) {
      setStarted(true);
      setSharing(false);
      managerRef.current = await makeManager(
        webcamPreviewRef.current,
        screenPreviewRef.current
      );
    }
  }

  return (
    <div className="container">
      <h1 className="heading">Your experience is ready.</h1>
      <p>Click the link below to join your simulated classroom experience.</p>
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
          style={{ display: sharing ? "" : "none" }}
        ></video>
      </div>
      <div className={styles.buttons}>
        {!started ? (
          <button type="button" className="button" onClick={startZoom}>
            Begin Class
          </button>
        ) : (
          <>
            <button
              type="button"
              className="button"
              onClick={() => {
                managerRef.current
                  ?.screenShare(true)
                  .then(() => setSharing(true))
                  .catch(() => setSharing(false));
              }}
            >
              {sharing ? "Change Screen" : "Share Screen"}
            </button>
            {sharing ? (
              <button
                type="button"
                className="button"
                onClick={() => {
                  managerRef.current?.screenShare(false);
                  setSharing(false);
                }}
              >
                Stop Sharing
              </button>
            ) : null}
            <button
              type="button"
              className="button"
              onClick={() => {
                managerRef.current?.kill();
                setStarted(false);
              }}
            >
              End Meeting
            </button>
          </>
        )}
      </div>
    </div>
  );
}

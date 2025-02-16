"use client";

import childImage from "@/../public/DEMO_CHILD.jpg";
import { makeManager, Manager } from "@/lib/MeetingManager";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import styles from "./page.module.css";
import Image from "next/image";
import { getAnalytics } from "@/lib/api";

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
      <h1 className={`heading ${styles.heading}`}>Your experience is ready.</h1>
      <p className={styles.instruction}>
        Click the link below to join your simulated classroom experience.
      </p>
      <div
        className={`${styles.videos} ${sharing ? styles.sharing : styles.grid}`}
        style={{ display: started ? "" : "none" }}
      >
        {sharing ? (
          <div className={styles.warning}>You are screen sharing</div>
        ) : null}
        <video
          className={styles.screenShare}
          ref={screenPreviewRef}
          playsInline
          style={{ display: sharing ? "" : "none" }}
        ></video>
        <div className={styles.people}>
          <div
            className={`${styles.person} ${styles.speaking} ${styles.hasVideo}`}
            data-name="You (Host)"
          >
            <video
              className={styles.video}
              ref={webcamPreviewRef}
              playsInline
            ></video>
          </div>
          {Array.from({ length: 4 }, (_, i) => (
            <div
              key={i}
              className={`${styles.person} ${i === 2 ? styles.speaking : ""}`}
              data-name="John Asshole"
            >
              <Image
                src={childImage}
                alt="person"
                width={80}
                height={80}
                className={styles.pfp}
              />
            </div>
          ))}
        </div>
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
              onClick={async () => {
                managerRef.current?.kill();
                setStarted(false);
                await new Promise((resolve) => setTimeout(resolve, 1000));
                console.log(await getAnalytics());
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

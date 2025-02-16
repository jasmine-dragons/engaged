"use client";

import { makeManager, Manager } from "@/lib/MeetingManager";
import Link from "next/link";
import { redirect, RedirectType, useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import styles from "./page.module.css";
import Image, { StaticImageData } from "next/image";
import { getAnalytics } from "@/lib/api";
import { allStudents } from "@/lib/students";

type Student = {
  id: string;
  name: string;
  image: string | StaticImageData;
  speaking: boolean;
};

export default function Start() {
  const [started, setStarted] = useState(false);
  const [sharing, setSharing] = useState(false);
  const [loading, setLoading] = useState(false);

  const [students, setStudents] = useState<Student[]>([]);

  const webcamPreviewRef = useRef<HTMLVideoElement>(null);
  const screenPreviewRef = useRef<HTMLVideoElement>(null);

  const managerRef = useRef<Manager>(null);
  useEffect(() => {
    return () => {
      managerRef.current?.kill();
      managerRef.current = null;
    };
  }, []);

  async function endMeeting() {
    if (!managerRef.current) {
      return;
    }
    managerRef.current.kill();
    managerRef.current = null;
    setLoading(true);
    setStarted(false);
    const { simId, analytics } = await getAnalytics();
    console.log(analytics);
    redirect(`/results/${simId}`, RedirectType.push);
  }

  async function startZoom() {
    if (webcamPreviewRef.current && screenPreviewRef.current) {
      setStarted(true);
      setSharing(false);
      managerRef.current = await makeManager(
        webcamPreviewRef.current,
        screenPreviewRef.current,
        endMeeting,
        (students) =>
          setStudents(
            students.map(([id, personality, { name }]) => ({
              id,
              name,
              image:
                allStudents.find((s) => s.personality === personality)?.image ??
                "",
              speaking: false,
            }))
          ),
        (studentId, speaking) =>
          setStudents((students) =>
            students.map((s) => (s.id === studentId ? { ...s, speaking } : s))
          )
      );
    }
  }

  return (
    <div className="container">
      <h1 className="heading">Your experience is ready.</h1>
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
          {students.map(({ id, image, name, speaking }) => (
            <div
              key={id}
              className={`${styles.person} ${speaking ? styles.speaking : ""}`}
              data-name={name}
            >
              <Image
                src={image}
                alt={name}
                width={80}
                height={80}
                className={styles.pfp}
              />
            </div>
          ))}
        </div>
      </div>
      <div className={styles.buttons}>
        {loading ? (
          <button className="button" type="button" disabled>
            <span className={styles.spinner} /> Analyzing session...
          </button>
        ) : !started ? (
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
            <button type="button" className="button" onClick={endMeeting}>
              End Meeting
            </button>
          </>
        )}
      </div>
    </div>
  );
}

"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useRef } from "react";
import styles from "./page.module.css";

export default function Start() {
  const searchParams = useSearchParams();

  return (
    <div className={styles.container}>
      <h1 className={styles.heading}>Your experience is ready.</h1>
      <p>Click the link below to join your simulated classroom experience.</p>
      <pre>{searchParams.get("personalities")}</pre>
      <Link href="#" className={styles.button}>
        Begin Class
      </Link>
      <div className="container">
        <div className="main-content">
          <div className="meeting-header">
            <h2 className="meeting-title">RTMS Mock Server</h2>
          </div>

          <div className="form-group">
            <div className="url-container">
              <label>
                Provide Webhook URL. To know more about Zoom Webhooks, visit{" "}
                <a
                  href="https://developers.zoom.us/docs/api/webhooks/"
                  target="_blank"
                >
                  here
                </a>
                .
              </label>

              <input
                type="text"
                id="webhookUrl"
                placeholder="Enter Webhook URL"
              />
              <button id="validateBtn">
                <i className="fas fa-check-circle"></i> Validate
              </button>
            </div>
          </div>

          <div className="video-container">
            <video id="mediaVideo" autoPlay playsInline muted></video>
            <audio id="mediaAudio" autoPlay></audio>
          </div>

          <div className="controls">
            <button id="sendBtn" disabled>
              <i className="fas fa-video"></i> Start Meeting
            </button>
            <button id="pauseBtn" disabled>
              <i className="fas fa-pause"></i> Pause RTMS
            </button>
            <button id="resumeBtn" disabled>
              <i className="fas fa-play"></i> Resume RTMS
            </button>
            <button id="stopBtn" disabled>
              <i className="fas fa-stop"></i> Stop RTMS
            </button>
            <button id="startRtmsBtn" disabled>
              <i className="fas fa-play-circle"></i> Start RTMS
            </button>
            <button id="endBtn" disabled>
              <i className="fas fa-phone-slash"></i> End Meeting
            </button>
          </div>
        </div>

        <div className="sidebar">
          <div className="log-tabs">
            <button className="tab-button active" data-tab="transcripts">
              Transcripts
            </button>
            <button className="tab-button" data-tab="logs">
              Logs
            </button>
          </div>

          <div id="transcripts-container" className="logs-container">
            <div id="transcript"></div>
          </div>

          <div
            id="logs-container"
            className="logs-container"
            style={{ display: "none" }}
          >
            <div id="system-logs"></div>
          </div>
        </div>
      </div>

      <script src="/js/config.js"></script>

      <script src="/js/api.js"></script>

      <script src="/js/mediaHandler.js"></script>
      <script src="/js/webSocket.js"></script>

      <script src="/js/uiController.js"></script>

      <script src="/js/audio-processor.js"></script>
    </div>
  );
}

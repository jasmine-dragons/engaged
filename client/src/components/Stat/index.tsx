"use client";

import { useEffect, useState } from "react";
import styles from "./index.module.css";

const ANIM_DURATION = 2000;

export type StatProps = {
  label: string;
  count: number;
  fixed?: number;
  units?: string;
  min: number;
  avg: number;
  max: number;
  animate?: boolean;
  rightAlign?: boolean;
};
export function Stat({
  label,
  count,
  fixed = 0,
  units,
  min,
  avg,
  max,
  animate = false,
  rightAlign = false,
}: StatProps) {
  const [progress, setProgress] = useState(animate ? 0 : 1);

  useEffect(() => {
    if (!animate) {
      setProgress(1);
      return;
    }
    const start = Date.now();
    let requestId = 0;
    const paint = () => {
      const now = Date.now();
      if (now > start + ANIM_DURATION) {
        setProgress(1);
      } else {
        const progress = (now - start) / ANIM_DURATION;
        setProgress((progress - 1) ** 3 + 1);
        requestId = window.requestAnimationFrame(paint);
      }
    };
    paint();
    return () => {
      window.cancelAnimationFrame(requestId);
    };
  }, [animate]);

  return (
    <div className={styles.stat}>
      <span
        className={`${styles.label} ${rightAlign ? styles.rightAlign : ""}`}
      >
        {label}{" "}
      </span>
      <span className={styles.measure}>
        <span className={styles.count}>
          {(progress * count).toFixed(fixed)}
        </span>
        {units}
      </span>
    </div>
  );
}

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
};
export function Stat({
  label,
  count,
  fixed = 0,
  units,
  min,
  avg,
  max,
}: StatProps) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
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
  }, []);

  return (
    <div className={styles.stat}>
      <span className={styles.label}>{label} </span>
      <span className={styles.measure}>
        <span className={styles.count}>
          {(progress * count).toFixed(fixed)}
        </span>
        {units}
      </span>
    </div>
  );
}

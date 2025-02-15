"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useRef } from "react";
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
    </div>
  );
}

import styles from "./page.module.css";
import Link from "next/link";

export default async function Home() {
  return (
    <div className={styles.page}>
      <video
        src="/LAUGHLAUGHLAUGHHAHAHA.mp4"
        className={styles.video}
        autoPlay
        muted
        loop
      />
      <h1 className={styles.title}>Teacher Teacher</h1>
      <p className={styles.tagline}>Predict the unpredictable.</p>
      <Link href="/login" className="button">
        Log In
      </Link>
    </div>
  );
}

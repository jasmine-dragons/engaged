import Link from "next/link";
import styles from "./page.module.css";

export default function Start() {
  return (
    <div className={styles.container}>
      <h1 className={styles.heading}>Your experience is ready.</h1>
      <p>Click the link below to join your simulated classroom experience.</p>
      <Link href="#" className={styles.button}>
        Begin Class
      </Link>
    </div>
  );
}

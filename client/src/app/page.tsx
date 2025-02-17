import styles from "./page.module.css";
import Link from "next/link";
import PersonAtDeskZoom from "@/../public/remote learning.svg";
import Whiteboard from "@/../public/teaching.svg";
import PersonPcWindow from "@/../public/videolearning.svg";
import Image from "next/image";

export default async function Home() {
  return (
    <div className={styles.page}>
      <nav className={styles.nav}>
        <Link href="/login" className={`button ${styles.login}`}>
          Log In
        </Link>
      </nav>
      <div className={styles.hero}>
        <div className={styles.content}>
          <h1 className={styles.title}>
            engag<strong className={styles.ed}>ed</strong>
          </h1>
          <p className={styles.tagline}>
            An AI-powered classroom simulator that helps teachers practice
            real-world classroom management in a risk-free environment. Interact
            with dynamic student personalities, refine your teaching strategies,
            and receive real-time feedback—all to build confidence and improve
            student engagement.
          </p>
          <Image
            src={PersonAtDeskZoom}
            alt="A person sits at a desk holding paper while a different person waits on their computer screen"
            height={300}
            className={styles.imageBottom}
          />
        </div>
        <div className={styles.blobWrapper}>
          <div className={styles.blob} />
          <Image
            src={PersonPcWindow}
            alt="A person in a desktop window does a presentation while two people look at her"
            className={styles.imageRight}
          />
        </div>
      </div>
    </div>
  );
}

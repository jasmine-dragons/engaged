import Image from "next/image";
import childImage from "@/../public/DEMO_CHILD.jpg";
import styles from "./page.module.css";

export default function Setup() {
  return (
    <div className={styles.container}>
      <h1 className={styles.heading}>Set up your classroom.</h1>
      <p>Choose from one of our classroom templates.</p>
      <div></div>
      <p>Or build your own class of students.</p>
      <div></div>
      <div className={styles.bottom}>
        <p>1 of 4 students selected.</p>
        <button className={styles.button} type="button">
          Next
        </button>
      </div>
    </div>
  );
}

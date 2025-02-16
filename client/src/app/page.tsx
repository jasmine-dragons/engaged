import styles from "./page.module.css";
import Link from "next/link";

export default async function Home() {
  return (
    <div className={styles.page}>
      <h1>landing page</h1>
      <p>
        pages: <Link href="/setup">setup</Link>,{" "}
        <Link href="/start">start</Link>
      </p>
    </div>
  );
}

import Image from "next/image";
import styles from "./page.module.css";
import Link from "next/link";
import { healthCheck } from "@/lib/api";

export default async function Home() {
  const status = await healthCheck();
  return (
    <div className={styles.page}>
      <h1>landing page</h1>
      <p>
        pages: <Link href="/setup">setup</Link>,{" "}
        <Link href="/start">start</Link>
      </p>
      <pre>from backend: {JSON.stringify(status)}</pre>
    </div>
  );
}

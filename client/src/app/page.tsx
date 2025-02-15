import Image from "next/image";
import styles from "./page.module.css";
import Link from "next/link";
import { healthCheck } from "@/lib/api";

export default async function Home() {
  const status = await healthCheck();
  return (
    <div className={styles.page}>
      <h1>landing page</h1>
      <pre>{JSON.stringify(status)}</pre>
      <Link href="/setup">i'm interest</Link>
    </div>
  );
}

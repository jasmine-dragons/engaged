import styles from "./page.module.css";
import { Stat } from "@/components/Stat";
import { dateFormat } from "@/lib/fmt";
import { getSimulation } from "@/lib/api";
import { notFound } from "next/navigation";
import Image from "next/image";
import { allStudents } from "@/lib/students";
import childImage from "@/../public/DEMO_CHILD.jpg";
import Link from "next/link";

type ResultsPageProps = {
  params: Promise<{ simId: string }>;
};
export default async function ResultsPage({ params }: ResultsPageProps) {
  const { simId } = await params;
  const { data } = await getSimulation(simId);

  if (!data) {
    notFound();
  }
  console.log(data);

  return (
    <div className="container">
      <h1 className="heading">Results</h1>
      <div className={styles.wrapper}>
        <div className={styles.transcriptWrapper}>
          <h2>Transcript</h2>
          <ul className={styles.transcript}>
            {data.transcript
              .filter((t) => t.text)
              .map(({ text, speaker, timestamp }, i) => {
                const personality = speaker.split("_")[1];
                return (
                  <li
                    className={`${styles.messageItem} ${
                      speaker === "teacher"
                        ? styles.messageRight
                        : styles.messageLeft
                    }`}
                    style={{ animationDelay: `${(i + 1) * 50}ms` }}
                    key={i}
                  >
                    {speaker !== "teacher" ? (
                      <Image
                        src={
                          allStudents.find((s) => s.personality === personality)
                            ?.image ?? childImage
                        }
                        alt={speaker}
                        width={40}
                        height={40}
                        className={styles.who}
                      />
                    ) : null}
                    <div className={styles.message}>{text}</div>
                  </li>
                );
              })}
          </ul>
        </div>
        <div className={styles.sidebar}>
          {"error" in data.analytics ? (
            <p>Analysis failed: {data.analytics.error}</p>
          ) : (
            <>
              <h2>Stats</h2>
              <div className={styles.stats}>
                <Stat
                  label="talk speed"
                  count={data.analytics.speech_rate_wpm}
                  units=" wpm"
                  min={100}
                  avg={135}
                  max={180}
                  animate
                />
                <Stat
                  label="emotion"
                  count={4}
                  fixed={1}
                  min={1}
                  avg={3}
                  max={5}
                  animate
                />
                <Stat
                  label="talk time ratio"
                  count={80}
                  units="%"
                  min={60}
                  avg={77.5}
                  max={90}
                  animate
                />
                <Stat
                  label="filler words"
                  count={Object.values(
                    data.analytics.filler_words_count
                  ).reduce((a, b) => a + b, 0)}
                  min={0}
                  avg={7.5}
                  max={15}
                  animate
                />
              </div>
              <h2>Suggestions</h2>
              <p>{data.analytics.suggestions}</p>
            </>
          )}
          {data.personalities ? (
            <div className={styles.children}>
              {data.personalities.map((personality, i) => (
                <Image
                  src={
                    allStudents.find((s) => s.personality === personality)
                      ?.image ?? childImage
                  }
                  alt={personality}
                  width={40}
                  height={40}
                  className={styles.child}
                  key={i}
                  style={{ zIndex: (data.personalities?.length ?? 0) - i }}
                />
              ))}
              <Link
                href={`/setup?${new URLSearchParams({
                  p: data.personalities.join("\n"),
                })}`}
                className={styles.retry}
              >
                Retry class →
              </Link>
            </div>
          ) : null}
          <p className={styles.timestamp}>
            {dateFormat.format(new Date(data.timestamp))}
          </p>
        </div>
      </div>
    </div>
  );
}

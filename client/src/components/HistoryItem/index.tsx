import { dateFormat } from "@/lib/fmt";
import { Analysis } from "@/lib/types";
import Link from "next/link";
import styles from "./index.module.css";
import { Stat } from "../Stat";
import { CSSProperties } from "react";

export type HistoryItemProps = {
  analysis: Analysis;
  style?: CSSProperties;
};
export function HistoryItem({ analysis, style }: HistoryItemProps) {
  return (
    <Link href="/results/1139475891" className={styles.wrapper} style={style}>
      <div className={styles.left}>
        <p className={styles.timestamp}>{dateFormat.format(analysis.time)}</p>
        <p className={styles.summary}>{analysis.summary}</p>
      </div>
      <div className={styles.stats}>
        <Stat
          label="talk speed"
          count={analysis.ratings.talkSpeed}
          units=" wpm"
          min={100}
          avg={135}
          max={180}
        />
        <Stat
          label="emotion"
          count={analysis.ratings.emotion}
          fixed={1}
          min={1}
          avg={3}
          max={5}
        />
        <Stat
          label="talk time ratio"
          count={analysis.ratings.talkTimeRatio}
          units="%"
          min={60}
          avg={77.5}
          max={90}
        />
        <Stat
          label="filler words"
          count={analysis.ratings.fillerWords}
          min={0}
          avg={7.5}
          max={15}
        />
      </div>
    </Link>
  );
}

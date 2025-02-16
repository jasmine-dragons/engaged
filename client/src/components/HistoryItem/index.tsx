import { dateFormat } from "@/lib/fmt";
import { Analysis } from "@/lib/types";
import Link from "next/link";
import styles from "./index.module.css";
import { Stat } from "../Stat";
import { CSSProperties } from "react";
import { HistoricEntry } from "@/lib/api";

export type HistoryItemProps = {
  analysis: HistoricEntry;
  style?: CSSProperties;
};
export function HistoryItem({ analysis, style }: HistoryItemProps) {
  return (
    <Link
      href={`/results/${analysis.simulation_id_str}`}
      className={styles.wrapper}
      style={style}
    >
      <div className={styles.left}>
        <p className={styles.timestamp}>
          {dateFormat.format(new Date(analysis.timestamp))}
        </p>
        <p className={styles.summary}>
          {"error" in analysis.analytics ? "" : analysis.analytics.suggestions}
        </p>
      </div>
      {"error" in analysis.analytics ? null : (
        <div className={styles.stats}>
          <Stat
            label="talk speed"
            count={analysis.analytics.speech_rate_wpm}
            units=" wpm"
            min={100}
            avg={135}
            max={180}
            rightAlign
          />
          <Stat label="emotion" count={0} fixed={1} min={1} avg={3} max={5} />
          <Stat
            label="talk time ratio"
            count={0}
            units="%"
            min={60}
            avg={77.5}
            max={90}
          />
          <Stat
            label="filler words"
            count={Object.values(analysis.analytics.filler_words_count).reduce(
              (a, b) => a + b,
              0
            )}
            min={0}
            avg={7.5}
            max={15}
          />
        </div>
      )}
    </Link>
  );
}

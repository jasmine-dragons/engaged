import { Analysis } from "@/lib/types";
import styles from "./page.module.css";
import { Stat } from "@/components/Stat";
import { dateFormat } from "@/lib/fmt";
import { getSimulation } from "@/lib/api";
import { notFound } from "next/navigation";

const result: Analysis = {
  transcript: [
    {
      what: "Alright class, settle in, settle in! Today, we're diving into the fascinating world of cellular biology, and specifically, we're going to explore an organelle that's absolutely crucial for life as we know it: the mitochondrion.  (Slight pause)  Can anyone tell me what they already know about mitochondria?  Don't be shy!",
    },
    { what: "Yes, Sarah?" },
    {
      who: "Sarah",
      what: "I think… I think they have something to do with energy?",
    },
    {
      what: "Absolutely, Sarah!  That's exactly right. Mitochondria are often called the \"powerhouses of the cell,\" and for good reason.  They're the primary sites of cellular respiration. Now, what does that mean?  Well, cellular respiration is the process by which our cells take the food we eat, break it down, and convert it into a form of energy that the cell can actually use.  Think of it like this: you eat an apple, right? That apple contains energy, but your cells can't directly use the energy in the apple.  It's like trying to plug a European plug into an American socket – it just won't work.  Mitochondria are the adaptors, if you will.",
    },
    {
      what: "They take that energy from the apple, and through a complex series of chemical reactions, they transform it into ATP.  ATP is like the cell's energy currency. It's the fuel that powers everything the cell does, from muscle contractions to building new proteins.  So, without mitochondria, our cells would be completely energy-starved.  We wouldn't be able to move, think, or even stay alive!",
    },
    {
      what: "Now, let's take a closer look at the structure of a mitochondrion.  As you can see, it has a double membrane.  There's the outer membrane, which is relatively smooth, and then there's the inner membrane, which is folded into these…  (Slight pause, points to folds) … these cristae.  These folds increase the surface area within the mitochondrion, which allows for more of those energy-producing reactions to take place.  Think of it like… like crumpling up a piece of paper.  It takes up the same amount of paper, but it fits into a smaller space and has more surface area.",
    },
    {
      what: "So, remember, mitochondria: powerhouses of the cell, responsible for cellular respiration, producing ATP, and crucial for life!  Any questions?",
    },
  ],
  summary:
    'The teacher explains that mitochondria are the "powerhouses of the cell" because they are the primary sites of cellular respiration.  Cellular respiration is the process of converting food into usable energy in the form of ATP.  The teacher uses the analogy of an apple and a plug to explain how mitochondria convert the energy in food into a usable form for the cell.  The teacher also describes the structure of a mitochondrion, highlighting the double membrane and the cristae, which increase the surface area for cellular respiration.  The overall message is that mitochondria are essential for life.',
  ratings: {
    talkSpeed: 120,
    emotion: 4,
    talkTimeRatio: 80,
    fillerWords: 5,
  },
  time: new Date("2024-10-27T10:00:00"),
};

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
            {data.transcript.map(({ text, speaker, timestamp }, i) => (
              <li
                className={`${styles.messageItem} ${
                  speaker === "teacher"
                    ? styles.messageRight
                    : styles.messageLeft
                }`}
                style={{ animationDelay: `${(i + 1) * 50}ms` }}
                key={i}
              >
                {speaker !== "teacher" ? <div className={speaker} /> : null}
                <div className={styles.message}>{text}</div>
              </li>
            ))}
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
                  count={result.ratings.emotion}
                  fixed={1}
                  min={1}
                  avg={3}
                  max={5}
                  animate
                />
                <Stat
                  label="talk time ratio"
                  count={result.ratings.talkTimeRatio}
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
          <p className={styles.timestamp}>
            {dateFormat.format(new Date(data.timestamp))}
          </p>
        </div>
      </div>
    </div>
  );
}

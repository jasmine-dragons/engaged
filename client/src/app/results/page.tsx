import { Analysis } from "@/lib/types";
import styles from "./page.module.css";

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
};

export default function Results() {
  return (
    <div className="container">
      <h1 className="heading">Results</h1>
      <div className={styles.wrapper}>
        <ul className={styles.transcript}>
          {result.transcript.map(({ who, what }, i) => (
            <li
              className={`${styles.messageItem} ${
                who ? styles.messageLeft : styles.messageRight
              }`}
              key={i}
            >
              {who ? <div className={styles.who} /> : null}
              <div className={styles.message}>{what}</div>
            </li>
          ))}
        </ul>
        <div className={styles.sidebar}>
          <h2>Summary</h2>
          <p>{result.summary}</p>
        </div>
      </div>
    </div>
  );
}

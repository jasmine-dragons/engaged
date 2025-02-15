"use client";

import { Classroom } from "@/components/Classroom";
import styles from "./page.module.css";
import { Student } from "@/components/Student";
import { ClassroomTemplate, StudentTemplate } from "@/lib/types";
import childImage from "@/../public/DEMO_CHILD.jpg";
import { useState } from "react";
import { startSession } from "./actions";

const MAX_STUDENTS = 5;
const students: StudentTemplate[] = [
  {
    name: "Emily Carter",
    description:
      "Emily is always enthusiastic and eager to learn new things. Her energy is infectious, and she brings a positive vibe to any group project.",
    personality: "excitable",
  },
  {
    name: "Jason Maxwell",
    description:
      "Jason is a highly competitive and driven individual. He's not afraid to voice his opinions, even if they're unpopular, and he can sometimes come across as abrasive.",
    personality: "asshole",
  },
  {
    name: "David Lee",
    description:
      "David prefers routine and avoids taking risks. He's a reliable student who consistently completes his assignments, but he rarely contributes anything innovative or exciting.",
    personality: "boring",
  },
  {
    name: "Sarah Chen",
    description:
      "Sarah is a balanced and well-rounded student. She's friendly and approachable, participates in class discussions, and works well with others. She's a good all-around team player.",
    personality: "normal",
  },
];
const classrooms: ClassroomTemplate[] = [
  {
    name: "An Ordinary Classroom",
    students: ["boring", "normal", "normal", "excitable"],
  },
  {
    name: "You Would Want to Avoid This",
    students: ["asshole", "asshole", "asshole"],
  },
];

export default function Setup() {
  const [selection, setSelection] = useState<Record<string, number>>({});
  const totalSelected = Object.values(selection).reduce((a, b) => a + b, 0);

  const [loading, setLoading] = useState(false);

  return (
    <div className="container">
      <h1 className="heading">Set up your classroom.</h1>
      <p>Start with one of our classroom templates.</p>
      <div className={`${styles.gridIsh} ${styles.classrooms}`}>
        {classrooms.map(({ name, students }) => {
          let selected = true;
          const sel = { ...selection };
          for (const personality of students) {
            if (sel[personality] && sel[personality] > 0) {
              sel[personality]--;
              if (sel[personality] <= 0) {
                delete sel[personality];
              }
            } else {
              selected = false;
              break;
            }
          }
          if (Object.keys(sel).length > 0) {
            selected = false;
          }
          return (
            <Classroom
              key={name}
              name={name}
              studentImages={students.map(() => ({
                src: childImage,
                name: "todo",
              }))}
              onClick={() => {
                const sel: Record<string, number> = {};
                for (const personality of students) {
                  sel[personality] ??= 0;
                  sel[personality]++;
                }
                setSelection(sel);
              }}
              selected={selected}
            />
          );
        })}
      </div>
      <p>Or build your own class of students.</p>
      <div className={styles.gridIsh}>
        {students.map(({ name, description, personality }) => (
          <Student
            key={personality}
            name={name}
            description={description}
            count={selection[personality] ?? 0}
            onCount={(count) =>
              setSelection((sel) => ({ ...sel, [personality]: count }))
            }
          />
        ))}
      </div>
      <div className={styles.bottom}>
        <p className={styles.count}>
          {totalSelected} of {MAX_STUDENTS} students selected.
        </p>
        <button
          className={styles.button}
          type="button"
          disabled={
            totalSelected === 0 || totalSelected > MAX_STUDENTS || loading
          }
          onClick={() => {
            setLoading(true);
            startSession(
              Object.entries(selection).flatMap(([personality, count]) =>
                Array.from({ length: count }, () => personality)
              )
            );
          }}
        >
          {loading ? <span className={styles.spinner} /> : null}
          Next
        </button>
      </div>
    </div>
  );
}

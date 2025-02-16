"use client";

import { Classroom } from "@/components/Classroom";
import styles from "./page.module.css";
import { Student } from "@/components/Student";
import { Suspense, useState } from "react";
import { startSession } from "./actions";
import { classrooms, allStudents, MAX_STUDENTS } from "@/lib/students";
import { useSearchParams } from "next/navigation";

function Setup() {
  const params = useSearchParams();
  const personalities = params.get("p")?.split("\n") ?? [];
  const defaultSelection: Record<string, number> = {};
  for (const personality of personalities) {
    defaultSelection[personality] ??= 0;
    defaultSelection[personality]++;
  }

  const [selection, setSelection] =
    useState<Record<string, number>>(defaultSelection);
  const totalSelected = Object.values(selection).reduce((a, b) => a + b, 0);

  const [loading, setLoading] = useState(false);

  return (
    <div className="container">
      <h1 className="heading">Set up your classroom.</h1>
      <p className={styles.instruction}>
        Start with one of our classroom templates.
      </p>
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
              studentImages={students
                .map((personality) => {
                  const student = allStudents.find(
                    (s) => s.personality === personality
                  );
                  return student
                    ? { src: student.image, name: student.name }
                    : null;
                })
                .filter((s) => !!s)}
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
      <p className={styles.or}>Or build your own class of students.</p>
      <div className={`${styles.gridIsh} ${styles.students}`}>
        {allStudents.map(({ name, description, personality, image }) => (
          <Student
            key={personality}
            name={name}
            description={description}
            image={image}
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
          className="button"
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

export default function SetupWrapped() {
  return (
    <Suspense>
      <Setup />
    </Suspense>
  );
}

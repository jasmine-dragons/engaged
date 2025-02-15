import { Classroom } from "@/components/Classroom";
import styles from "./page.module.css";
import { Student } from "@/components/Student";

const classrooms = ["An Ordinary Classroom", "You Would Want to Avoid This"];
const students = ["excitable", "asshole", "boring", "normal"];

export default function Setup() {
  return (
    <div className={styles.container}>
      <h1 className={styles.heading}>Set up your classroom.</h1>
      <p>Start with one of our classroom templates.</p>
      <div className={`${styles.gridIsh} ${styles.classrooms}`}>
        {classrooms.map((name) => (
          <Classroom key={name} name={name} />
        ))}
      </div>
      <p>Or build your own class of students.</p>
      <div className={styles.gridIsh}>
        {students.map((student) => (
          <Student
            key={student}
            name={`John ${student[0].toUpperCase()}${student.slice(1)}`}
            description={`A really ${student} kid. Like, really, really ${student}. I once met them in like fifth grade and became ${student} myself. That's how ${student} they are.`}
          />
        ))}
      </div>
      <div className={styles.bottom}>
        <p className={styles.count}>1 of 4 students selected.</p>
        <button className={styles.button} type="button">
          Next
        </button>
      </div>
    </div>
  );
}

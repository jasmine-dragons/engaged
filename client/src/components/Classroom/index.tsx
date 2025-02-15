import Image from "next/image";
import styles from "./index.module.css";
import classImage from "@/../public/classroom.png";
import childImage from "@/../public/DEMO_CHILD.jpg";

export type ClassroomProps = {
  name: string;
};
export function Classroom({ name }: ClassroomProps) {
  return (
    <button className={styles.card}>
      <div className={styles.imageWrapper}>
        <Image src={classImage} alt="classroom" fill className={styles.image} />
      </div>
      <div className={styles.contents}>
        <p className={styles.name}>{name}</p>
        <div className={styles.children}>
          {Array.from({ length: 5 }, (_, i) => (
            <Image
              src={childImage}
              alt="child"
              width={40}
              height={40}
              className={styles.child}
              key={i}
              style={{ zIndex: 10 - i }}
            />
          ))}
          <p className={styles.total}>4 students</p>
        </div>
      </div>
    </button>
  );
}

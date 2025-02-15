import Image, { StaticImageData } from "next/image";
import styles from "./index.module.css";
import classImage from "@/../public/classroom.png";

export type ClassroomProps = {
  name: string;
  studentImages: { src: string | StaticImageData; name: string }[];
  onClick: () => void;
  selected?: boolean;
};
export function Classroom({
  name,
  studentImages,
  onClick,
  selected,
}: ClassroomProps) {
  return (
    <button
      className={`${styles.card} ${selected ? styles.selected : ""}`}
      onClick={onClick}
    >
      <div className={styles.imageWrapper}>
        <Image src={classImage} alt="classroom" fill className={styles.image} />
      </div>
      <div className={styles.contents}>
        <p className={styles.name}>{name}</p>
        <div className={styles.children}>
          {studentImages.map(({ src, name }, i) => (
            <Image
              src={src}
              alt={name}
              width={40}
              height={40}
              className={styles.child}
              key={i}
              style={{ zIndex: studentImages.length - i }}
            />
          ))}
          <p className={styles.total}>{studentImages.length} students</p>
        </div>
      </div>
    </button>
  );
}

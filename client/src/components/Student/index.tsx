import Image, { StaticImageData } from "next/image";
import styles from "./index.module.css";

export type StudentProps = {
  name: string;
  description: string;
  image: string | StaticImageData;
  count: number;
  onCount: (count: number) => void;
};
export function Student({
  name,
  description,
  image,
  count,
  onCount,
}: StudentProps) {
  return (
    <div className={styles.card}>
      <Image
        src={image}
        alt="child"
        width={80}
        height={80}
        className={styles.pfp}
      />
      <p className={styles.name}>{name}</p>
      <p className={styles.description}>{description}</p>
      <div className={styles.counter}>
        <button
          className={styles.btn}
          onClick={() => onCount(count - 1)}
          disabled={count <= 0}
        >
          &minus;
        </button>
        <div className={styles.count}>{count}</div>
        <button className={styles.btn} onClick={() => onCount(count + 1)}>
          +
        </button>
      </div>
    </div>
  );
}

import Image from "next/image";
import styles from "./index.module.css";
import childImage from "@/../public/DEMO_CHILD.jpg";

export type StudentProps = {
  name: string;
  description: string;
};
export function Student({ name, description }: StudentProps) {
  return (
    <div className={styles.card}>
      <Image
        src={childImage}
        alt="child"
        width={80}
        height={80}
        className={styles.pfp}
      />
      <p className={styles.name}>{name}</p>
      <p className={styles.description}>{description}</p>
    </div>
  );
}

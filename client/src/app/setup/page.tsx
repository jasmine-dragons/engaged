import Image from "next/image";
import childImage from "@/../public/DEMO_CHILD.jpg";
import child from "./page.module.css";

export default function Setup() {
  return (
    <form>
      <h1>choose ur classroom</h1>
      <div>
        <button className={child.children}>
          <Image
            className={child.src}
            width={40}
            height={40}
            src={childImage}
            alt="child"
          />
          <Image
            className={child.src}
            width={40}
            height={40}
            src={childImage}
            alt="child"
          />
          <Image
            className={child.src}
            width={40}
            height={40}
            src={childImage}
            alt="child"
          />
        </button>
      </div>
      <button type="submit">next -&gt;</button>
    </form>
  );
}

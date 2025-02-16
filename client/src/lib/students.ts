import David from "@/../public/David.png";
import Emily from "@/../public/Emily.png";
import Jason from "@/../public/Jason.png";
import Sarah from "@/../public/sarah.png";
import { ClassroomTemplate, StudentTemplate } from "./types";

export const MAX_STUDENTS = 5;
export const allStudents: StudentTemplate[] = [
  {
    name: "Emily Carter",
    description:
      "Emily is always enthusiastic and eager to learn new things. Her energy is infectious, and she brings a positive vibe to any group project.",
    personality: "excitable",
    image: Emily,
  },
  {
    name: "Jason Maxwell",
    description:
      "Jason is a highly competitive and driven individual. He's not afraid to voice his opinions, even if they're unpopular, and he can sometimes come across as abrasive.",
    personality: "asshole",
    image: Jason,
  },
  {
    name: "David Lee",
    description:
      "David prefers routine and avoids taking risks. He's a reliable student who consistently completes his assignments, but he rarely contributes anything innovative or exciting.",
    personality: "boring",
    image: David,
  },
  {
    name: "Sarah Chen",
    description:
      "Sarah is a balanced and well-rounded student. She's friendly and approachable, participates in class discussions, and works well with others. She's a good all-around team player.",
    personality: "normal",
    image: Sarah,
  },
];
export const classrooms: ClassroomTemplate[] = [
  {
    name: "An Ordinary Classroom",
    students: ["boring", "normal", "normal", "excitable"],
  },
  {
    name: "You Would Want to Avoid This",
    students: ["asshole", "asshole", "asshole"],
  },
];

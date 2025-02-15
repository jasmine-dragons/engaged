"use server";

import { createPracticeSession } from "@/lib/api";
import { redirect } from "next/navigation";

export async function startSession(personalities: string[]) {
  // await new Promise((resolve) => setTimeout(resolve, 1000));
  await createPracticeSession({
    number_of_students: personalities.length,
    student_avatar_types: personalities,
  });
  redirect(
    "/start?" + new URLSearchParams({ personalities: personalities.join(",") })
  );
}

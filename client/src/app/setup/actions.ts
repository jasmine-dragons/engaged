"use server";

import { startSim } from "@/lib/api";
import { redirect } from "next/navigation";

export async function startSession(personalities: string[]) {
  await startSim({ studentPersonalities: personalities });
  redirect("/start");
}

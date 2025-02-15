const backendBaseUrl = process.env.BACKEND_URL;

export type PracticeSessionConfig = {
  number_of_students: number;
  student_avatar_types: string[];
  /** Defaults to 60 */
  session_duration_minutes?: number;
};

export type MeetingResponse = {
  join_url: string;
  meeting_id: string;
  password: string;
  host_key: string;
  config: PracticeSessionConfig;
};

export function createPracticeSession(
  config: PracticeSessionConfig
): Promise<MeetingResponse> {
  return fetch(`${backendBaseUrl}/create-practice-session`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(config),
  }).then((r) => r.json());
}

export function healthCheck(): Promise<{ status: "healthy" }> {
  return fetch(`${backendBaseUrl}/health`).then((r) => r.json());
}

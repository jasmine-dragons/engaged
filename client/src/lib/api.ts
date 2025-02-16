"use server";

const backendBaseUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

export type SimulationRequest = {
  studentPersonalities: string[];
};

export type SimulationResponse = {
  message: string;
};

export async function startSim(
  config: SimulationRequest
): Promise<SimulationResponse> {
  return fetch(`${backendBaseUrl}/start-sim`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(config),
  }).then((r) => r.json());
}

/** As defined in student_bots.py */
export type Personality = {
  name: string;
  traits: string;
  behavior: string;
  interaction_frequency: number;
  response_style: string;
  cooldown: number;
  voice_id: string;
};

export type HistoricEntry = {
  analytics: Analytics;
  config: Personality[];
  personalities?: string[];
  /** Do NOT use since it gets rounded in JS; use `simulation_id_str` instead */
  simulation_id: number;
  simulation_id_str: string;
  transcript: {
    /** `teacher` for teacher */
    speaker: string;
    text: string;
    timestamp: string;
  }[];
  user_id: number;
  timestamp: string;
};

export type Analytics =
  | { error: string }
  | {
      emotions: string;
      speech_rate_wpm: number;
      filler_words_count: Record<string, number>;
      suggestions: string;
      summary?: string;
    };

export async function getHistory(
  userId: string
): Promise<{ data: HistoricEntry[] }> {
  return fetch(`${backendBaseUrl}/history/${userId}?_=${Date.now()}`).then(
    (r) => r.json()
  );
}

export async function getSimulation(
  simulationId: string
): Promise<{ data: HistoricEntry | false }> {
  return fetch(`${backendBaseUrl}/sim/${simulationId}`).then((r) => r.json());
}

export async function getAnalytics(): Promise<{
  simId: string;
  analytics: Analytics;
}> {
  return fetch(`${backendBaseUrl}/analytics`, { method: "POST" }).then((r) =>
    r.json()
  );
}

export type WebSocketJsonMessage =
  | {
      type: "students";
      students: [
        name: string,
        personalityType: string,
        personality: Personality
      ][];
    }
  | { type: "about-to-speak"; studentName: string };

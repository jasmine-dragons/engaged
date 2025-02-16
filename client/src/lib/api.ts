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

export type HistoricEntry = {
  analytics: Record<string, number>;
  audio: string;
  config: string[];
  transcript: {
    speaker: string;
    text: string;
    timestamp: string;
  };
  user_id: number;
};

export async function getHistory(
  userId: number
): Promise<{ data: HistoricEntry }> {
  return fetch(`${backendBaseUrl}/history/${userId}?_=${Date.now()}`).then(
    (r) => r.json()
  );
}

export async function getAnalytics(): Promise<unknown> {
  return fetch(`${backendBaseUrl}/analytics?_=${Date.now()}`).then((r) =>
    r.json()
  );
}

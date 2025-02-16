export const backendBaseUrl = process.env.BACKEND_URL;

export type SimulationRequest = {
  studentPersonalities: string[];
};

export type SimulationResponse = {};

export function startSim(
  config: SimulationRequest
): Promise<SimulationResponse> {
  return fetch(`${backendBaseUrl}/start-sim`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(config),
  }).then((r) => r.json());
}

import type { components } from "./schema";

export type ModelInfo = components["schemas"]["ModelInfo"];
export type Prediction = components["schemas"]["Prediction"];

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:7860";

export async function listModels(): Promise<ModelInfo[]> {
  const res = await fetch(`${API_URL}/models`);
  if (!res.ok) throw new Error(`GET /models failed: ${res.status}`);
  return res.json();
}

export async function predict(photo: File, arch: string, backbone: string, init: string): Promise<Prediction> {
  const form = new FormData();
  form.append("file", photo);
  form.append("arch", arch);
  form.append("backbone", backbone);
  form.append("init", init);

  const res = await fetch(`${API_URL}/predict`, { method: "POST", body: form });
  if (!res.ok) throw new Error((await res.json()).detail ?? `POST /predict failed: ${res.status}`);
  return res.json();
}

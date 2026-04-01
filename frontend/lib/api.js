import { readFile } from "node:fs/promises";
import path from "node:path";

async function readStaticJson(name) {
  const filePath = path.join(process.cwd(), "public", "data", name);
  const content = await readFile(filePath, "utf-8");
  return JSON.parse(content);
}

export async function getDashboardData() {
  const payload = await readStaticJson("dashboard.json");
  return payload.data;
}

export async function getNewsData() {
  const payload = await readStaticJson("news.json");
  return payload.data;
}

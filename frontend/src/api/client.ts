import axios from "axios";
import type { APIError } from "../types/api";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "",
  headers: { "Content-Type": "application/json" },
  timeout: 10000,
});

export function getApiErrorMessage(error: unknown): string {
  if (axios.isAxiosError<APIError>(error)) {
    const responseMessage =
      error.response?.data?.error?.message ?? error.response?.data?.detail;
    if (responseMessage) return responseMessage;
    if (error.code === "ECONNABORTED") {
      return "The API request timed out. Check that the backend is available.";
    }
    if (!error.response) {
      return "Unable to reach the backend. Check the API connection and try again.";
    }
    return `The backend returned an unexpected response (${error.response.status}).`;
  }
  return "Something went wrong while communicating with the backend.";
}

export default apiClient;

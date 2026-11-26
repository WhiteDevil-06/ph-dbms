import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": "http://localhost:8000",
      "/health": "http://localhost:8000",
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("/node_modules/recharts/")) {
            return "recharts";
          }
          if (id.includes("/node_modules/victory-vendor/")) {
            return "chart-vendor";
          }
          if (/\/node_modules\/d3-[^/]+\//.test(id)) {
            return "d3";
          }
        },
      },
    },
  },
});

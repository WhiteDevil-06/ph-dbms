/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        navy: "#101d2d",
        teal: "#0f8b83",
        canvas: "#f4f7f8",
      },
    },
  },
  plugins: [],
};

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}",
    "./lib/**/*.{js,jsx}"
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(210 20% 88%)",
        input: "hsl(210 20% 88%)",
        ring: "hsl(205 90% 40%)",
        background: "hsl(47 57% 97%)",
        foreground: "hsl(215 35% 15%)",
        primary: {
          DEFAULT: "hsl(204 84% 34%)",
          foreground: "hsl(0 0% 100%)"
        },
        secondary: {
          DEFAULT: "hsl(40 70% 92%)",
          foreground: "hsl(215 35% 15%)"
        },
        muted: {
          DEFAULT: "hsl(48 42% 93%)",
          foreground: "hsl(210 16% 38%)"
        },
        accent: {
          DEFAULT: "hsl(18 90% 58%)",
          foreground: "hsl(0 0% 100%)"
        },
        card: {
          DEFAULT: "hsla(0 0% 100% / 0.8)",
          foreground: "hsl(215 35% 15%)"
        }
      },
      fontFamily: {
        sans: ["var(--font-sans)", "PingFang SC", "Microsoft YaHei", "sans-serif"]
      },
      boxShadow: {
        soft: "0 20px 60px rgba(15, 23, 42, 0.08)"
      },
      borderRadius: {
        xl: "1.2rem",
        "2xl": "1.6rem"
      }
    }
  },
  plugins: []
};

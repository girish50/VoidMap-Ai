/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          bg: "#090D16",      // Ultra-deep slate blue
          card: "#121826",    // Lighter card panel
          border: "#1F293D",  // Premium metallic border
          text: "#E2E8F0",    // Soft white
          muted: "#8892B0"    // Muted tech blue
        },
        brand: {
          glow: "#3B82F6",    // Electric blue
          success: "#10B981", // Emerald
          danger: "#F43F5E",  // Ruby
          warning: "#F59E0B", // Amber
          purple: "#8B5CF6"   // Violet
        }
      },
      fontFamily: {
        sans: ["Outfit", "Inter", "system-ui", "sans-serif"],
      },
      boxShadow: {
        glow: "0 0 15px rgba(59, 130, 246, 0.15)",
        cardGlow: "0 4px 20px rgba(0, 0, 0, 0.25)"
      }
    },
  },
  plugins: [],
}

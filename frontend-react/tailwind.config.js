/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Custom color scheme - Dark minimal
        brand: {
          light: '#C6E0FF',     // Light blue
          gold: '#BCAB79',      // Golden/tan
          teal: '#2978A0',      // Teal blue - primary
          dark: '#315659',      // Dark teal
          darker: '#253031',    // Very dark teal/black
        },
        // Mapped dark theme
        dark: {
          50: '#C6E0FF',
          100: '#a8d0ff',
          200: '#7ab8f5',
          300: '#5a9ed6',
          400: '#4a7a99',
          500: '#3d6577',
          600: '#315659',
          700: '#2c4a4d',
          800: '#253031',
          900: '#1e2627',
          950: '#181e1f',
        },
        accent: {
          primary: '#2978A0',    // Teal blue
          secondary: '#BCAB79',  // Golden
          success: '#6AA87C',    // Muted green
          warning: '#BCAB79',    // Golden
          error: '#B85C5C',      // Muted red
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'gradient': 'gradient 8s linear infinite',
      },
      keyframes: {
        gradient: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        }
      },
      boxShadow: {
        'glow': '0 0 20px rgba(41, 120, 160, 0.3)',
        'glow-lg': '0 0 40px rgba(41, 120, 160, 0.4)',
      }
    },
  },
  plugins: [],
}

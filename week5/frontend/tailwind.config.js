/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Match existing design tokens from styles.css
      colors: {
        background: '#fafafa',
        surface: '#ffffff',
        border: '#eeeeee',
      },
      fontFamily: {
        sans: [
          'system-ui',
          '-apple-system',
          'Segoe UI',
          'Roboto',
          'Helvetica',
          'Arial',
          'sans-serif',
        ],
      },
      borderRadius: {
        'sm': '4px',
        'md': '8px',
        'lg': '12px',
      },
    },
  },
  plugins: [],
  // Purge unused CSS in production
  corePlugins: {
    preflight: true, // Enable CSS reset
  },
}

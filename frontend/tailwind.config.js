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
        ibm: {
          blue: '#0f62fe',
          dark: '#161616',
          light: '#f4f4f4',
          gray: '#262626',
          border: '#393939'
        }
      }
    },
  },
  plugins: [],
}

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'alexandria': ['Alexandria', 'sans-serif'],
      },
      colors: {
        'figma-bg': '#181818',
        'figma-text': '#FAFAFA',
        'figma-gray': '#3D3D3D',
        'figma-gray-light': '#4A4A4A',
        'figma-gray-dark': '#2D2D2D',
        'figma-placeholder': '#999999',
      }
    },
  },
  plugins: [],
}

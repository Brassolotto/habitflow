/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./habits/templates/**/*.html",
    "./users/templates/**/*.html",
    "./static/js/**/*.js"
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        purple: {
          500: '#8B5CF6',
          600: '#7C3AED',
          700: '#6D28D9',
          800: '#5B21B6',
        },
        pink: {
          500: '#EC4899',
          600: '#DB2777',
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

import type { Config } from 'tailwindcss'

export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],

  theme: {
    extend: {
      colors: {
        text: {
          DEFAULT: '#ededed',
          50: '#f2f2f2',
          100: '#e6e6e6',
          200: '#cccccc',
          300: '#b3b3b3',
          400: '#999999',
          500: '#808080',
          600: '#666666',
          700: '#4d4d4d',
          800: '#333333',
          900: '#1a1a1a',
          950: '#0d0d0d'
        },
        background: {
          DEFAULT: '#04080b',
          50: '#ecf3f8',
          100: '#dae7f1',
          200: '#b4cfe4',
          300: '#8fb7d6',
          400: '#699fc9',
          500: '#4487bb',
          600: '#366c96',
          700: '#295170',
          800: '#1b364b',
          900: '#0e1b25',
          950: '#070e13'
        },
        primary: {
          DEFAULT: '#9edf6f',
          50: '#f1faea',
          100: '#e3f6d5',
          200: '#c7edab',
          300: '#aae382',
          400: '#8eda58',
          500: '#72d12e',
          600: '#5ba725',
          700: '#447d1c',
          800: '#2e5412',
          900: '#172a09',
          950: '#0b1505'
        },
        secondary: {
          DEFAULT: '#05ad63',
          50: '#e6fef4',
          100: '#cefde9',
          200: '#9cfcd2',
          300: '#6bfabc',
          400: '#39f9a6',
          500: '#08f78f',
          600: '#06c673',
          700: '#059456',
          800: '#036339',
          900: '#02311d',
          950: '#01190e'
        },
        accent: {
          DEFAULT: '#2b95f9',
          50: '#e6f3fe',
          100: '#cee6fd',
          200: '#9ccefc',
          300: '#6bb5fa',
          400: '#399cf9',
          500: '#0883f7',
          600: '#0669c6',
          700: '#054f94',
          800: '#033563',
          900: '#021a31',
          950: '#010d19'
        }
      },
      fontSize: {
        sm: '0.800rem',
        base: '1rem',
        xl: '1.250rem',
        '2xl': '1.563rem',
        '3xl': '1.954rem',
        '4xl': '2.442rem',
        '5xl': '3.053rem'
      },
      fontFamily: {
        heading: 'Jost',
        body: 'Kanit'
      },
      fontWeight: {
        normal: '400',
        bold: '700'
      }
    }
  },

  plugins: []
} satisfies Config

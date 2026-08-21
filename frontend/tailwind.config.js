/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
      extend: {
          "colors": {
              "on-primary-fixed-variant": "#2e4867",
              "error": "#ba1a1a",
              "on-primary": "#ffffff",
              "on-secondary-fixed": "#001e2f",
              "on-secondary-fixed-variant": "#204b65",
              "on-secondary": "#ffffff",
              "outline": "#74777e",
              "secondary": "#3a637e",
              "primary-fixed-dim": "#aec9ed",
              "tertiary-fixed-dim": "#93d0e0",
              "surface-bright": "#f7f9ff",
              "surface-tint": "#466080",
              "tertiary-container": "#003640",
              "surface-container-highest": "#d9e3f1",
              "on-primary-container": "#809abd",
              "on-tertiary-fixed-variant": "#004e5c",
              "surface-container": "#e4effd",
              "on-error": "#ffffff",
              "surface-dim": "#d1dbe8",
              "inverse-on-surface": "#e8f2ff",
              "surface-container-low": "#edf4ff",
              "on-tertiary-container": "#65a1b1",
              "primary-container": "#16324f",
              "primary": "#001d37",
              "tertiary": "#001f26",
              "inverse-surface": "#27313c",
              "surface-container-lowest": "#ffffff",
              "on-primary-fixed": "#001d37",
              "tertiary-fixed": "#afecfd",
              "on-background": "#121d26",
              "inverse-primary": "#aec9ed",
              "on-surface": "#121d26",
              "surface-container-high": "#dfe9f7",
              "outline-variant": "#c3c6ce",
              "on-surface-variant": "#43474d",
              "error-container": "#ffdad6",
              "on-secondary-container": "#3b637f",
              "on-tertiary": "#ffffff",
              "secondary-container": "#b6dfff",
              "background": "#f7f9ff",
              "surface-variant": "#d9e3f1",
              "on-error-container": "#93000a",
              "surface": "#f7f9ff",
              "on-tertiary-fixed": "#001f26",
              "secondary-fixed-dim": "#a3cbeb",
              "secondary-fixed": "#c8e6ff",
              "primary-fixed": "#d2e4ff",
              // Risk Palette overrides
              "risk": {
                  "low": "#3a637e",      // secondary
                  "moderate": "#466080", // surface-tint
                  "high": "#b6dfff",     // secondary-container
                  "veryHigh": "#ba1a1a"  // error
              }
          },
          "borderRadius": {
              "DEFAULT": "0.5rem",
              "sm": "0.25rem",
              "md": "0.75rem",
              "lg": "1rem",
              "xl": "1.5rem",
              "full": "9999px"
          },
          "spacing": {
              "stack-sm": "8px",
              "container-padding": "24px",
              "unit": "4px",
              "gutter": "16px",
              "stack-md": "16px",
              "stack-lg": "32px"
          },
          "fontFamily": {
              "body-md": ["Inter", "sans-serif"],
              "data-mono": ["Inter", "monospace"],
              "label-sm": ["Inter", "sans-serif"],
              "label-md": ["Inter", "sans-serif"],
              "headline-md": ["Inter", "sans-serif"],
              "body-lg": ["Inter", "sans-serif"],
              "headline-sm": ["Inter", "sans-serif"],
              "display-lg": ["Inter", "sans-serif"]
          },
          "fontSize": {
              "body-md": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
              "data-mono": ["13px", {"lineHeight": "18px", "fontWeight": "500"}],
              "label-sm": ["11px", {"lineHeight": "14px", "fontWeight": "600"}],
              "label-md": ["12px", {"lineHeight": "16px", "letterSpacing": "0.02em", "fontWeight": "500"}],
              "headline-md": ["24px", {"lineHeight": "32px", "letterSpacing": "-0.01em", "fontWeight": "600"}],
              "body-lg": ["16px", {"lineHeight": "24px", "fontWeight": "400"}],
              "headline-sm": ["20px", {"lineHeight": "28px", "fontWeight": "600"}],
              "display-lg": ["32px", {"lineHeight": "40px", "letterSpacing": "-0.02em", "fontWeight": "600"}]
          }
      }
  },
  plugins: [],
}

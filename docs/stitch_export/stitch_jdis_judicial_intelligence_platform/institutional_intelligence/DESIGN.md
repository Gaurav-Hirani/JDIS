---
name: Institutional Intelligence
colors:
  surface: '#f7f9ff'
  surface-dim: '#d1dbe8'
  surface-bright: '#f7f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#edf4ff'
  surface-container: '#e4effd'
  surface-container-high: '#dfe9f7'
  surface-container-highest: '#d9e3f1'
  on-surface: '#121d26'
  on-surface-variant: '#43474d'
  inverse-surface: '#27313c'
  inverse-on-surface: '#e8f2ff'
  outline: '#74777e'
  outline-variant: '#c3c6ce'
  surface-tint: '#466080'
  primary: '#001d37'
  on-primary: '#ffffff'
  primary-container: '#16324f'
  on-primary-container: '#809abd'
  inverse-primary: '#aec9ed'
  secondary: '#3a637e'
  on-secondary: '#ffffff'
  secondary-container: '#b6dfff'
  on-secondary-container: '#3b637f'
  tertiary: '#001f26'
  on-tertiary: '#ffffff'
  tertiary-container: '#003640'
  on-tertiary-container: '#65a1b1'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d2e4ff'
  primary-fixed-dim: '#aec9ed'
  on-primary-fixed: '#001d37'
  on-primary-fixed-variant: '#2e4867'
  secondary-fixed: '#c8e6ff'
  secondary-fixed-dim: '#a3cbeb'
  on-secondary-fixed: '#001e2f'
  on-secondary-fixed-variant: '#204b65'
  tertiary-fixed: '#afecfd'
  tertiary-fixed-dim: '#93d0e0'
  on-tertiary-fixed: '#001f26'
  on-tertiary-fixed-variant: '#004e5c'
  background: '#f7f9ff'
  on-background: '#121d26'
  surface-variant: '#d9e3f1'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
  data-mono:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  container-padding: 24px
  gutter: 16px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style
The design system is engineered for high-stakes judicial decision-making. It adopts a **Modern Corporate** aesthetic with a focus on **Institutional Trust** and **Data-Driven Transparency**. The brand personality is authoritative yet accessible, replacing the archaic complexity of legal systems with clarity and precision. 

The visual language follows a strict "Information First" philosophy, drawing inspiration from high-density enterprise platforms. It utilizes a refined palette and structural rigor to convey stability, ensuring that critical case data is the focal point. The emotional response is one of calm control and professional confidence.

## Colors
The color strategy prioritizes legibility and semantic clarity. The background uses a warm off-white to reduce eye strain during prolonged research sessions. 

- **Primary & Secondary**: Deep navies and steels represent the formal nature of the judiciary.
- **Text Hierarchy**: Charcoal is used for primary content to ensure maximum contrast, while slate gray handles metadata and supporting labels.
- **Risk Palette**: A specialized semantic scale is used for case delay indicators. These are muted to maintain a professional tone, avoiding the "alarmist" nature of pure neon traffic lights, while remaining distinct enough for rapid scanning.

## Typography
This design system utilizes **Inter** exclusively to leverage its exceptional legibility in data-heavy environments. 

- **Numerical Data**: Use tabular figures (`tnum`) for all case numbers and dates to ensure vertical alignment in tables.
- **Hierarchy**: Strong weight contrast (600 for headers vs 400 for body) guides the eye through dense case files.
- **Metadata**: Small, uppercase labels with slight tracking (letter spacing) are used for technical attributes to distinguish them from narrative text.
- **Mobile Scaling**: Headlines above 24px should scale down by a factor of 0.85 on mobile devices to maintain readability without excessive wrapping.

## Layout & Spacing
The layout follows a **Fixed Grid** system for analytical dashboards to ensure data visualization components maintain their aspect ratios. 

- **Grid**: A 12-column grid is used for desktop (1440px max-width).
- **Density**: High-density spacing (4px increments) allows for more information above the fold. 
- **Breakpoints**: 
    - Mobile (<768px): Single column, 16px margins.
    - Tablet (768px - 1024px): 6 columns, 20px margins.
    - Desktop (>1024px): 12 columns, 24px margins.
- **Reflow**: Complex data tables should transition to "Card View" on mobile devices, or utilize horizontal scrolling with a frozen first column (Case ID).

## Elevation & Depth
Depth is signaled through **Tonal Layers** and **Subtle Outlines** rather than heavy shadows. 

- **Surface Levels**: The page background is the lowest level. Content containers use a pure white (#FFFFFF) background with a 1px solid border (#D9DEE5).
- **Shadows**: Only two levels of shadows are permitted:
    - *Low*: 0px 1px 2px rgba(0, 0, 0, 0.05) (Used for standard cards).
    - *Medium*: 0px 4px 12px rgba(0, 0, 0, 0.08) (Used for active dropdowns or modals).
- **Interactive States**: Hovering over an element should result in a slight border-color darken (#B0B8C1) rather than an increase in elevation.

## Shapes
The shape language is professional and structured. 

- **Standard Radius**: 8px (0.5rem) for most containers, input fields, and buttons.
- **Large Radius**: 16px (1rem) for major dashboard sections or modal containers.
- **Small Radius**: 4px (0.25rem) for small tags or checkboxes.
Avoid full "pill" shapes for buttons to maintain the institutional feel; keep them rectangular with the standard 8px radius.

## Components
- **Buttons**: Primary buttons use the Deep Navy background with white text. Ghost buttons use a 1px border (#D9DEE5) and Charcoal text. Use 12px/20px (vertical/horizontal) padding.
- **Data Tables**: Zero outer padding on table cells; use 12px internal padding. Rows should have a subtle hover state (#F0F2F5). Header cells use `label-sm` with a bottom border.
- **Risk Badges**: Small, high-contrast labels using the Risk Palette. Text should be white on the colored background for High/Critical, and dark charcoal on lighter tints for Low/Moderate.
- **Input Fields**: 1px solid border (#D9DEE5) that turns Steel Blue (#315A75) on focus. Labels sit 4px above the field using `label-md`.
- **Case Cards**: Use a white background, 1px border, and a 4px left-edge accent strip colored by the Risk Palette to indicate case urgency at a glance.
- **Progress Indicators**: Linear, 4px height bars for caseload processing, utilizing the Primary color for neutral progress and Risk Palette for delay-specific metrics.
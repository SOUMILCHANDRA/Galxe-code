---
name: Civic Voice Resonance
colors:
  surface: '#f8f9ff'
  surface-dim: '#d0dbed'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e6eeff'
  surface-container-high: '#dee9fc'
  surface-container-highest: '#d9e3f6'
  on-surface: '#121c2a'
  on-surface-variant: '#3f4946'
  inverse-surface: '#27313f'
  inverse-on-surface: '#eaf1ff'
  outline: '#6f7976'
  outline-variant: '#bec9c5'
  surface-tint: '#21695f'
  primary: '#00433b'
  on-primary: '#ffffff'
  primary-container: '#0d5c52'
  on-primary-container: '#8ed2c5'
  inverse-primary: '#8fd3c6'
  secondary: '#006b5f'
  on-secondary: '#ffffff'
  secondary-container: '#6df5e1'
  on-secondary-container: '#006f64'
  tertiary: '#5c2f00'
  on-tertiary: '#ffffff'
  tertiary-container: '#7e4200'
  on-tertiary-container: '#ffb579'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#abf0e2'
  primary-fixed-dim: '#8fd3c6'
  on-primary-fixed: '#00201c'
  on-primary-fixed-variant: '#005047'
  secondary-fixed: '#71f8e4'
  secondary-fixed-dim: '#4fdbc8'
  on-secondary-fixed: '#00201c'
  on-secondary-fixed-variant: '#005048'
  tertiary-fixed: '#ffdcc3'
  tertiary-fixed-dim: '#ffb77d'
  on-tertiary-fixed: '#2f1500'
  on-tertiary-fixed-variant: '#6e3900'
  background: '#f8f9ff'
  on-background: '#121c2a'
  surface-variant: '#d9e3f6'
typography:
  headline-xl:
    fontFamily: Outfit
    fontSize: 40px
    fontWeight: '600'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Outfit
    fontSize: 30px
    fontWeight: '600'
    lineHeight: 38px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.015em
  headline-lg-mobile:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: 0em
  headline-md:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '500'
    lineHeight: 32px
  headline-sm:
    fontFamily: Outfit
    fontSize: 20px
    fontWeight: '500'
    lineHeight: 28px
  body-xl:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
  label-lg:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  space-xxs: 0.25rem
  space-xs: 0.5rem
  space-sm: 0.75rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
  space-2xl: 3rem
  space-3xl: 4rem
  gutter-mobile: 1rem
  gutter-tablet: 1.5rem
  gutter-desktop: 2rem
  margin-mobile: 1rem
  margin-tablet: 2rem
  margin-desktop: auto
---

## Brand & Style

This design system expresses a civic-first, humanely intelligent philosophy tailored for diverse citizens seeking welfare support. The tone balances authoritative institutional dependability with deep empathetic warmth. It bridges the divide between complex governmental frameworks and rural, semi-urban, or non-technical individuals through effortless, dignified voice interaction.

### Aesthetic Foundation
- **Tactile Soft-Modernism:** Generous, organic corner geometry (`rounded-3xl` containers), calm breathing room, and soft physical cues that resemble clean, tactile stationery rather than cold administrative portals.
- **Ambient Calm & Dignity:** A warm, neutral-grounded visual field designed to reduce anxiety during critical welfare discovery, eliminating bureaucratic visual clutter.
- **Voice-First Primacy:** Interfaces center on dynamic auditory states—listening, processing, speaking, and confirming—represented through rhythmic ambient glow ripples, high optical clarity, and low cognitive density.

## Colors

The palette establishes reassurance and legitimacy while welcoming users of all visual abilities. It intentionally avoids clinical blues and stark paper whites in favor of organic mineral and paper tones.

### Functional Palette Structure
- **Primary Deep Teal (`#0D5C52`):** Communicates institutional integrity, civic security, and grounded reliability. Serves as the primary anchor for core actions, structural branding, and dominant interactive states.
- **Secondary Sage/Teal (`#14B8A6`):** Drives interactive feedback, micro-interactions, voice waveform ripples, and highlight focuses.
- **Tertiary Warm Gold (`#D97706`):** Denotes official scheme accreditations, central/state sponsorship tags, notifications, and attention flags without inducing alarm. Paired with soft sunburst backing (`#F59E0B` tint).
- **Match Success Emerald (`#10B981`):** Applied exclusively to confirmed eligibility indicators, verified qualifications, and successful enrollment milestones.
- **Neutral Dark Slate (`#1F2937`):** High-legibility text tone that mitigates the ocular fatigue caused by pure black `#000000`.
- **Surfaces & Backgrounds:** Off-white natural base canvas (`#FBFBF9`) combined with secondary surface tiles (`#F4F3EE`) to provide gentle, non-glare separation.

## Typography

The typographic hierarchy addresses varying levels of literacy and language fluency. 

- **Display & Titles (Outfit):** Features generous open counters, rhythmic circular geometries, and approachable proportions that eliminate the coldness of bureaucratic portals.
- **Reading & Functional Copy (Inter):** Neutral, x-height optimized, and robust at diverse screen densities. Crucial for clear translations, multi-lingual renderings, and dynamic text scaling.
- **Formatting Principles:** Line lengths should not exceed 65 characters. Spacing between paragraphs and cards is increased by 15% relative to standard web software to allow voice prompts to sync comfortably with visual reading.

## Layout & Spacing

Layouts prioritize singular focus, low cognitive load, and tap targets suitable for one-handed thumb navigation.

### Breakpoints and Layout Grid
- **Mobile (Base to 639px):** Single-column stack with persistent floating voice action orb. Container margins: `1rem`, card internal padding: `1.5rem`.
- **Tablet (640px to 1023px):** 6-column fluid grid, 24px gutters. Dual-pane view during voice playback (voice console + scheme results).
- **Desktop (1024px+):** Max width container capped at `840px` for conversational discovery views or `1140px` for comparative scheme tables. Centered layout ensures focused linear reading.

### Spatial Rhythm
Vertical rhythm relies on generous `space-lg` (`1.5rem`) and `space-xl` (`2rem`) separation to decouple cards and preserve breathing room. Dense groupings of data are deliberately avoided.

## Elevation & Depth

Visual hierarchy is communicated via layered tactile warmth rather than harsh elevation drops.

### Surface Tiers
- **Canvas Base:** `#FBFBF9` provides the global ambient backdrop.
- **Card Tier (Level 1):** Solid `#FFFFFF` elevated over `#FBFBF9`, bounded by a hairline border (`1px solid rgba(31, 41, 55, 0.07)`), augmented by a warm ambient shadow: `0 4px 20px -2px rgba(13, 92, 82, 0.05)`.
- **Floating Controls (Level 2 - Voice Console):** Pill-shaped floating dock utilizing `rgba(255, 255, 255, 0.92)` with `16px` backdrop-filter blur, enclosed in a soft emerald border: `1px solid rgba(20, 184, 166, 0.25)`. Shadow: `0 12px 32px -4px rgba(13, 92, 82, 0.12)`.
- **Active Voice Pulse:** Multi-stage radiating rings with non-shadow diffused glows (`box-shadow: 0 0 0 12px rgba(20, 184, 166, 0.15), 0 0 0 24px rgba(20, 184, 166, 0.08)`).

## Shapes

The design system incorporates friendly, welcoming curvature with full `rounded-3xl` radii on major structural modules.

### Curvature Standard
- **Primary Content Cards & Dialog Sheets:** `1.5rem` to `2rem` border radius (`rounded-3xl`), eliminating harsh visual edges.
- **Buttons, Badges, & Voice Orbs:** Completely circular or pill-shaped (`rounded-full`), reinforcing physical touch-points.
- **Input Fields:** Generously rounded at `1rem` to `1.25rem` (`rounded-2xl`) for a soft, welcoming feel.

## Components

### Buttons & Voice Triggers
- **Voice Action Button (Hero Orb):** A `72px` circle with a `#0D5C52` background, featuring an active icon and gentle teal ripples (`#14B8A6`). Smooth scaling animations indicate listening modes without relying exclusively on color.
- **Primary CTA:** Solid `#0D5C52` background, pure `#FFFFFF` label, full pill radius, minimum touch target height of `56px`.
- **Secondary CTA:** Cream fill `#F4F3EE`, slate text `#1F2937`, border `1px solid rgba(31, 41, 55, 0.1)`.

### Scheme Discovery Cards
- Contained within `rounded-3xl` structures on `#FFFFFF` with `24px` internal padding.
- **Eligibility Banner:** Embedded pill chip featuring soft emerald green (`rgba(16, 185, 129, 0.12)`) and deep green text (`#065F46`), accompanied by a clear checkmark icon.
- **Scheme Sponsor Badge:** Amber accent tag (`rgba(217, 119, 6, 0.1)`) with `#92400E` text denoting jurisdictional level (e.g., "Central Gov", "State Welfare").
- **Voice Summary Trigger:** A compact speaker icon button on each card that reads aloud scheme details in the citizen's chosen dialect.

### Input Fields & Search Bars
- Minimum height of `56px` with `rounded-2xl` geometry, styled with a `#FFFFFF` fill and a `1.5px` border in `#E5E7EB`.
- On focus: shifts border to `#14B8A6` with a soft outer ring `rgba(20, 184, 166, 0.2)`.
- Includes a prominent voice-dictation microphone shortcut embedded on the right side of the input field.

### Selection Chips & Toggles
- Filter chips feature `rounded-full` boundaries with a base height of `40px`.
- Inactive: `#F4F3EE` surface, `#1F2937` typography.
- Active: `#0D5C52` surface, `#FFFFFF` typography, accompanied by gentle spring-motion transition feedback.

### Voice Status Transcript Bubble
- Centered conversational response tile with dynamic waveform visualization. Uses `#F4F3EE` with `rounded-3xl` corners, ensuring spoken responses are clearly displayed in high-contrast text for dual audio-visual comprehension.
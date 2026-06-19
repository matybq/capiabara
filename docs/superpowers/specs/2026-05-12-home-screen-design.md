# CapIAbara Home Screen Design Spec

## Goal
Build the approved CapIAbara home screen as a static, pixel-focused mobile-first view that matches the provided screenshot and reuses the existing capybara asset/component.

## Scope
- Create a new `HomeScreen` screen for the frontend.
- Render a centered mobile frame with a maximum width of 430px and a full-viewport height.
- Reuse the existing `Capybara` component for the mascot.
- Update `App.jsx` to render the home screen.
- Add any Home-specific CSS to `frontend/src/styles.css` without adding dependencies.

## Non-goals
- No routing, auth, data fetching, or backend integration.
- No navigation behavior from the CTA or settings button.
- No modal, drawer, or settings panel.
- No new assets, icon libraries, or component libraries.
- No redesign of the broader design system beyond what the Home screen needs.

## Visual requirements
- The screen is static and screenshot-driven.
- Mobile layout is centered in a 430px-wide container with `100vh` height.
- Desktop shows the same mobile frame centered on a neutral outer background.
- The inner screen uses a warm cream canvas.
- Header:
  - `CAPIABARA` appears as a small eyebrow at the top left.
  - A circular settings button appears at the top right.
- Greeting:
  - `Buen día, matias` is shown prominently.
  - `matias` is italic and uses the chocolate text color.
- Mascot:
  - Reuse `Capybara` as the main visual.
  - It should appear large and centered.
  - The home screen renders it in a static state.
- Badge:
  - Show `1.247 mates juntos 🧉` below the mascot.
- Bottom CTA:
  - A wide chocolate pill button spans the available width.
  - Left side shows a chat icon.
  - Center label is `Agregame una tarea`.
  - Right side shows an arrow.
- Caption:
  - Show `Hablale a Capi por WhatsApp · todo se anota solo` under the CTA.

## Component architecture
- `frontend/src/App.jsx`
  - Acts as the screen entry point and renders `HomeScreen`.
- `frontend/src/screens/HomeScreen.jsx`
  - Owns the layout and composition of the home screen.
  - Imports and renders `Capybara`.
  - Renders the header, greeting, badge, CTA, and caption.
  - Keeps the screen stateless.
- `frontend/src/styles.css`
  - Adds Home screen layout and element-specific classes.
  - Reuses the existing CapIAbara tokens for cream, cacao, radii, and typography.
  - Avoids introducing duplicate styling systems.

## Behavior
- The screen is static only.
- The CTA button and settings button are visual buttons with normal hover/active states only.
- Clicking either button does not navigate, open a modal, or change app state.
- The mascot stays visually fixed; no animated talking or breathing state is required on this screen.
- The layout should remain centered and stable across viewport sizes.

## Implementation notes
- Keep the screen simple and focused on composition.
- Use the existing `Capybara` component with a static configuration for the home screen (`animated={false}`, `talking={false}`, neutral accessory state).
- Prefer the existing color tokens in `styles.css` rather than hardcoded colors.
- Use one screen wrapper that handles the mobile frame, spacing, and desktop centering.
- Keep icon treatment lightweight and local to the screen/CSS.

## Verification
- Later verification commands:
  - `cd frontend && npm run lint`
  - `cd frontend && npm run build`
- The implementation is correct when both commands pass and the rendered screen matches the approved static composition.

# Home Screen Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the static CapIAbara Home screen from the approved screenshot-focused spec.

**Architecture:** Keep `App.jsx` as a thin entry point that renders one stateless `HomeScreen` component. Put the full screenshot-driven composition in `HomeScreen.jsx`, keep the mascot static with the shared `Capybara` asset, and use `styles.css` for layout and element styling with the existing CapIAbara tokens only.

**Tech Stack:** React 19, Vite, JavaScript, CSS tokens in `src/styles.css`.

---

### Task 1: Create the home screen component

**Files:**
- Create: `frontend/src/screens/HomeScreen.jsx`

- [ ] **Step 1: Add the full stateless screen component.**

```jsx
import Capybara from '../components/Capybara'

function SettingsIcon() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" className="home-icon home-icon--settings">
      <path
        d="M12 8.25a3.75 3.75 0 1 0 0 7.5 3.75 3.75 0 0 0 0-7.5Zm8.25 3.75-.99-.57.07-1.14a1.2 1.2 0 0 0-.34-.92l-1.02-1.02a1.2 1.2 0 0 0-.92-.34l-1.14.07-.57-.99a1.2 1.2 0 0 0-.81-.6l-1.45-.36a1.2 1.2 0 0 0-1.07.29l-.88.75-.88-.75a1.2 1.2 0 0 0-1.07-.29l-1.45.36a1.2 1.2 0 0 0-.81.6l-.57.99-1.14-.07a1.2 1.2 0 0 0-.92.34L4.99 9.4a1.2 1.2 0 0 0-.34.92l.07 1.14-.99.57a1.2 1.2 0 0 0-.6.81l-.36 1.45a1.2 1.2 0 0 0 .29 1.07l.75.88-.75.88a1.2 1.2 0 0 0-.29 1.07l.36 1.45a1.2 1.2 0 0 0 .6.81l.99.57-.07 1.14a1.2 1.2 0 0 0 .34.92l1.02 1.02a1.2 1.2 0 0 0 .92.34l1.14-.07.57.99a1.2 1.2 0 0 0 .81.6l1.45.36a1.2 1.2 0 0 0 1.07-.29l.88-.75.88.75a1.2 1.2 0 0 0 1.07.29l1.45-.36a1.2 1.2 0 0 0 .81-.6l.57-.99 1.14.07a1.2 1.2 0 0 0 .92-.34l1.02-1.02a1.2 1.2 0 0 0 .34-.92l-.07-1.14.99-.57a1.2 1.2 0 0 0 .6-.81l.36-1.45a1.2 1.2 0 0 0-.29-1.07l-.75-.88.75-.88a1.2 1.2 0 0 0 .29-1.07l-.36-1.45a1.2 1.2 0 0 0-.6-.81Z"
        fill="currentColor"
      />
    </svg>
  )
}

function ChatIcon() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" className="home-icon">
      <path
        d="M6.5 5.5h11A2.5 2.5 0 0 1 20 8v5.5a2.5 2.5 0 0 1-2.5 2.5H12l-4.5 3v-3H6.5A2.5 2.5 0 0 1 4 13.5V8a2.5 2.5 0 0 1 2.5-2.5Z"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function ArrowIcon() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" className="home-icon">
      <path
        d="M7 12h10M13 6l6 6-6 6"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function HomeScreen() {
  return (
    <main className="home-shell">
      <section className="home-screen" aria-label="CapIAbara home screen">
        <header className="home-header">
          <p className="eyebrow home-eyebrow">CAPIABARA</p>

          <button type="button" className="home-settings" aria-label="Settings">
            <SettingsIcon />
          </button>
        </header>

        <div className="home-copy">
          <h1 className="home-title display">
            Buen día, <span className="home-name display-italic">matias</span>
          </h1>
        </div>

        <div className="home-mascot" aria-hidden="true">
          <Capybara accessory="none" animated={false} talking={false} size={288} />
        </div>

        <p className="home-badge ui">1.247 mates juntos 🧉</p>

        <div className="home-footer">
          <button type="button" className="home-cta btn" aria-label="Agregame una tarea">
            <ChatIcon />
            <span>Agregame una tarea</span>
            <ArrowIcon />
          </button>

          <p className="home-caption ui">Hablale a Capi por WhatsApp · todo se anota solo</p>
        </div>
      </section>
    </main>
  )
}

export default HomeScreen
```

- [ ] **Step 2: Confirm the file stays dependency-free.** Make sure the only import is `Capybara`, the screen uses `animated={false}` and `talking={false}`, and the file ends with `export default HomeScreen`.

### Task 2: Point the app entry at the home screen

**Files:**
- Modify: `frontend/src/App.jsx`

- [ ] **Step 1: Replace the placeholder wrapper with the new screen entry point.**

```jsx
import HomeScreen from './screens/HomeScreen'

function App() {
  return <HomeScreen />
}

export default App
```

- [ ] **Step 2: Verify the entry file stays minimal.** Confirm there is no default React import, no inline layout styling, and no extra wrapper markup.

### Task 3: Add Home-specific layout and visual styles

**Files:**
- Modify: `frontend/src/styles.css`

- [ ] **Step 1: Update the global page centering rules and append the Home screen block.** Replace the current `body` rule with the version below, then append the Home screen selectors near the other layout rules.

```css
body {
  min-height: 100vh;
  background:
    radial-gradient(1200px 600px at 15% -5%, rgba(123, 97, 255, 0.06) 0%, transparent 55%),
    radial-gradient(1000px 800px at 100% 100%, rgba(74, 46, 21, 0.04) 0%, transparent 50%),
    var(--cream-100);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

#root {
  width: 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
}

.home-shell {
  width: min(100%, 430px);
  min-height: 100vh;
  background: var(--cream-100);
  overflow: hidden;
}

.home-screen {
  min-height: 100vh;
  padding: 18px 18px 22px;
  display: flex;
  flex-direction: column;
}

.home-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 22px;
}

.home-eyebrow {
  margin: 0;
}

.home-settings {
  width: 40px;
  height: 40px;
  border: 1px solid var(--cream-300);
  border-radius: 50%;
  background: rgba(254, 251, 246, 0.82);
  color: var(--cacao-700);
  box-shadow: var(--sh-soft);
  display: grid;
  place-items: center;
  cursor: pointer;
}

.home-copy {
  margin-bottom: 10px;
}

.home-title {
  margin: 0;
  font-size: clamp(34px, 8vw, 44px);
  line-height: 0.98;
  letter-spacing: var(--tracking-display);
  color: var(--cacao-900);
}

.home-name {
  color: var(--cacao-600);
}

.home-mascot {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px 0 14px;
}

.home-badge {
  margin: 0 auto 14px;
  padding: 10px 16px;
  border-radius: var(--r-pill);
  border: 1px solid var(--cream-300);
  background: rgba(250, 246, 240, 0.82);
  color: var(--cacao-600);
  text-align: center;
}

.home-footer {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.home-cta {
  width: 100%;
  min-height: 60px;
  padding-inline: 18px;
  justify-content: space-between;
}

.home-cta span {
  flex: 1;
  text-align: center;
}

.home-icon {
  width: 20px;
  height: 20px;
  flex: none;
}

.home-icon--settings {
  width: 18px;
  height: 18px;
}

.home-caption {
  margin: 0;
  text-align: center;
  color: var(--ink-500);
  font-size: 13px;
}

@media (min-width: 431px) {
  .home-shell {
    border-radius: 40px;
    box-shadow: var(--sh-lift);
  }
}
```

- [ ] **Step 2: Check that every selector matches the JSX class names.** Confirm the screen uses the same names for the shell, header, setting button, mascot block, badge, footer, CTA, and caption.

### Task 4: Verify the frontend build after the screen swap

**Files:**
- No code changes; verification only.

- [ ] **Step 1: Run the frontend lint check.**

Run: `cd frontend && npm run lint`

Expected: exit code `0` with no ESLint errors or warnings.

- [ ] **Step 2: Run the production build.**

Run: `cd frontend && npm run build`

Expected: exit code `0` and a successful Vite build that emits the production bundle.

## Self-review

### 1. Spec coverage
- Static screenshot-driven home screen: covered by Tasks 1–3.
- Centered mobile frame with 430px max width and desktop centering: covered by Task 3.
- Warm cream canvas and existing token reuse: covered by Task 3.
- Header eyebrow and circular settings button: covered by Task 1 and Task 3.
- Greeting with italic chocolate `matias`: covered by Task 1 and Task 3.
- Static `Capybara` mascot: covered by Task 1.
- Badge, CTA, and caption text: covered by Task 1 and Task 3.
- `App.jsx` entry point swap: covered by Task 2.
- No routing, auth, fetching, or settings behavior: preserved by Task 1.
- Verification with lint and build: covered by Task 4.

### 2. Placeholder scan
- No `TBD`, `TODO`, or “implement later” placeholders remain in the plan.
- All file paths are explicit.
- All code-edit steps include concrete snippets.

### 3. Consistency check
- `HomeScreen.jsx` import path matches `App.jsx`.
- The `Capybara` prop names match the existing component signature.
- JSX class names match the CSS selectors in Task 3.
- Verification commands match the frontend scripts in `package.json`.

### Open questions
- The spec is screenshot-driven, so exact spacing and icon glyph polish may still need visual tuning during implementation.

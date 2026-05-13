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
          <Capybara accessory="none" animated={false} talking={false} size="min(288px, calc(100vw - 52px))" />
        </div>

        <div className="home-footer">
          <button type="button" className="home-cta btn btn-primary" aria-label="Agregame una tarea">
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

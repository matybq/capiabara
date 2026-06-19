import Capybara from '../components/Capybara'

function HomeScreen() {
  return (
    <main className="home-shell">
      <section className="home-screen" aria-label="CapIAbara home screen">
        <header className="home-header">
          <p className="eyebrow home-eyebrow">CAPIABARA</p>
        </header>

        <div className="home-mascot" aria-hidden="true">
          <Capybara accessory="none" animated={false} talking={false} size="min(288px, calc(100vw - 52px))" />
        </div>
      </section>
    </main>
  )
}

export default HomeScreen

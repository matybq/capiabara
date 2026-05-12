import Capybara from "./components/Capybara";
import "./styles.css";

function App() {
  return (
    <div style={{ padding: 40, background: "#FBF6EE", minHeight: "100vh" }}>
      <Capybara size={200} mood="chill" animated={true} />
    </div>
  );
}

export default App;

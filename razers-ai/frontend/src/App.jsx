
function App() {
  return (
    <main className="app">
      <h1>Razers AI</h1>
      <p>Your personal AI assistant.</p>

      <div className="chat-box">
        <div className="message assistant">
          Halo! Saya Razers AI. Ada yang bisa saya bantu?
        </div>

        <form className="chat-input">
          <input
            type="text"
            placeholder="Ketik pesan kamu..."
            disabled
          />
          <button type="button" disabled>
            Kirim
          </button>
        </form>
      </div>
    </main>
  );
}

export default App;

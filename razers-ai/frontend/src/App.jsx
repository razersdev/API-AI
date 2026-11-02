
import { useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Halo! Saya Razers AI. Ada yang bisa saya bantu?",
    },
  ]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (event) => {
    event.preventDefault();

    const userMessage = message.trim();

    if (!userMessage || loading) return;

    setMessages((prev) => [
      ...prev,
      { role: "user", text: userMessage },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
        }),
      });

      if (!response.ok) {
        throw new Error("Gagal mendapatkan respons dari server.");
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: data.reply },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Maaf, gagal terhubung ke server. Pastikan Backend berjalan.",
        },
      ]);

      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="app">
      <h1>Razers AI</h1>
      <p>Your personal AI assistant.</p>

      <div className="chat-box">
        <div className="messages">
          {messages.map((item, index) => (
            <div
              key={index}
              className={`message ${item.role}`}
            >
              {item.text}
            </div>
          ))}

          {loading && (
            <div className="message assistant">
              Razers AI sedang mengetik...
            </div>
          )}
        </div>

        <form className="chat-input" onSubmit={sendMessage}>
          <input
            type="text"
            placeholder="Ketik pesan kamu..."
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            disabled={loading}
          />

          <button type="submit" disabled={loading || !message.trim()}>
            Kirim
          </button>
        </form>
      </div>
    </main>
  );
}

export default App;

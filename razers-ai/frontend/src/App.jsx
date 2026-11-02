
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
      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: userMessage,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Server response error");
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
          text: "Tidak dapat terhubung ke server. Periksa koneksi Backend.",
        },
      ]);

      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const newChat = () => {
    if (loading) return;

    setMessages([
      {
        role: "assistant",
        text: "Halo! Saya Razers AI. Ada yang bisa saya bantu?",
      },
    ]);
  };

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">R</div>
          <span>RAZERS AI</span>
        </div>

        <button className="new-chat-button" onClick={newChat}>
          <span>+</span>
          Percakapan baru
        </button>

        <div className="sidebar-section">
          <span className="section-label">WORKSPACE</span>

          <div className="sidebar-item active">
            <span>◫</span>
            Percakapan
          </div>
        </div>

        <div className="sidebar-bottom">
          <div className="system-status">
            <span className="status-dot"></span>
            <span>Backend connected</span>
          </div>

          <div className="profile">
            <div className="profile-avatar">R</div>
            <div>
              <strong>Razers User</strong>
              <small>Personal workspace</small>
            </div>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <span>Workspace / Chat</span>
          <span className="version">VERSION 0.1</span>
        </header>

        <section className="chat-area">
          <div className="chat-content">
            {messages.length === 1 ? (
              <div className="welcome">
                <span className="welcome-label">
                  PERSONAL AI ASSISTANT
                </span>

                <h1>
                  A space for
                  <br />
                  <span>your thoughts.</span>
                </h1>

                <p>
                  Ask questions, explore ideas, and get things done
                  with Razers AI.
                </p>
              </div>
            ) : (
              <div className="conversation">
                {messages.map((item, index) => (
                  <div
                    key={index}
                    className={`message-row ${item.role}`}
                  >
                    {item.role === "assistant" && (
                      <div className="message-avatar">R</div>
                    )}

                    <div className="message-text">
                      {item.text}
                    </div>
                  </div>
                ))}

                {loading && (
                  <div className="message-row assistant">
                    <div className="message-avatar">R</div>
                    <div className="message-text loading-text">
                      Thinking...
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          <div className="composer-wrapper">
            <form className="composer" onSubmit={sendMessage}>
              <textarea
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                placeholder="Message Razers AI..."
                rows={1}
                disabled={loading}
                onKeyDown={(event) => {
                  if (
                    event.key === "Enter" &&
                    !event.shiftKey
                  ) {
                    event.preventDefault();
                    event.currentTarget.form.requestSubmit();
                  }
                }}
              />

              <button
                className="send-button"
                type="submit"
                disabled={loading || !message.trim()}
              >
                ↑
              </button>
            </form>

            <p className="composer-note">
              Razers AI can make mistakes. Verify important information.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;

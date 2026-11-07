
import { useState, useEffect } from "react";

const STORAGE_KEY = "razers-ai-conversations";
const API_URL = "http://127.0.0.1:8000";

function createConversation() {
  return {
    id: crypto.randomUUID(),
    title: "Percakapan baru",
    messages: [
      {
        role: "assistant",
        text: "Halo! Saya Razers AI. Ada yang bisa saya bantu?",
      },
    ],
    updatedAt: Date.now(),
  };
}

function loadConversations() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);

    if (saved) {
      const data = JSON.parse(saved);

      if (
        Array.isArray(data.conversations) &&
        data.conversations.length > 0 &&
        data.conversations.every(
          (chat) =>
            typeof chat.id === "string" &&
            Array.isArray(chat.messages)
        )
      ) {
        const activeExists = data.conversations.some(
          (chat) => chat.id === data.activeConversationId
        );

        return {
          conversations: data.conversations,
          activeConversationId: activeExists
            ? data.activeConversationId
            : data.conversations[0].id,
        };
      }
    }
  } catch (error) {
    console.error("Gagal membaca conversation storage:", error);
  }

  const initialChat = createConversation();

  return {
    conversations: [initialChat],
    activeConversationId: initialChat.id,
  };
}

// Request AI response from backend
async function requestAI(message) {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(
      data.detail || `Server error (${response.status})`
    );
  }

  if (!data.reply) {
    throw new Error("Server returned an empty response.");
  }

  return data.reply;
}

function App() {
  const [conversationState, setConversationState] = useState(
    loadConversations
  );

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState("connecting");

  const { conversations, activeConversationId } = conversationState;

  const activeConversation = conversations.find(
    (chat) => chat.id === activeConversationId
  );

  const messages = activeConversation?.messages ?? [];

  // Save conversations automatically
  useEffect(() => {
    try {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(conversationState)
      );
    } catch (error) {
      console.error("Gagal menyimpan percakapan:", error);
    }
  }, [conversationState]);

  // Backend health check
  useEffect(() => {
    let active = true;

    const checkBackend = async () => {
      try {
        const response = await fetch(`${API_URL}/health`);

        if (!response.ok) {
          throw new Error("Backend unavailable");
        }

        if (active) {
          setBackendStatus("connected");
        }
      } catch {
        if (active) {
          setBackendStatus("disconnected");
        }
      }
    };

    checkBackend();

    const interval = setInterval(checkBackend, 5000);

    return () => {
      active = false;
      clearInterval(interval);
    };
  }, []);

  // Create new conversation
  const newChat = () => {
    if (loading) return;

    const newConversation = createConversation();

    setConversationState((prev) => ({
      conversations: [
        newConversation,
        ...prev.conversations,
      ],
      activeConversationId: newConversation.id,
    }));

    setMessage("");
  };

  // Switch conversation
  const selectConversation = (id) => {
    if (loading) return;

    setConversationState((prev) => ({
      ...prev,
      activeConversationId: id,
    }));

    setMessage("");
  };

  // Update conversation
  const updateConversation = (id, updater) => {
    setConversationState((prev) => ({
      ...prev,
      conversations: prev.conversations.map((chat) =>
        chat.id === id
          ? {
              ...chat,
              ...updater(chat),
              updatedAt: Date.now(),
            }
          : chat
      ),
    }));
  };

  // Send message
  const sendMessage = async (event) => {
    event.preventDefault();

    const userMessage = message.trim();

    if (!userMessage || loading || !activeConversation) return;

    const conversationId = activeConversation.id;

    updateConversation(conversationId, (chat) => ({
      title:
        chat.messages.length === 1 &&
        chat.messages[0].role === "assistant"
          ? userMessage.slice(0, 35) +
            (userMessage.length > 35 ? "..." : "")
          : chat.title,

      messages: [
        ...chat.messages,
        { role: "user", text: userMessage },
      ],
    }));

    setMessage("");
    setLoading(true);

    try {
      const reply = await requestAI(userMessage);

      updateConversation(conversationId, (chat) => ({
        messages: [
          ...chat.messages,
          {
            role: "assistant",
            text: reply,
          },
        ],
      }));
    } catch (error) {
      const retryId = crypto.randomUUID();

      updateConversation(conversationId, (chat) => ({
        messages: [
          ...chat.messages,
          {
            role: "assistant",
            text: "Maaf, Razers AI belum bisa memproses pesanmu. Silakan coba lagi.",
            isError: true,
            retryMessage: userMessage,
            retryId,
          },
        ],
      }));

      console.error("Chat Error:", error);
    } finally {
      setLoading(false);
    }
  };

  // Retry failed message
  const retryMessage = async (conversationId, failedMessage) => {
    if (loading || !failedMessage.retryMessage) return;

    setLoading(true);

    try {
      const reply = await requestAI(failedMessage.retryMessage);

      updateConversation(conversationId, (chat) => ({
        messages: chat.messages.map((item) =>
          item.retryId === failedMessage.retryId
            ? {
                role: "assistant",
                text: reply,
              }
            : item
        ),
      }));
    } catch (error) {
      console.error("Retry Error:", error);

      updateConversation(conversationId, (chat) => ({
        messages: chat.messages.map((item) =>
          item.retryId === failedMessage.retryId
            ? {
                ...item,
                text: "Percobaan ulang gagal. Periksa koneksi backend atau layanan AI, lalu coba lagi.",
              }
            : item
        ),
      }));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">R</div>
          <span>RAZERS AI</span>
        </div>

        <button
          className="new-chat-button"
          onClick={newChat}
          disabled={loading}
        >
          <span>+</span>
          Percakapan baru
        </button>

        <div className="sidebar-section">
          <span className="section-label">RECENT CHATS</span>

          <div className="history-list">
            {conversations.map((chat) => (
              <button
                key={chat.id}
                className={`sidebar-item ${
                  chat.id === activeConversationId ? "active" : ""
                }`}
                onClick={() => selectConversation(chat.id)}
                disabled={loading}
                title={chat.title}
              >
                <span>◫</span>
                <span className="history-title">{chat.title}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="sidebar-bottom">
          <div className="system-status">
            <span className={`status-dot ${backendStatus}`}></span>

            <span>
              {backendStatus === "connecting" && "Connecting..."}
              {backendStatus === "connected" && "Connected"}
              {backendStatus === "disconnected" && "Disconnected"}
            </span>
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
                    key={item.retryId || index}
                    className={`message-row ${item.role}`}
                  >
                    {item.role === "assistant" && (
                      <div className="message-avatar">R</div>
                    )}

                    <div className="message-text">
                      <div>{item.text}</div>

                      {item.isError && (
                        <button
                          className="retry-button"
                          onClick={() =>
                            retryMessage(
                              activeConversationId,
                              item
                            )
                          }
                          disabled={loading}
                        >
                          ↻ Coba lagi
                        </button>
                      )}
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


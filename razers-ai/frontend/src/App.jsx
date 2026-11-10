
import { useState, useEffect } from "react";

const STORAGE_KEY = "razers-ai-conversations";
const API_URL = "http://127.0.0.1:8000";

const WELCOME_MESSAGE =
  "Halo! Saya Razers AI. Ada yang bisa saya bantu?";

// ==========================================
// CREATE CONVERSATION
// ==========================================

function createConversation() {
  return {
    id: crypto.randomUUID(),
    title: "Percakapan baru",
    messages: [
      {
        role: "assistant",
        text: WELCOME_MESSAGE,
      },
    ],
    updatedAt: Date.now(),
  };
}

// ==========================================
// LOAD CONVERSATIONS
// ==========================================

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
    console.error(
      "Gagal membaca conversation storage:",
      error
    );
  }

  const initialChat = createConversation();

  return {
    conversations: [initialChat],
    activeConversationId: initialChat.id,
  };
}

// ==========================================
// BUILD CONVERSATION HISTORY
// ==========================================

function buildConversationHistory(messages) {
  return messages
    .filter((item, index) => {
      // Exclude default welcome message
      if (
        index === 0 &&
        item.role === "assistant" &&
        item.text === WELCOME_MESSAGE
      ) {
        return false;
      }

      // Exclude failed assistant messages
      return !item.isError;
    })
    .map((item) => ({
      role: item.role,
      content: item.text,
    }))
    // Reserve one slot for the latest user message
    .slice(-49);
}

// ==========================================
// REQUEST AI
// ==========================================

async function requestAI(messages) {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      messages,
    }),
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

// ==========================================
// MAIN APP
// ==========================================

function App() {
  const [conversationState, setConversationState] = useState(
    loadConversations
  );

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState("connecting");

  const { conversations, activeConversationId } =
    conversationState;

  const activeConversation = conversations.find(
    (chat) => chat.id === activeConversationId
  );

  const messages = activeConversation?.messages ?? [];

  // ==========================================
  // SAVE CONVERSATIONS AUTOMATICALLY
  // ==========================================

  useEffect(() => {
    try {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(conversationState)
      );
    } catch (error) {
      console.error(
        "Gagal menyimpan percakapan:",
        error
      );
    }
  }, [conversationState]);

  // ==========================================
  // BACKEND HEALTH CHECK
  // ==========================================

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

  // ==========================================
  // CREATE NEW CONVERSATION
  // ==========================================

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

  // ==========================================
  // SWITCH CONVERSATION
  // ==========================================

  const selectConversation = (id) => {
    if (loading) return;

    setConversationState((prev) => ({
      ...prev,
      activeConversationId: id,
    }));

    setMessage("");
  };

  // ==========================================
  // UPDATE CONVERSATION
  // ==========================================

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

  // ==========================================
  // SEND MESSAGE WITH CONTEXT
  // ==========================================

  const sendMessage = async (event) => {
    event.preventDefault();

    const userMessage = message.trim();

    if (!userMessage || loading || !activeConversation) {
      return;
    }

    const conversationId = activeConversation.id;

    // Build previous conversation history
    const conversationHistory = buildConversationHistory(
      activeConversation.messages
    );

    // Append latest user message
    conversationHistory.push({
      role: "user",
      content: userMessage,
    });

    // Update conversation title and messages
    updateConversation(conversationId, (chat) => ({
      title:
        chat.messages.length === 1 &&
        chat.messages[0].role === "assistant"
          ? userMessage.slice(0, 35) +
            (userMessage.length > 35 ? "..." : "")
          : chat.title,

      messages: [
        ...chat.messages,
        {
          role: "user",
          text: userMessage,
        },
      ],
    }));

    setMessage("");
    setLoading(true);

    try {
      const reply = await requestAI(conversationHistory);

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

  // ==========================================
  // RETRY WITH CONVERSATION CONTEXT
  // ==========================================

  const retryMessage = async (conversationId, failedMessage) => {
    if (loading || !failedMessage.retryMessage) {
      return;
    }

    const conversation = conversationState.conversations.find(
      (chat) => chat.id === conversationId
    );

    if (!conversation) return;

    const errorIndex = conversation.messages.findIndex(
      (item) => item.retryId === failedMessage.retryId
    );

    if (errorIndex === -1) return;

    // Restore conversation history before failed response
    const conversationHistory = buildConversationHistory(
      conversation.messages.slice(0, errorIndex)
    );

    // Ensure latest message is from user
    if (
      conversationHistory.length === 0 ||
      conversationHistory[conversationHistory.length - 1].role !==
        "user"
    ) {
      return;
    }

    setLoading(true);

    try {
      const reply = await requestAI(conversationHistory);

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

  // ==========================================
  // USER INTERFACE
  // ==========================================

  return (
    <div className="app-layout">

      {/* SIDEBAR */}

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

          <span className="section-label">
            RECENT CHATS
          </span>

          <div className="history-list">

            {conversations.map((chat) => (
              <button
                key={chat.id}
                className={`sidebar-item ${
                  chat.id === activeConversationId
                    ? "active"
                    : ""
                }`}
                onClick={() => selectConversation(chat.id)}
                disabled={loading}
                title={chat.title}
              >
                <span>◫</span>

                <span className="history-title">
                  {chat.title}
                </span>
              </button>
            ))}

          </div>
        </div>

        <div className="sidebar-bottom">

          <div className="system-status">

            <span
              className={`status-dot ${backendStatus}`}
            ></span>

            <span>
              {backendStatus === "connecting" &&
                "Connecting..."}

              {backendStatus === "connected" &&
                "Connected"}

              {backendStatus === "disconnected" &&
                "Disconnected"}
            </span>

          </div>

          <div className="profile">

            <div className="profile-avatar">
              R
            </div>

            <div>
              <strong>Razers User</strong>
              <small>Personal workspace</small>
            </div>

          </div>

        </div>

      </aside>

      {/* MAIN CONTENT */}

      <main className="main-content">

        <header className="topbar">
          <span>Workspace / Chat</span>
          <span className="version">VERSION 0.1</span>
        </header>

        {/* CHAT AREA */}

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
                      <div className="message-avatar">
                        R
                      </div>
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

                {/* LOADING INDICATOR */}

                {loading && (

                  <div className="message-row assistant">

                    <div className="message-avatar">
                      R
                    </div>

                    <div className="message-text loading-text">
                      Thinking...
                    </div>

                  </div>

                )}

              </div>

            )}

          </div>

          {/* MESSAGE COMPOSER */}

          <div className="composer-wrapper">

            <form
              className="composer"
              onSubmit={sendMessage}
            >

              <textarea
                value={message}
                onChange={(event) =>
                  setMessage(event.target.value)
                }
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

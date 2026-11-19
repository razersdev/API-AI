import main
from main import ChatRequest, ChatMessage


# ==========================================
# MOCK OPENAI CLIENT
# ==========================================

class MockResponses:

    def create(self, **kwargs):

        # Validasi AI menerima instructions
        assert "instructions" in kwargs
        assert "PERSISTENT USER MEMORY" in kwargs["instructions"]

        # Validasi conversation history diterima
        assert "input" in kwargs

        print("\n========== PRODUCTION TEST ==========")
        print("Model:", kwargs["model"])
        print("Memory injected: SUCCESS")
        print("Conversation input: SUCCESS")
        print("=================================\n")

        class MockResponse:
            output_text = "Production integration test berhasil."

        return MockResponse()


class MockOpenAI:

    def __init__(self):
        self.responses = MockResponses()


# ==========================================
# OVERRIDE CONFIGURATION
# ==========================================

main.MOCK_MODE = False
main.client = MockOpenAI()


# ==========================================
# TEST REQUEST
# ==========================================

request = ChatRequest(
    conversation_id="cp40-production-test",
    messages=[
        ChatMessage(
            role="user",
            content="Razers AI"
        )
    ]
)


# ==========================================
# EXECUTE CHAT
# ==========================================

response = main.chat(request)


# ==========================================
# VALIDATION
# ==========================================

assert response.reply == "Production integration test berhasil."

print("TEST RESULT: PASS")
print("Response:", response.reply)
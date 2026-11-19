from database.connection import SessionLocal
from database.models import Memory
from services.memory_service import retrieve_memories

db = SessionLocal()

# ==========================================
# CONVERSATION A - SIMPAN MEMORY
# ==========================================

memory = Memory(
    content="CROSS CONVERSATION TEST RAZERS suka Python",
    category="preference",
    source_conversation_id="conversation_A",
    importance=5,
)

db.add(memory)
db.commit()

print("Memory saved from Conversation A.")


# ==========================================
# CONVERSATION B - RETRIEVE MEMORY
# ==========================================

conversation_b_id = "conversation_B"

results = retrieve_memories(
    db=db,
    keyword="CROSS CONVERSATION TEST RAZERS",
    limit=10,
)

assert len(results) >= 1

found_memory = next(
    (
        item for item in results
        if item.content == "CROSS CONVERSATION TEST RAZERS suka Python"
    ),
    None,
)

assert found_memory is not None
assert found_memory.source_conversation_id == "conversation_A"
assert conversation_b_id != found_memory.source_conversation_id

print("CROSS-CONVERSATION RETRIEVAL: PASS")
print("Memory source:", found_memory.source_conversation_id)
print("Memory accessed from:", conversation_b_id)
print("Memory content:", found_memory.content)


# ==========================================
# CLEANUP
# ==========================================

db.query(Memory).filter(
    Memory.content == "CROSS CONVERSATION TEST RAZERS suka Python"
).delete(synchronize_session=False)

db.commit()
db.close()

print("TEST CLEANUP: SUCCESS")
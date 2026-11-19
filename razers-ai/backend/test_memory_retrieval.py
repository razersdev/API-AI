from database.connection import SessionLocal
from database.models import Memory
from services.memory_service import retrieve_memories


# ==========================================
# SETUP TEST MEMORY
# ==========================================

db = SessionLocal()

test_memory = Memory(
    content="Razers AI menggunakan SQLite untuk persistent memory retrieval.",
    category="project",
    importance=5,
)

db.add(test_memory)
db.commit()

print("Test memory created.")


# ==========================================
# TEST MEMORY RETRIEVAL
# ==========================================

results = retrieve_memories(
    db=db,
    keyword="SQLite",
    limit=10,
)


# ==========================================
# VALIDATION
# ==========================================

assert len(results) > 0

found = any(
    "SQLite" in memory.content
    for memory in results
)

assert found

print("MEMORY RETRIEVAL: PASS")
print(f"Memories found: {len(results)}")


# ==========================================
# CLEANUP
# ==========================================

db.delete(test_memory)
db.commit()
db.close()

print("TEST CLEANUP: SUCCESS")
from database.connection import SessionLocal
from database.models import Memory


# ==========================================
# TEST 1 — SAVE MEMORY
# ==========================================

db = SessionLocal()

test_memory = Memory(
    content="Persistence Test Razers AI CP40",
    category="project",
    importance=5,
)

db.add(test_memory)
db.commit()

memory_id = test_memory.id

print(f"Memory saved with ID: {memory_id}")

db.close()


# ==========================================
# TEST 2 — REOPEN DATABASE
# ==========================================

db = SessionLocal()

saved_memory = db.query(Memory).filter(
    Memory.id == memory_id
).first()


# ==========================================
# VALIDATION
# ==========================================

assert saved_memory is not None
assert saved_memory.content == "Persistence Test Razers AI CP40"

print("MEMORY PERSISTENCE: PASS")
print("Memory survived database session closure.")

# Cleanup test data
db.delete(saved_memory)
db.commit()
db.close()

print("TEST CLEANUP: SUCCESS")
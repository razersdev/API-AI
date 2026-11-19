from database.connection import SessionLocal
from database.models import Memory
from services.memory_service import retrieve_memories


db = SessionLocal()

# ==========================================
# SETUP TEST DATA
# ==========================================

low_memory = Memory(
    content="IMPORTANCE TEST RAZERS LOW PRIORITY",
    category="project",
    importance=1,
)

high_memory = Memory(
    content="IMPORTANCE TEST RAZERS HIGH PRIORITY",
    category="project",
    importance=5,
)

db.add_all([low_memory, high_memory])
db.commit()

print("Test memories created.")


# ==========================================
# TEST IMPORTANCE PRIORITIZATION
# ==========================================

results = retrieve_memories(
    db=db,
    keyword="IMPORTANCE TEST RAZERS",
    limit=10,
)


# ==========================================
# VALIDATION
# ==========================================

assert len(results) >= 2

test_results = [
    memory
    for memory in results
    if "IMPORTANCE TEST RAZERS" in memory.content
]

assert len(test_results) == 2

assert test_results[0].importance >= test_results[1].importance

assert test_results[0].content == (
    "IMPORTANCE TEST RAZERS HIGH PRIORITY"
)

print("IMPORTANCE PRIORITIZATION: PASS")

for memory in test_results:
    print(
        f"Importance: {memory.importance} | "
        f"Content: {memory.content}"
    )


# ==========================================
# CLEANUP
# ==========================================

db.query(Memory).filter(
    Memory.content.like("IMPORTANCE TEST RAZERS%")
).delete(synchronize_session=False)

db.commit()
db.close()

print("TEST CLEANUP: SUCCESS")
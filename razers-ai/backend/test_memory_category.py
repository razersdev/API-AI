
from database.connection import SessionLocal
from database.models import Memory
from services.memory_service import retrieve_memories


db = SessionLocal()

# ==========================================
# SETUP TEST DATA
# ==========================================

personal_memory = Memory(
    content="CATEGORY TEST PERSONAL RAZERS",
    category="personal",
    importance=3,
)

project_memory = Memory(
    content="CATEGORY TEST PROJECT RAZERS",
    category="project",
    importance=5,
)

db.add_all([personal_memory, project_memory])
db.commit()

print("Test memories created.")


# ==========================================
# TEST CATEGORY FILTER
# ==========================================

results = retrieve_memories(
    db=db,
    category="personal",
    limit=10,
)

# ==========================================
# VALIDATION
# ==========================================

assert len(results) >= 1

assert all(
    memory.category == "personal"
    for memory in results
)

assert any(
    memory.content == "CATEGORY TEST PERSONAL RAZERS"
    for memory in results
)

assert not any(
    memory.content == "CATEGORY TEST PROJECT RAZERS"
    for memory in results
)

print("CATEGORY FILTERING: PASS")
print(f"Personal memories found: {len(results)}")


# ==========================================
# CLEANUP
# ==========================================

db.query(Memory).filter(
    Memory.content.in_([
        "CATEGORY TEST PERSONAL RAZERS",
        "CATEGORY TEST PROJECT RAZERS",
    ])
).delete(synchronize_session=False)

db.commit()
db.close()

print("TEST CLEANUP: SUCCESS")
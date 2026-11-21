
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database.connection import Base
from services.memory_service import (
    retrieve_memories,
    create_memory,
    get_memory,
    update_memory,
    delete_memory,
)


# ==========================================
# TEST DATABASE
# ==========================================

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base.metadata.create_all(bind=engine)

db = TestingSessionLocal()


# ==========================================
# MEMORY SERVICE TEST
# ==========================================

print("\n=== MEMORY SERVICE TEST ===")


# TEST CREATE
memory = create_memory(
    db=db,
    content="Belajar FastAPI",
    category="knowledge",
    importance=3,
)

assert memory is not None
assert memory.content == "Belajar FastAPI"

print("[PASS] CREATE")


# TEST GET
retrieved = get_memory(
    db=db,
    memory_id=memory.id,
)

assert retrieved is not None
assert retrieved.id == memory.id

print("[PASS] GET")


# TEST RETRIEVE
memories = retrieve_memories(
    db=db,
    keyword="FastAPI",
)

assert len(memories) >= 1
assert memories[0].content == "Belajar FastAPI"

print("[PASS] RETRIEVE")


# TEST UPDATE
updated = update_memory(
    db=db,
    memory_id=memory.id,
    content="Belajar FastAPI Advanced",
    importance=5,
)

assert updated is not None
assert updated.content == "Belajar FastAPI Advanced"
assert updated.importance == 5

print("[PASS] UPDATE")


# TEST DELETE
deleted = delete_memory(
    db=db,
    memory_id=memory.id,
)

assert deleted is True
assert get_memory(db=db, memory_id=memory.id) is None

print("[PASS] DELETE")


# ==========================================
# CLEANUP
# ==========================================

db.close()
Base.metadata.drop_all(bind=engine)
engine.dispose()


print("\nSERVICE TEST: 5/5 PASS")


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database.connection import Base
from database.models import Memory

from database.repository import (
    create_memory,
    get_memory_by_id,
    update_memory,
    delete_memory,
)


# ==========================================
# TEST DATABASE
# ==========================================

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


# ==========================================
# SETUP
# ==========================================

Base.metadata.create_all(bind=test_engine)

db = TestingSessionLocal()


try:

    print("\n=== MEMORY CRUD TEST ===\n")

    # ======================================
    # TEST CREATE
    # ======================================

    memory = create_memory(
        db=db,
        content="CRUD testing Razers AI",
        category="project",
        importance=5,
        source_conversation_id="test-crud-001",
    )

    assert memory.id is not None
    assert memory.content == "CRUD testing Razers AI"

    print("[PASS] CREATE")


    # ======================================
    # TEST READ
    # ======================================

    retrieved_memory = get_memory_by_id(
        db=db,
        memory_id=memory.id,
    )

    assert retrieved_memory is not None
    assert retrieved_memory.content == "CRUD testing Razers AI"

    print("[PASS] READ")


    # ======================================
    # TEST UPDATE
    # ======================================

    updated_memory = update_memory(
        db=db,
        memory_id=memory.id,
        content="CRUD testing Razers AI CP41",
        category="knowledge",
        importance=4,
    )

    assert updated_memory is not None
    assert updated_memory.content == "CRUD testing Razers AI CP41"
    assert updated_memory.category == "knowledge"
    assert updated_memory.importance == 4

    print("[PASS] UPDATE")


    # ======================================
    # TEST DELETE
    # ======================================

    deleted = delete_memory(
        db=db,
        memory_id=memory.id,
    )

    assert deleted is True

    remaining_memory = get_memory_by_id(
        db=db,
        memory_id=memory.id,
    )

    assert remaining_memory is None

    print("[PASS] DELETE")


    # ======================================
    # TEST EDGE CASES
    # ======================================

    # READ: Memory tidak ditemukan
    missing_memory = get_memory_by_id(
        db=db,
        memory_id=99999,
    )

    assert missing_memory is None

    print("[PASS] READ NON-EXISTENT MEMORY")


    # UPDATE: Memory tidak ditemukan
    missing_update = update_memory(
        db=db,
        memory_id=99999,
        content="Tidak seharusnya tersimpan",
    )

    assert missing_update is None

    print("[PASS] UPDATE NON-EXISTENT MEMORY")


    # DELETE: Memory tidak ditemukan
    missing_delete = delete_memory(
        db=db,
        memory_id=99999,
    )

    assert missing_delete is False

    print("[PASS] DELETE NON-EXISTENT MEMORY")


    # ======================================
    # FINAL RESULT
    # ======================================

    print("\n==============================")
    print("CRUD TEST: 7/7 PASS")
    print("==============================\n")


finally:

    db.close()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()

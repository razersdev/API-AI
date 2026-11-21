
from sqlalchemy.orm import Session

from database.repository import (
    search_memories,
    create_memory as repository_create_memory,
    get_memory_by_id,
    update_memory as repository_update_memory,
    delete_memory as repository_delete_memory,
)


# ==========================================
# RETRIEVE MEMORIES
# ==========================================

def retrieve_memories(
    db: Session,
    keyword: str | None = None,
    category: str | None = None,
    limit: int = 10,
):
    """
    Service untuk mengambil persistent memory.
    """

    # Validasi batas hasil pencarian
    if limit < 1:
        limit = 1

    if limit > 50:
        limit = 50

    # Bersihkan input pencarian
    if keyword:
        keyword = keyword.strip()

    if category:
        category = category.strip().lower()

    # Ambil data melalui repository
    memories = search_memories(
        db=db,
        keyword=keyword,
        category=category,
        limit=limit,
    )

    return memories


# ==========================================
# CREATE MEMORY
# ==========================================

def create_memory(
    db: Session,
    content: str,
    category: str,
    importance: int = 1,
    source_conversation_id: str | None = None,
):
    """
    Service untuk membuat persistent memory.
    """

    content = content.strip()
    category = category.strip().lower()

    return repository_create_memory(
        db=db,
        content=content,
        category=category,
        importance=importance,
        source_conversation_id=source_conversation_id,
    )


# ==========================================
# GET MEMORY BY ID
# ==========================================

def get_memory(
    db: Session,
    memory_id: int,
):
    """
    Service untuk mengambil memory berdasarkan ID.
    """

    return get_memory_by_id(
        db=db,
        memory_id=memory_id,
    )


# ==========================================
# UPDATE MEMORY
# ==========================================

def update_memory(
    db: Session,
    memory_id: int,
    content: str | None = None,
    category: str | None = None,
    importance: int | None = None,
):
    """
    Service untuk memperbarui persistent memory.
    """

    if content is not None:
        content = content.strip()

    if category is not None:
        category = category.strip().lower()

    return repository_update_memory(
        db=db,
        memory_id=memory_id,
        content=content,
        category=category,
        importance=importance,
    )


# ==========================================
# DELETE MEMORY
# ==========================================

def delete_memory(
    db: Session,
    memory_id: int,
):
    """
    Service untuk menghapus persistent memory.
    """

    return repository_delete_memory(
        db=db,
        memory_id=memory_id,
    )

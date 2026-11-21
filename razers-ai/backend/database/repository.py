
from sqlalchemy.orm import Session

from database.models import Memory


# ==========================================
# SEARCH MEMORIES
# ==========================================

def search_memories(
    db: Session,
    keyword: str | None = None,
    category: str | None = None,
    limit: int = 10,
):
    """
    Mencari persistent memory berdasarkan keyword
    dan kategori.
    """

    query = db.query(Memory)

    # Filter berdasarkan keyword
    if keyword:
        query = query.filter(
            Memory.content.ilike(f"%{keyword}%")
        )

    # Filter berdasarkan kategori
    if category:
        query = query.filter(
            Memory.category == category
        )

    # Prioritaskan memory dengan importance tertinggi
    query = query.order_by(
        Memory.importance.desc(),
        Memory.updated_at.desc(),
    )

    # Batasi jumlah hasil
    return query.limit(limit).all()


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
    Membuat persistent memory baru.
    """

    memory = Memory(
        content=content,
        category=category,
        importance=importance,
        source_conversation_id=source_conversation_id,
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory


# ==========================================
# GET MEMORY BY ID
# ==========================================

def get_memory_by_id(
    db: Session,
    memory_id: int,
):
    """
    Mengambil memory berdasarkan ID.
    """

    return db.query(Memory).filter(
        Memory.id == memory_id
    ).first()


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
    Memperbarui persistent memory.
    """

    memory = get_memory_by_id(
        db=db,
        memory_id=memory_id,
    )

    # Memory tidak ditemukan
    if not memory:
        return None

    # Update content
    if content is not None:
        memory.content = content

    # Update category
    if category is not None:
        memory.category = category

    # Update importance
    if importance is not None:
        memory.importance = importance

    db.commit()
    db.refresh(memory)

    return memory


# ==========================================
# DELETE MEMORY
# ==========================================

def delete_memory(
    db: Session,
    memory_id: int,
):
    """
    Menghapus persistent memory berdasarkan ID.
    """

    memory = get_memory_by_id(
        db=db,
        memory_id=memory_id,
    )

    # Memory tidak ditemukan
    if not memory:
        return False

    db.delete(memory)
    db.commit()

    return True

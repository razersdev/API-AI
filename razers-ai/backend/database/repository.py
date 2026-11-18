
from sqlalchemy.orm import Session

from database.models import Memory


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

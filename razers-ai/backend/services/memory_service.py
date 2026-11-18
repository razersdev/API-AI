
from sqlalchemy.orm import Session

from database.repository import search_memories


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

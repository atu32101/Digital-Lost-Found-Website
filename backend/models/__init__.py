"""
SQLAlchemy models package.
"""

# Import models so SQLAlchemy registers them for `db.create_all()`.
from backend.models.user import User  # noqa: F401
from backend.models.lost_items import LostItem  # noqa: F401
from backend.models.found_items import FoundItem  # noqa: F401



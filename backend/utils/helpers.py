import os
import uuid
from datetime import datetime, timezone
from typing import Optional

from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename: str) -> bool:
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[-1].lower().strip()
    return ext in ALLOWED_EXTENSIONS


def generate_image_filename(original_filename: str) -> str:
    """
    Generates a safe random filename while preserving extension.
    """
    ext = original_filename.rsplit(".", 1)[-1].lower()
    return f"{uuid.uuid4().hex}.{ext}"


def utc_now():
    return datetime.now(timezone.utc)


def parse_date(date_str: Optional[str]) -> Optional[datetime.date]:
    """
    Parses YYYY-MM-DD coming from HTML <input type="date">.
    """
    if not date_str:
        return None
    # Keep strict parsing (prevents weird formats)
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def ensure_upload_dir(upload_dir: str) -> None:
    os.makedirs(upload_dir, exist_ok=True)


def save_upload_image(storage, upload_dir: str) -> str:
    """
    Saves an uploaded file to upload_dir and returns the stored filename.
    """
    ensure_upload_dir(upload_dir)
    original = storage.filename or ""
    original = secure_filename(original)
    if not allowed_file(original):
        raise ValueError("Invalid image file type.")

    filename = generate_image_filename(original)
    dest = os.path.join(upload_dir, filename)
    storage.save(dest)
    return filename


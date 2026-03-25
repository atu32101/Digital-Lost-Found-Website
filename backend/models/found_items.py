from datetime import datetime, timezone

from backend.extensions import db


def _utc_now():
    return datetime.now(timezone.utc)


class FoundItem(db.Model):
    __tablename__ = "found_items"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(80), nullable=True, index=True)
    date = db.Column(db.Date, nullable=True, index=True)
    location = db.Column(db.String(200), nullable=True)

    image_filename = db.Column(db.String(255), nullable=True)
    contact_email = db.Column(db.String(120), nullable=True)
    contact_phone = db.Column(db.String(50), nullable=True)

    status = db.Column(db.String(20), nullable=False, default="unclaimed", index=True)
    claimed_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    claimed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=_utc_now)

    reporter = db.relationship("User", foreign_keys=[user_id], backref="found_items")
    claimed_by = db.relationship("User", foreign_keys=[claimed_by_user_id])

    def to_dict(self, include_contact: bool = False, include_image: bool = True):
        image_url = None
        if include_image and self.image_filename:
            image_url = f"/uploads/{self.image_filename}"

        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "date": self.date.isoformat() if self.date else None,
            "location": self.location,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "image_url": image_url,
        }

        if include_contact:
            data["contact_email"] = self.contact_email
            data["contact_phone"] = self.contact_phone

        if self.status == "claimed" and self.claimed_at:
            data["claimed_at"] = self.claimed_at.isoformat()

        return data


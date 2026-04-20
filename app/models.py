"""Database models for the Centralized Alumni Management System."""

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Load a user by primary key for Flask-Login session management."""
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """Application user model for authentication and role management."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship("AlumniProfile", back_populates="user", uselist=False)
    mentorship_requests = db.relationship(
        "Mentorship",
        back_populates="student",
        foreign_keys="Mentorship.student_id",
        lazy=True,
    )
    mentorship_offers = db.relationship(
        "Mentorship",
        back_populates="alumni",
        foreign_keys="Mentorship.alumni_id",
        lazy=True,
    )
    event_registrations = db.relationship(
        "EventRegistration", back_populates="user", cascade="all, delete-orphan"
    )

    def set_password(self, password):
        """Generate and store a password hash for the user."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Validate a plain-text password against the stored hash."""
        return check_password_hash(self.password_hash, password)


class AlumniProfile(db.Model):
    """Extended profile data for alumni users."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    batch = db.Column(db.String(20), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(120), nullable=True)
    job_role = db.Column(db.String(120), nullable=True)
    skills = db.Column(db.String(255), nullable=True)
    linkedin = db.Column(db.String(255), nullable=True)

    user = db.relationship("User", back_populates="profile")


class Mentorship(db.Model):
    """Mentorship requests made by students to alumni."""

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    alumni_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("User", foreign_keys=[student_id], back_populates="mentorship_requests")
    alumni = db.relationship("User", foreign_keys=[alumni_id], back_populates="mentorship_offers")


class Event(db.Model):
    """Event details created by administrators."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    registrations = db.relationship(
        "EventRegistration", back_populates="event", cascade="all, delete-orphan"
    )


class EventRegistration(db.Model):
    """User registration mapping for events."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="event_registrations")
    event = db.relationship("Event", back_populates="registrations")

    __table_args__ = (db.UniqueConstraint("user_id", "event_id", name="unique_user_event"),)


class Announcement(db.Model):
    """Announcements created by admins and displayed to all users."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

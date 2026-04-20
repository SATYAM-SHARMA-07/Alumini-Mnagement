"""Admin-specific routes for announcements and event management."""

from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from app import db
from app.models import Announcement, Event
from app.utils.decorators import roles_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/announcements", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def announcements():
    """Create and list platform-wide announcements."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Title and content are required.", "danger")
            return redirect(url_for("admin.announcements"))

        announcement = Announcement(title=title, content=content, created_by=current_user.id)
        db.session.add(announcement)
        db.session.commit()

        flash("Announcement posted successfully.", "success")
        return redirect(url_for("admin.announcements"))

    announcement_list = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template("announcements.html", announcements=announcement_list)


@admin_bp.route("/events/create", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def create_event():
    """Create a new event as an administrator."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        event_date_str = request.form.get("event_date", "").strip()
        location = request.form.get("location", "").strip()

        if not all([title, description, event_date_str, location]):
            flash("All fields are required.", "danger")
            return redirect(url_for("admin.create_event"))

        try:
            event_date = datetime.strptime(event_date_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            flash("Invalid date format.", "danger")
            return redirect(url_for("admin.create_event"))

        event = Event(
            title=title,
            description=description,
            event_date=event_date,
            location=location,
            created_by=current_user.id,
        )
        db.session.add(event)
        db.session.commit()

        flash("Event created successfully.", "success")
        return redirect(url_for("events.list_events"))

    return render_template("create_event.html")

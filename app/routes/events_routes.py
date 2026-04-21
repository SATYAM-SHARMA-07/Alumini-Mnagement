"""Event listing and registration routes."""

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Event, EventRegistration

events_bp = Blueprint("events", __name__, url_prefix="/events")


@events_bp.route("/")
@login_required
def list_events():
    """Show all events with registration status + attendee count."""

    events = Event.query.order_by(Event.event_date.asc()).all()

    # 🔷 Get events user registered for
    registered_event_ids = {
        reg.event_id
        for reg in EventRegistration.query.filter_by(user_id=current_user.id).all()
    }

    # 🔥 NEW: attendee count per event
    event_data = []

    for event in events:
        attendee_count = EventRegistration.query.filter_by(
            event_id=event.id
        ).count()

        event_data.append({
            "event": event,
            "attendee_count": attendee_count
        })

    return render_template(
        "events.html",
        event_data=event_data,
        registered_event_ids=registered_event_ids,
    )


@events_bp.route("/register/<int:event_id>")
@login_required
def register_event(event_id):
    """Register current user for an event if not already registered."""

    event = Event.query.get_or_404(event_id)

    existing = EventRegistration.query.filter_by(
        user_id=current_user.id,
        event_id=event.id,
    ).first()

    if existing:
        flash("You are already registered for this event.", "info")
        return redirect(url_for("events.list_events"))

    registration = EventRegistration(
        user_id=current_user.id,
        event_id=event.id
    )

    db.session.add(registration)
    db.session.commit()

    flash("Event registration successful.", "success")
    return redirect(url_for("events.list_events"))
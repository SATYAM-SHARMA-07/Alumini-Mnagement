"""Mentorship request, review, and status routes."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Mentorship, User
from app.utils.decorators import roles_required

mentorship_bp = Blueprint("mentorship", __name__, url_prefix="/mentorship")


@mentorship_bp.route("/", methods=["GET", "POST"])
@login_required
def mentorship_home():
    """Show mentorship dashboard and allow students to submit requests."""
    alumni_users = User.query.filter_by(role="alumni").all()

    if request.method == "POST":
        if current_user.role != "student":
            flash("Only students can submit mentorship requests.", "danger")
            return redirect(url_for("mentorship.mentorship_home"))

        alumni_id = request.form.get("alumni_id", type=int)
        message = request.form.get("message", "").strip()

        if not alumni_id:
            flash("Please choose an alumni mentor.", "danger")
            return redirect(url_for("mentorship.mentorship_home"))

        existing = Mentorship.query.filter_by(
            student_id=current_user.id,
            alumni_id=alumni_id,
            status="pending",
        ).first()
        if existing:
            flash("You already have a pending request with this alumni.", "warning")
            return redirect(url_for("mentorship.mentorship_home"))

        mentorship = Mentorship(student_id=current_user.id, alumni_id=alumni_id, message=message)
        db.session.add(mentorship)
        db.session.commit()

        flash("Mentorship request sent.", "success")
        return redirect(url_for("mentorship.mentorship_home"))

    if current_user.role == "student":
        requests = Mentorship.query.filter_by(student_id=current_user.id).order_by(Mentorship.created_at.desc()).all()
    elif current_user.role == "alumni":
        requests = Mentorship.query.filter_by(alumni_id=current_user.id).order_by(Mentorship.created_at.desc()).all()
    else:
        requests = Mentorship.query.order_by(Mentorship.created_at.desc()).all()

    return render_template("mentorship.html", requests=requests, alumni_users=alumni_users)


@mentorship_bp.route("/update/<int:request_id>/<string:action>")
@login_required
@roles_required("alumni")
def update_request(request_id, action):
    """Allow alumni to accept or reject pending mentorship requests."""
    mentorship_request = Mentorship.query.get_or_404(request_id)

    if mentorship_request.alumni_id != current_user.id:
        flash("You are not authorized to update this request.", "danger")
        return redirect(url_for("mentorship.mentorship_home"))

    if action not in {"accept", "reject"}:
        flash("Invalid action.", "danger")
        return redirect(url_for("mentorship.mentorship_home"))

    mentorship_request.status = "accepted" if action == "accept" else "rejected"
    db.session.commit()

    flash(f"Request {mentorship_request.status}.", "success")
    return redirect(url_for("mentorship.mentorship_home"))

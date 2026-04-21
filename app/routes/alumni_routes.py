"""Alumni, dashboard, profile, and directory routes."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import AlumniProfile, Announcement, Event, Mentorship, User

alumni_bp = Blueprint("alumni", __name__)


@alumni_bp.route("/")
def index():
    """Redirect users to dashboard or login."""
    if current_user.is_authenticated:
        return redirect(url_for("alumni.dashboard"))
    return redirect(url_for("auth.login"))


@alumni_bp.route("/dashboard")
@login_required
def dashboard():
    """Render role-aware dashboard with analytics and updates."""

    # 🔷 Announcements + Events
    announcements = Announcement.query.order_by(
        Announcement.created_at.desc()
    ).limit(5).all()

    upcoming_events = Event.query.order_by(
        Event.event_date.asc()
    ).limit(5).all()

    # 🔥 NEW ANALYTICS
    total_alumni = User.query.filter_by(role="alumni").count()
    total_events = Event.query.count()
    total_mentorships = Mentorship.query.count()

    # 🔷 Base context
    context = {
        "announcements": announcements,
        "upcoming_events": upcoming_events,
        "mentorship_count": 0,
        "total_alumni": total_alumni,
        "total_events": total_events,
        "total_mentorships": total_mentorships,  # optional (future use)
    }

    # 🔷 Role-based mentorship count
    if current_user.role == "student":
        context["mentorship_count"] = Mentorship.query.filter_by(
            student_id=current_user.id
        ).count()

    elif current_user.role == "alumni":
        context["mentorship_count"] = Mentorship.query.filter_by(
            alumni_id=current_user.id
        ).count()

    return render_template("dashboard.html", **context)


@alumni_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Create or update alumni profile details."""

    profile_obj = AlumniProfile.query.filter_by(
        user_id=current_user.id
    ).first()

    if request.method == "POST":

        if current_user.role != "alumni":
            flash("Only alumni users can maintain alumni profiles.", "danger")
            return redirect(url_for("alumni.dashboard"))

        batch = request.form.get("batch", "").strip()
        branch = request.form.get("branch", "").strip()
        company = request.form.get("company", "").strip()
        job_role = request.form.get("job_role", "").strip()
        skills = request.form.get("skills", "").strip()
        linkedin = request.form.get("linkedin", "").strip()

        if not batch or not branch:
            flash("Batch and branch are required.", "danger")
            return redirect(url_for("alumni.profile"))

        if not profile_obj:
            profile_obj = AlumniProfile(
                user_id=current_user.id,
                batch=batch,
                branch=branch
            )
            db.session.add(profile_obj)

        profile_obj.batch = batch
        profile_obj.branch = branch
        profile_obj.company = company
        profile_obj.job_role = job_role
        profile_obj.skills = skills
        profile_obj.linkedin = linkedin

        db.session.commit()

        flash("Profile updated successfully.", "success")
        return redirect(url_for("alumni.profile"))

    return render_template("profile.html", profile=profile_obj)


@alumni_bp.route("/directory")
@login_required
def directory():
    """Display alumni directory with search and filters."""

    batch = request.args.get("batch", "").strip()
    company = request.args.get("company", "").strip()
    skills = request.args.get("skills", "").strip()

    query = AlumniProfile.query.join(AlumniProfile.user)

    if batch:
        query = query.filter(AlumniProfile.batch.ilike(f"%{batch}%"))

    if company:
        query = query.filter(AlumniProfile.company.ilike(f"%{company}%"))

    if skills:
        query = query.filter(AlumniProfile.skills.ilike(f"%{skills}%"))

    profiles = query.all()

    return render_template(
        "directory.html",
        profiles=profiles,
        filters={
            "batch": batch,
            "company": company,
            "skills": skills
        },
    )
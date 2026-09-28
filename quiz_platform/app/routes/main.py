from flask import Blueprint, redirect, render_template, request, session, url_for, flash

from .. import db
from ..models import Candidate

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def home():
    return render_template("home.html")


@main_bp.route("/candidate", methods=["GET", "POST"])
def candidate():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        candidate_code = request.form.get("candidate_id", "").strip()
        branch = request.form.get("branch", "").strip()
        year = request.form.get("year", "").strip()
        section = request.form.get("section", "").strip()

        if not name or not candidate_code:
            flash("Candidate name and ID are required.", "danger")
            return render_template("candidate.html")
        if len(name) > 120 or len(candidate_code) > 64:
            flash("Name or ID too long.", "danger")
            return render_template("candidate.html")

        candidate = Candidate.query.filter_by(candidate_code=candidate_code).first()
        if not candidate:
            candidate = Candidate(
                name=name,
                candidate_code=candidate_code,
                branch=branch or "N/A",
                year=year or "N/A",
                section=section or "N/A",
            )
            db.session.add(candidate)
            db.session.commit()

        session["candidate_id"] = candidate.id
        return redirect(url_for("exam.configure_exam"))

    return render_template("candidate.html")


@main_bp.get("/history")
def history_redirect():
    return redirect(url_for("result.history"))

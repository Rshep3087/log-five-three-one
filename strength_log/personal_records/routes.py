from strength_log import db
from strength_log.personal_records.forms import PersonalRecordForm
from strength_log.models import (
    SquatPersonalRecord,
    BenchPersonalRecord,
    DeadliftPersonalRecord,
    PressPersonalRecord,
    User,
    GeneralSetting,
)

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from loguru import logger


personal_records = Blueprint("user_personal_records", __name__)


@personal_records.route("/personal_records", methods=["GET", "POST"])
@login_required
def new_personal_records():
    user = User.query.get(current_user.id)

    if not user.authenticated:
        flash("Account must be authenticated to access Personal Records.", "danger")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        form = PersonalRecordForm()
        if form.validate_on_submit():
            squat_record = SquatPersonalRecord(
                one_rep=form.squat.data["one_rep"],
                two_reps=form.squat.data["two_reps"],
                three_reps=form.squat.data["three_reps"],
                four_reps=form.squat.data["four_reps"],
                five_reps=form.squat.data["five_reps"],
                lifter=current_user,
            )
            bench_record = BenchPersonalRecord(
                one_rep=form.bench.data["one_rep"],
                two_reps=form.bench.data["two_reps"],
                three_reps=form.bench.data["three_reps"],
                four_reps=form.bench.data["four_reps"],
                five_reps=form.bench.data["five_reps"],
                lifter=current_user,
            )
            deadlift_record = DeadliftPersonalRecord(
                one_rep=form.deadlift.data["one_rep"],
                two_reps=form.deadlift.data["two_reps"],
                three_reps=form.deadlift.data["three_reps"],
                four_reps=form.deadlift.data["four_reps"],
                five_reps=form.deadlift.data["five_reps"],
                lifter=current_user,
            )
            press_record = PressPersonalRecord(
                one_rep=form.press.data["one_rep"],
                two_reps=form.press.data["two_reps"],
                three_reps=form.press.data["three_reps"],
                four_reps=form.press.data["four_reps"],
                five_reps=form.press.data["five_reps"],
                lifter=current_user,
            )

            db.session.add(squat_record)
            db.session.add(bench_record)
            db.session.add(deadlift_record)
            db.session.add(press_record)

            db.session.commit()

            flash("Your PR was successfully logged.", "success")

            return redirect(url_for("main.home"))

    user_squat_records = SquatPersonalRecord.query.filter_by(
        user_id=current_user.id
    ).first()

    user_bench_records = BenchPersonalRecord.query.filter_by(
        user_id=current_user.id
    ).first()

    user_deadlift_records = DeadliftPersonalRecord.query.filter_by(
        user_id=current_user.id
    ).first()

    user_press_records = PressPersonalRecord.query.filter_by(
        user_id=current_user.id
    ).first()

    form = PersonalRecordForm(
        squat=user_squat_records,
        bench=user_bench_records,
        deadlift=user_deadlift_records,
        press=user_press_records,
    )
    settings = GeneralSetting.query.filter_by(user=current_user).first()
    if not settings:
        unit = "lbs"
    else:
        unit = settings.unit

    if not user_press_records:
        """If the user has not submitted PR's, share a tip with a info message."""
        flash(
            "Tip: Use Personal Records to track your all-time best lifts on reps 1-5. This is usually not the values you base your programming on, track that in the training max tab.",
            "info",
        )

    return render_template(
        "personal_records.html", form=form, title="Personal Records", unit=unit
    )

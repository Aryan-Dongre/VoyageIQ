from . import profile_bp
from flask import render_template, redirect, session, url_for, flash
from voyageiq.utils.decorators import login_required

from voyageiq.blueprint.profile.forms import ProfileForm
from voyageiq.services.profile_service import ProfileService

@profile_bp.route("/", methods=["GET", "POST"])
@login_required
def profile():

    user_id = session.get("user_id")

    if not user_id:
        flash(
             "Please login first.",
             "warning"
        )

        return redirect(
            url_for("auth.login")
        )
    
    form = ProfileForm()
    
    # Load the profile
    profile = ProfileService.get_profile(user_id)

    if not profile:

        flash(
              "Profile not found",
              "danger"
        )

        return redirect(url_for("dashboard.dashboard"))
    
    if form.validate_on_submit():

        updated = ProfileService.update_profile(form=form, user_id=user_id)

        if  updated:

            flash(
                    "Profile updated Successfully ",
                    "success"
            )

        else:
            flash(
                    "Failed to update profile",
                    "danger"
            )

        return redirect(
             url_for("profile.profile")
        )    

    if not form.is_submitted():

        form.full_name.data = profile["full_name"] 
        form.phone.data = profile["phone"] 
        form.country.data = profile["country"] 
        form.profile_picture.data = profile["profile_picture"]  
    
    return render_template(
        "dashboard/profile/index.html",
        form=form,
        profile=profile
    )
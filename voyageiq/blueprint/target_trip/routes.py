from . import target_trip_bp

from flask import render_template, session, flash, template_rendered, redirect, url_for
from voyageiq.utils.decorators import login_required

from voyageiq.blueprint.target_trip.forms import TargetTripForm
from voyageiq.services.target_trip_service import TravelTripService
from voyageiq.services.target_trip_match_service import TargetTripMatchService

@target_trip_bp.route("/")
@login_required
def target_trip_home():

    user_id = session.get("user_id")

    target_trips = (
                    TravelTripService.get_user_target_trips(user_id)  
    )  # It is use to fetch all the trip belong to user id

    return render_template(
           "dashboard/target_trip/index.html",
           target_trips=target_trips
    )

@target_trip_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_target_trip():

    # This func is for to create a new trip

    form = TargetTripForm()

    if form.validate_on_submit():

        TravelTripService.create_target_trip(
                           form,
                        session["user_id"]
                        )
        flash(
                "Target Trip created successfully.",
                "success"
            )
        
        return redirect(url_for("target_trip.target_trip_home"))
    
    return render_template  (
                          "dashboard/target_trip/create.html",
                          form=form
                            )

@target_trip_bp.route("/<int:target_trip_id>/edit", methods=["GET", "POST"])
@login_required
def edit_target_trip(target_trip_id):

    user_id = session.get("user_id")

    target_trip = (
                   TravelTripService.get_target_trip(target_trip_id,user_id)
                )
    
    if not target_trip:
        flash(
              "Target Trip not found.",
              "danger"
            )
        
        return redirect(url_for("target_trip.target_trip_home"))
    
    form = TargetTripForm(data=target_trip)

    if form.validate_on_submit():

        TravelTripService.update_target_trip(
                         target_trip_id,
                         form,
                         user_id
                        )
        
        flash(
                "Target Trip updated successfully.",
                "success"
        )

        return redirect(url_for( "target_trip.target_trip_home"))
    
    return render_template(
        "dashboard/target_trip/edit.html",
        form=form,
        target_trip=target_trip
    )

@target_trip_bp.route("/<int:target_trip_id>/delete", methods=["GET", "POST"])
@login_required
def delete_target_trip(target_trip_id):

    user_id = session.get("user_id")

    success = (
                 TravelTripService.delete_target_trip(
            target_trip_id,
            user_id
    ))

    if success:

        flash(
                 "Target Trip deleted successfully.",
                 "success"
        )

    else:
        flash(
                "Unable to delete Target Trip.",
                "danger"
        )

    return redirect(url_for("target_trip.target_trip_home"))    

@target_trip_bp.route("/<int:target_trip_id>/matches")
@login_required
def find_matches(target_trip_id):

    user_id = session.get("user_id")

    matches = (
               TargetTripMatchService.find_matches(target_trip_id,user_id)
                    )
    
    if not matches:
        flash(
             "Target Trip not found.",
             "danger"
        )

        return redirect(
            url_for(
                "target_trip.target_trip_home"
            )
        )
    
    target_trips = TravelTripService.get_user_target_trips(user_id)

    print("matches = ", matches)
    print("selected trip", target_trip_id)
    
    return render_template(
        "dashboard/target_trip/index.html",
        target_trips=target_trips,
        matches=matches,
        selected_trip_id=target_trip_id
    )


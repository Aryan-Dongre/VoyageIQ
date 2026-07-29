from flask import  render_template, redirect, url_for, flash
from flask import session, request

from . import auth_bp
from .forms import RegisterForm
from .forms import LoginForm

from voyageiq.services.auth_service import AuthService

# Login part

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        result = AuthService.login_user(form)

        if result["success"]:

            user= result["user"]

            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["email"] = user["email"]

            flash("Login successful", "success")

            return redirect(url_for("dashboard.dashboard"))
        
        flash(result["message"], "danger")

    return render_template(
                    "auth/login.html",
                    form=form)
    

# Register part

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    

    form = RegisterForm()

    if form.validate_on_submit():  # internally flask method ko check karta ki method post hai ki nahi 
        
       
        result = AuthService.register_user(form)

       

        if result["success"]:

            flash(
                result["message"],
                "success"
            )
            return redirect(
                url_for("auth.login")
            )
        flash(
            result["message"],
            "danger"
        )
    return render_template(
        "auth/register.html",
        form=form
    )    

@auth_bp.route("/logout")
def logout() :
    session.clear()   
    return redirect(url_for("auth.login"))
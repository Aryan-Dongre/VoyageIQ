from flask import render_template
from voyageiq.blueprint.home import home_bp

@home_bp.route("/")
def home():
    return render_template("home/index.html")
from voyageiq.blueprint.contact.forms import ContactForm
from voyageiq.services.contact_service import ContactService
from . import contact_bp

from flask import render_template, flash,redirect, url_for

@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():

    form = ContactForm()

    if form.validate_on_submit():

        ContactService.submit_contact(form)

        flash(
               "MESSAGE_SENT",
              "success"
        )
        return redirect(url_for("contact.contact"))



    return render_template(
         "contact/contact.html",
         form=form
    )    


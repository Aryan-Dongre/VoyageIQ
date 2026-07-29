from voyageiq.models.contact_model import create_contact

class ContactService:

    @staticmethod
    def submit_contact(form):
        contact_data = {
                        "full_name": form.full_name.data,
                        "email": form.email.data,
                        "category": form.category.data,
                        "message": form.message.data
                     }
        
        return create_contact(contact_data)
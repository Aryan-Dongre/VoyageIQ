from voyageiq.models.profile_model import ProfileModel

class ProfileService:

    @staticmethod
    def get_profile(user_id):

        profile = ProfileModel.get_user_profile(user_id)

        return profile
    
    @staticmethod
    def update_profile(form, user_id):

        # This is the one way for update service

        profile_data = {
            "full_name" : form.full_name.data,
             "phone": form.phone.data,
             "country": form.country.data,
            "profile_picture": form.profile_picture.data
        }

        return ProfileModel.update_user_profile(
            user_id=user_id,
            full_name = profile_data["full_name"],
            phone=profile_data["phone"],
            country=profile_data["country"],
            profile_picture=profile_data["profile_picture"]
        )
        
        # this is the second way  

        # return ProfileModel.update_user_profile(
        #     user_id=user_id,
        #     full_name=form.full_name.data,
        #     phone=form.phone.data,
        #     country=form.country.data,
        #     profile_picture=form.profile_picture.data
        # )
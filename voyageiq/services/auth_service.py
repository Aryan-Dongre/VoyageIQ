# in this we will maintain and decide the rules of authentication
#like password hash, registration logic etc
# Contain the register and ogin user 

from voyageiq.models.user_model import UserModel

from voyageiq.models.auth_model import AuthModel


from werkzeug.security import(generate_password_hash, check_password_hash)

class AuthService:  # Encapsulation  + Abstraction

    @staticmethod
    def register_user(form):

        print("Register Status")

        email = form.email.data.strip().lower()
        username = form.user_name.data.strip()


        # check email
        existing_user  = UserModel.get_user_by_email(email)

        if existing_user:
            return{
                "success": False,
                "message": "Email already registered."
            }
        
        # check existing username
        existing_auth = AuthModel.get_auth_by_username(username)

        if existing_auth:
            return{
                "success":False,
                "message":"Username already exists."
            }
        
        # Hash password
        password_hash = generate_password_hash(form.password.data)

        # create user
        user_id = UserModel.create_user(
                 full_name=form.full_name.data.strip(),
                 email=email,
                 phone=form.phone.data.strip()
        )

        if not user_id:
            return {
                "success":False,
                "message":"Failed to create user"
            }
        

        #creating authentication record

        AuthModel.create_auth_record(
                           user_id=user_id,
                           username=username,
                           password_hash=password_hash
        )

        return {
            "success":True,
            "message": "Registration successful."
        }

    @staticmethod
    def login_user(form):

        identifier = form.identifier.data.strip()
    
        user = AuthModel.get_login_user(identifier)
        
        if not user:
            return {
                "success":False,
                "message": "Invalid credentials."
            }
        password_valid = check_password_hash(
                         user["password_hash"],
                         form.password.data
        )
        

        if not password_valid:
            return {
                "success": False,
                "message": "Invalid credentials."
            }
        
        return{
            "success":True,
            "message": "Login Successful.",
            "user": user
        }
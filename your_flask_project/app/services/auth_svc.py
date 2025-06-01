from app import db
from app.models.user_model import Users

def create_user(username, email, phone, password):
    """
    Creates a new user.
    Returns (success_boolean, message_or_user_object)
    """
    if Users.query.filter_by(username=username).first():
        return False, "Username already exists."
    if Users.query.filter_by(email=email).first():
        return False, "Email address already registered."
    if Users.query.filter_by(phone=phone).first():
        return False, "Phone number already registered."

    user = Users(username=username, email=email, phone=phone)
    user.set_password(password) # This method is in the Users model

    try:
        db.session.add(user)
        db.session.commit()
        return True, "User registered successfully. Please login."
    except Exception as e:
        db.session.rollback()
        # Log the exception e
        return False, f"An error occurred during registration: {str(e)}"

def authenticate_user(username, password):
    """
    Authenticates a user.
    Returns user object if authentication is successful, None otherwise.
    """
    user = Users.query.filter_by(username=username).first()
    if user and user.check_password(password): # check_password is in Users model
        return user
    return None

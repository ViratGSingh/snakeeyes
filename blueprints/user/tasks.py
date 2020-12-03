from lib.flask_mailplus import send_template_message
from blueprints.user.models import User


def deliver_password_reset_email(user):
    """
    Send a reset password e-mail to a user.

    :param user_id: The user id
    :type user_id: int
    :param reset_token: The reset token
    :type reset_token: str
    :return: None if a user was not found
    """
    
    
    if user is None:
        pass

    ctx = {'user': user["id"], 'reset_token': user["token"]}

    send_template_message(subject='Password reset from Snake Eyes',
                          recipients=[user["email"]],
                          template='user/mail/password_reset',ctx=ctx)

    

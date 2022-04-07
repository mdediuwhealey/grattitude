from grattitude import db, app
from flask import session, g, request, flash, Blueprint, render_template
from grattitude.models import init_models_module 
from grattitude.view_helpers import twiml, check_affirmative, confirm_grattitude, confirm_admin_command
from twilio.twiml.messaging_response import MessagingResponse
import phonenumbers


init_models_module(db, app)

from grattitude.models.user import User

@app.route('/post-gratitude', methods=["POST"])
def post_gratitude():
    values = request.values
    body = request.values.get('Body', None)
    number = request.values.get('From', None)
    number = phonenumbers.format_number(phonenumbers.parse(number, 'US'), phonenumbers.PhoneNumberFormat.E164)
    print("Body: ", body, "Number: ", number)
    user = User.query.filter(User.phone_number == number).first()

    if user.opted_in == False and check_affirmative(body):
        user.opted_in = True
        sms_response_text = render_template('messages/intro_opt_in_response.txt')

    elif confirm_grattitude(body):
        sms_response_text = render_template('messages/response.txt')

    elif user.opted_in == False and not check_affirmative(body):
        sms_response_text = render_template('messages/intro_opt_out_response.txt')

    elif confirm_admin_command(body) and user.is_admin():
        argument = ''.join(body.split()[1:])
        u = User(argument)
        db.session.add(u)
        db.session.commit()
        sms_response_text = render_template('messages/added.txt', number = u.phone_number)

    else:
        sms_response_text = render_template('messages/generic.txt')
        user.left_unresponded += 1

    user.last_message = body
    db.session.add(user)
    db.session.commit()
    return twiml(_respond_message(sms_response_text))

def _respond_message(message):
    response = MessagingResponse()
    response.message(message)
    return response

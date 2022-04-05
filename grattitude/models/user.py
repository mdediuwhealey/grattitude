from airtng_flask.models import app_db, auth_token, account_sid, phone_number
from flask import render_template
from twilio.rest import Client
import  phonenumbers 
from sqlalchemy.sql import func

db = app_db()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String, nullable=False)

    # the number of unresponded messages they have sent me
    left_unresponded = db.Column(db.Integer, nullable=True)

    # if they have recieved an introduction
    introduced = db.Column(db.Boolean, nullable=False, default=0)

    # if they opted in
    opted_in = db.Column(db.Boolean, nullable=False, default=0)

    # to detect people screwing around
    last_message = db.Column(db.String(160), nullable=True)

    # to add people easily
    admin_powers = db.Column(db.Boolean, nullable=False, default=0)

    # to detect people screwing around
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())


    def __init__(self, phone_number):
        self.phone_number = phonenumbers.format_number(phonenumbers.parse(phone_number, 'US'), phonenumbers.PhoneNumberFormat.E164)

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<User %r>' % (self.phone_number)


    def make_introduction(self):
        self._send_message(self.phone_number,
            render_template('messages/introduction.txt'))
        self.introduced = True
        db.session.add(self)
        db.session.commit()

    def ask_grattitude(self):
        self._send_message(self.phone_number,
            render_template('messages/reminder.txt'))
        db.session.add(self)
        db.session.commit()

    def is_admin(self):
        return self.admin_powers == 1 


    def _get_twilio_client(self):
        return Client(account_sid(), auth_token())

    def _send_message(self, to, message):
        self._get_twilio_client().messages.create(
                to=to,
                from_=phone_number(),
                body=message)



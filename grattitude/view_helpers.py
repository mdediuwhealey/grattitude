import flask
from flask import url_for, redirect, render_template

affirmatives = "yes y yee yea ye ya"
negatives = "no nah na n"
admin_commands ="./add"


def twiml(resp):
    resp = flask.Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'
    return resp

def check_affirmative(message):
    message = message.lower()
    for a in affirmatives.split():
        if a in message:
            return True
    for m in message.split():
        if m in affirmatives.split():
            return True
    return False


def confirm_grattitude(message):
    if "am grateful" in message.lower() or "im grateful" in message.lower():
        return True
    return False

def confirm_admin_command(message):
    for command in admin_commands.lower().split():
        if command in message: 
            return True
    return False

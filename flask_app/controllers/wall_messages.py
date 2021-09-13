from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.messages import Message
import flask_app.controllers.login_register

@app.route('/wall')
def user_wall():
    messages = Message.get_msg_by_recipient({"id":session['user_id']})
    print(messages)
    return render_template(
        "wall.html", 
        active_user = User.get_by_id({"id":session['user_id']}), 
        users = User.get_all(), 
        messages = messages
        )

@app.route('/message/send', methods=['POST'])
def save_message():
    if not Message.validate_message(request.form):
        return redirect('/wall')
    Message.save(request.form)
    flash("Message sent!", "msg_sent")
    return redirect('/wall')

@app.route('/message/delete/<int:id>')
def delete_message(id):
    Message.delete({"id":id})
    return redirect("/wall")
# app/routes/chat.py
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from app import db
from app.models.user import User
from app.models.chat import Chat
from app.models.message import Message

chat = Blueprint('chat', __name__)

@chat.route('/')
@login_required
def home():
    chats = current_user.get_chats()
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('home.html', title='Home', chats=chats, users=users)

@chat.route('/chat/<int:chat_id>')
@login_required
def view_chat(chat_id):
    chat_obj = Chat.query.get_or_404(chat_id)
    
    # Make sure the current user is part of this chat
    if chat_obj.user1_id != current_user.id and chat_obj.user2_id != current_user.id:
        return redirect(url_for('chat.home'))
    
    other_user = chat_obj.get_other_user(current_user.id)
    messages = chat_obj.messages.order_by(Message.timestamp).all()
    
    # Mark messages as read
    for message in messages:
        if message.recipient_id == current_user.id and not message.is_read:
            message.is_read = True
    
    db.session.commit()
    
    return render_template('chat.html', title=f'Chat with {other_user.username}', 
                          chat=chat_obj, messages=messages, other_user=other_user)

@chat.route('/create_chat/<int:user_id>', methods=['GET', 'POST'])
@login_required
def create_chat(user_id):
    if user_id == current_user.id:
        return redirect(url_for('chat.home'))
    
    # Check if chat already exists
    existing_chat = Chat.query.filter(
        ((Chat.user1_id == current_user.id) & (Chat.user2_id == user_id)) |
        ((Chat.user1_id == user_id) & (Chat.user2_id == current_user.id))
    ).first()
    
    if existing_chat:
        return redirect(url_for('chat.view_chat', chat_id=existing_chat.id))
    
    # Create new chat
    new_chat = Chat(user1_id=current_user.id, user2_id=user_id)
    db.session.add(new_chat)
    db.session.commit()
    
    return redirect(url_for('chat.view_chat', chat_id=new_chat.id))
# app/routes/message.py
from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import current_user, login_required
from app import db
from app.models.chat import Chat
from app.models.message import Message

message = Blueprint('message', __name__)

@message.route('/send_message/<int:chat_id>', methods=['POST'])
@login_required
def send_message(chat_id):
    chat_obj = Chat.query.get_or_404(chat_id)
    
    # Make sure the current user is part of this chat
    if chat_obj.user1_id != current_user.id and chat_obj.user2_id != current_user.id:
        return redirect(url_for('chat.home'))
    
    content = request.form.get('content')
    if not content:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    # Determine recipient
    recipient_id = chat_obj.user2_id if chat_obj.user1_id == current_user.id else chat_obj.user1_id
    
    # Create message
    new_message = Message(
        content=content,
        sender_id=current_user.id,
        recipient_id=recipient_id,
        chat_id=chat_id
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message_id': new_message.id})
    
    return redirect(url_for('chat.view_chat', chat_id=chat_id))

@message.route('/get_messages/<int:chat_id>', methods=['GET'])
@login_required
def get_messages(chat_id):
    chat_obj = Chat.query.get_or_404(chat_id)
    
    # Make sure the current user is part of this chat
    if chat_obj.user1_id != current_user.id and chat_obj.user2_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    last_id = request.args.get('last_id', 0, type=int)
    messages = chat_obj.messages.filter(Message.id > last_id).order_by(Message.timestamp).all()
    
    # Mark messages as read
    for msg in messages:
        if msg.recipient_id == current_user.id and not msg.is_read:
            msg.is_read = True
    
    db.session.commit()
    
    messages_data = [
        {
            'id': msg.id,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%H:%M | %d %b'),
            'sender_id': msg.sender_id,
            'is_sent_by_me': msg.sender_id == current_user.id
        }
        for msg in messages
    ]
    
    return jsonify({'messages': messages_data})
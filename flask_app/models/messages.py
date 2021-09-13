from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
import math
from datetime import datetime, date

DB = "private_wall_schema"

class Message:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.recipient_id = data['recipient_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 

    def time_since_sent(self):
        now = datetime.now()
        delta = now - self.created_at
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (int(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds()/60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds()/60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages(content, recipient_id, sender_id) VALUES (%(content)s,%(recipient_id)s,%(sender_id)s);"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM messages WHERE id = %(id)s;"
        print(f"Deleted msg with id: {data}")
        return connectToMySQL(DB).query_db(query,data)

    @classmethod
    def get_msg_by_recipient(cls, data):
        query = "SELECT * from messages Left join users on messages.recipient_id = users.id where messages.recipient_id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        messages = []
        for msg in results:
            messages.append(cls(msg))
        return messages

    @staticmethod
    def validate_message(message):
        is_valid = True
        # Name check - works
        if len(message['content']) < 1:
            flash("Please dont leave a blank message.", 'blank_msg')
            is_valid = False
        return is_valid

    
    
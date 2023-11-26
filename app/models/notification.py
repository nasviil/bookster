from app import mysql

class Notification():
  __tablename__ = 'notification'

  def __init__(self, notification_id=None, sender_id=None, receiver_id=None):
    self.notification_id = notification_id
    self.sender_id = sender_id
    self.receiver_id = receiver_id

  def add_notification
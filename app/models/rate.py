from app import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=True)

@classmethod
    def add_review(cls, user_id, book_id, rating, review_text):
        new_review = cls(user_id=user_id, book_id=book_id, rating=rating, review_text=review_text)
        db.session.add(new_review)
        db.session.commit()

class User (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    password= db.Column(db.String(35))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    gender = db.Column(db.String(6))


import app


class User(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    nickname = app.db.Column(app.db.String(64), index=True, unique=True)
    email = app.db.Column(app.db.String(120), index=True, unique=True)
    posts = app.db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            # python 2
            return unicode(self.id)
        except NameError:
            # python 3
            return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    body = app.db.Column(app.db.String(140))
    timestamp = app.db.Column(app.db.DateTime)
    user_id = app.db.Column(app.db.Integer, app.db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

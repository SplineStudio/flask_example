from project.database import db


class DataSystem(db.Model):
    __tablename__ = 'Data_system'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    system_id = db.Column(db.Integer, db.ForeignKey('Dir_system.id'), nullable=False)
    token = db.Column(db.String(120))
    name_slug = db.Column(db.String(120))


class DirSystem(db.Model):
    __tablename__ = 'Dir_system'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    url_img = db.Column(db.String)
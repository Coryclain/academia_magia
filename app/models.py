import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Application(db.Model):
    """
        Student application to the magic academy
        Attributes:
        ----------
        id: int
        name: str
        lastname: str
        identity: str
        age: int
        magical_affinity: str
        created_at: datetime
        status: str
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    identity = db.Column(db.String(10), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    magical_affinity = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    status = db.Column(db.String(20), default='Pending')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastname': self.lastname,
            'identity': self.identity,
            'age': self.age,
            'magical_affinity': self.magical_affinity,
            'status': self.status
        }

class Grimorio(db.Model):
    """
        Grimorio for the students
        Attributes:
        ----------
        id: int
        clover_type: str
        rarity: int
        assignment: str
    """
    id = db.Column(db.Integer, primary_key=True)
    clover_type = db.Column(db.String(20), nullable=False)
    rarity = db.Column(db.Integer, nullable=False)
    assignment = db.Column(db.String(10), db.ForeignKey('application.id'))

    def serialize(self):
        return {
            'id': self.id,
            'clover_type': self.clover_type,
            'rarity': self.rarity,
            'assignment': self.assignment
        }


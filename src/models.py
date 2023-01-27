from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nombre = db.Column(db.String(250), nullable=False)
    apellido = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favoritos = db.relationship("Favoritos", backref='user')

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    __tablename__ = 'people'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False) 
    birth_year = db.Column(db.String(250),nullable=False)
    homeworld = db.Column(db.String(250), nullable=False)
    starship = db.Column(db.String(250), nullable=False)
    favoritos = db.relationship("Favoritos", backref='people')

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "homeworld": self.homeworld,
            "starship": self.starship,
            # do not serialize the password, its a security breac
        }


class Planetas(db.Model):
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    climate = db.Column(db.String (250))
    created = db.Column(db.String (250))
    diameter = db.Column(db.String (250))
    favoritos = db.relationship("Favoritos", backref='planetas')

    def __repr__(self):
        return '<Planetas %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "climate": self.climate,
            "created": self.created,
            "diameter": self.diameter,
            # do not serialize the password, its a security breac
        }


class Favoritos(db.Model):
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    # personajes_id = db.Column(db.Integer, db.ForeignKey('personajes.id'))
    # vehiculos_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id'))
    planetas_id = db.Column(db.Integer, db.ForeignKey('planetas.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))

    def __repr__(self):
        return '<Favoritos %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            # "personajes_id": self.personajes_id,
            # "vehiculos_id": self.vehiculos_id,
            "planetas_id": self.planetas_id,
            "usuario_id": self.usuario_id,
            "people_id": self.people_id,
            # do not serialize the password, its a security breac
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False) 
    model = db.Column(db.String(250), nullable=False)
    vehicle_class = db.Column(db.String(250), nullable=False)
    passengers = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Vehicles %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicles_class": self.vehicle_class,
            "passengers": self.passengers,
            # do not serialize the password, its a security breac
        }


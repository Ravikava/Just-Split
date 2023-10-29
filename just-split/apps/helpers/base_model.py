from sqlalchemy.sql import func
from apps import db
from sqlalchemy.orm.exc import NoResultFound


class BaseModel(db.Model):
    """
    Base Model
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now())

    @classmethod
    def get_or_create(model, query, defaults):
        """
        Get the existing one 
        Or Create the new object
        """
        try:
            # Get the object
            object_instance = model.query.filter_by(**query).one()
            return object_instance, False
        except NoResultFound:
            # Merge defaults
            params = {
                **query,
                **defaults
            }

            return model(**params), True
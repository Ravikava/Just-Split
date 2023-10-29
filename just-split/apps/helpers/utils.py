def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    
    if instance:
        created = False
        return instance,created
    else:
        instance = model(**kwargs)
        created = True
        session.add(instance)
        session.flush()
        session.commit()
        return instance,created
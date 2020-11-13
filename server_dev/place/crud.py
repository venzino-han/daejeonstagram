
def create(model, params):
    #check model exist
    try:
        instance = model.objects.filter(**params).first()
        if instance :
            return None
        else :
            instance = model(**params)
            instance.save()
            return instance
    except Exception as e:
        print(e)

def read(model, params):
    try:
        instance = model.objects.filter(**params).first()
        if instance :
            return instance
        else :
            return None
    except Exception as e:
        print(e)

def update(model, getParams, params):
    try:
        instance = read(model, getParams)
        if not instance :
            return None
        else :
            for k,v in params.items():
                instance[k] = v
            instance.save()

    except Exception as e:
        print(e)

def delete(model, params):
    try:
        instance = read(model, params)
        if not instance:
            return None
        else:
            instance.delete()

    except Exception as e:
        print(e)
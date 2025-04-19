# -*- coding=utf-8 -*-
from flask import current_app
from xp_cms.extensions import db
from sqlalchemy import func, funcfilter, and_, or_
from xp_cms.extensions import mongodb
from mongoengine.queryset.visitor import Q


# from flask_sqlalchemy import record_queries


class XPService:
    model = None

    @classmethod
    def get_one_by_id(cls, pri_id):
        res = cls.model.query.get(pri_id)
        return res

    @classmethod
    def get_one_by_field(cls, field):
        res = None
        try:
            res = cls.model.query.filter(getattr(cls.model, field[0]) == field[1]). \
                first()
        except Exception as e:
            current_app.logger.error(e)
        return res

    @classmethod
    def get_all(cls):
        return cls.model.query.all()

    @classmethod
    def get_all_by_field(cls, field):
        res = cls.model.query.filter(getattr(cls.model, field[0]) == field[1]). \
            all()
        return res

    @classmethod
    def get_many(cls, conditions, order=None, page=None, pageSize=25):
        # [{"field":field, "value":value,  "operator":operator}]
        query = None
        conditions_list = []
        for item in conditions:
            if item['operator'] == "like":
                conditions_list.append(
                    getattr(cls.model, item['field']).like("{keyword}".format(keyword=item['value'])))
            if item['operator'] == "lt":
                conditions_list.append(getattr(cls.model, item['field']) <= item['value'])
            if item['operator'] == "gt":
                conditions_list.append(getattr(cls.model, item['field']) >= item['value'])
            if item['operator'] == "eq":
                conditions_list.append(getattr(cls.model, item['field']) == item['value'])
            if item['operator'] == "neq":
                conditions_list.append(getattr(cls.model, item['field']) != item['value'])
            if item['operator'] == "in":
                conditions_list.append(getattr(cls.model, item['field']).in_(item['value']))

        if conditions_list:
            query = cls.model.query.filter(*conditions_list)
        else:
            query = cls.model.query
        if order:
            # {"field":field, "type":"asc"}
            if order['type'] == "field":
                order = func.field(getattr(cls.model, order['field']), *order['order'])
            elif order['type'] == "multi_fields":
                order_list = [cls.field_order(field) for field in order['fields']]
                order = tuple(order_list)

            elif order['type'] == "desc":
                order = getattr(cls.model, order['field']).desc()
            else:
                order = getattr(cls.model, order['field']).asc()
            if type(order) == tuple:
                query = query.order_by(*order)
            else:
                query = query.order_by(order)

        if page:
            res = query.paginate(page=page, per_page=pageSize)
            pages = res.pages
            return {"items": res.items, "iter_pages": res.iter_pages(), "total": res.total, "pages": pages}
        else:
            pages = 1
            res = query.all()
            return {"items": res, "iter_pages": None, "total": len(res), "pages": pages}

    @classmethod
    def add_by_dicts(cls, dicts, replace=False):
        obj = cls.model(**dicts)
        return cls.add(obj, replace=replace)

    @classmethod
    def add(cls, obj, *other_obj, replace=False):
        if replace:
            db.session.merge(obj)
        else:
            db.session.add(obj)
        for other in other_obj:
            db.session.add(other)
        if cls.commit():
            return obj


    @classmethod
    def delete_by_id(cls, _id):
        obj = cls.get_one_by_id(_id)
        db.session.delete(obj)
        if cls.commit():
            return True

    @classmethod
    def update(cls, obj, *args, **kwargs):
        if cls.commit():
            return obj

    @classmethod
    def commit(cls):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
        else:
            return True

    @classmethod
    def update_columns(cls, conditions, fields):
        try:
            res = db.session.execute(
                db.update(cls.model).values(**fields).filter_by(**conditions)
            )
            db.session.commit()
        except:
            pass
        else:
            return res.rowcount

    @classmethod
    def field_order(cls, field):
        order_field = getattr(cls.model, field[0])
        if field[1] == "asc":
            return order_field.asc()
        else:
            return order_field.asc()


class DocumentBaseService:
    model = None

    @classmethod
    def add(cls, document_data):
        document = cls.model(**document_data)
        try:
            document.save()
        except Exception as e:
            raise e
        else:
            return document

    @classmethod
    def delete_by_id(cls, document_id):
        return cls.model.objects(pk=document_id).delete()

    @classmethod
    def update(cls, document, data=None):

        return document.save()

    @classmethod
    def get_one_by_id(cls, id, fields=None):

        if fields:
            return cls.model.objects(id=id).only(*fields).first()
        return cls.model.objects(id=id).first()

    @classmethod
    def get_all(cls, fields=None):
        if fields:
            return cls.model.objects(id=id).only(*fields).first()
        return cls.model.objects

    @classmethod
    def get_collection_sample(cls, size):
        pipeline = [{"$project": {'_id': 1}}, {"$sample": {"size": size}}]
        collection = cls.model._get_collection()
        return collection.aggregate(pipeline)

    @classmethod
    def get_sample(cls, condition, size):
        pipeline = [{"$project": {'_id': 1}}, {"$sample": {"size": size}}]
        objects = cls.model.objects(**condition)
        return objects.aggregate(pipeline)

    @classmethod
    def get_all_page(cls, page, per_page, conditions=None):
        q = Q()
        if conditions:
            for condition in conditions:
                q = q & Q(**condition)

            return cls.model.objects(q).paginate(page=page, per_page=per_page)
        else:
            return cls.model.objects.paginate(page=page, per_page=per_page)

    @classmethod
    def get_page_by_condition(cls, condition, page, page_size):
        return cls.model.objects.paginate(page=page, per_page=page_size)

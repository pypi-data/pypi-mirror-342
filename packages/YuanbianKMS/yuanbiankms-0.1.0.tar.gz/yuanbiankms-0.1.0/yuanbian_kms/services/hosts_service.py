# -*- coding=utf-8 -*-
from flask import current_app
from xp_cms.services.base_service import XPService
from xp_cms.models.docker_hosts import Hosts, HostIPPort
from xp_cms.extensions import db
from sqlalchemy import func, or_


class HostsService(XPService):
    model = Hosts
    @classmethod
    def list_hosts(cls):
        res = cls.model.query.all()
        return res

    @classmethod
    def add_host(cls, **kwargs):
        with cls.model.session.begin():
            for service, obj in kwargs.items():
                service.add_transaction(obj)
            try:
                cls.model.session.commit()
            except:
                cls.model.session.rollback()



class HostIPPortService(XPService):
    model = HostIPPort
    session = db.session
    @classmethod
    def group_hosts(cls):
        res = cls.session.query(HostIPPort.container_host_name).group_by(HostIPPort.container_host_name).all()
        return res

    @classmethod
    def count_hosts(cls, host_name, used=0):
        res = cls.session.query(func.count(1)).filter(
            HostIPPort.container_status==used , HostIPPort.container_host_name==host_name
        ).one()
        return res

    @classmethod
    def get_free_container(cls, host_ip, username):
        try:
            res = cls.model.query.filter(
            HostIPPort.container_status == 0,  HostIPPort.host_ip == host_ip
        ).filter(or_(HostIPPort.container_user == None, HostIPPort.container_user == username)).first()
        except Exception as e:
            current_app.logger.error(e)
            raise e
        try:
            res.container_user = username
            container = cls.update(res)
        except Exception as e:
            raise e
        return container

    @classmethod
    def get_host_max_port(cls, host_ip):
        try:
            container = cls.model.query.filter(cls.model.host_ip==host_ip).order_by(cls.model.container_id.asc()).first()
        except Exception:
            raise
        else:
            return container

    @classmethod
    def check_port_exits(cls, host_ip, port):
        try:
            container = cls.model.query.filter(cls.model.host_ip==host_ip)\
                .filter(or_(cls.model.container_lab_port.in_(port), cls.model.container_web_port.in_(port)))\
                .first()
        except Exception as e:
            raise e
        else:
            return container




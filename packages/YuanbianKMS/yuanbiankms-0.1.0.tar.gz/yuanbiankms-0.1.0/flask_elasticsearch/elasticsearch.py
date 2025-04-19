# -*- coding=utf-8 -*-
from elasticsearch import Elasticsearch


class FlaskES:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        try:
            url = app.config['ELASTIC_URL']
            user = app.config['ELASTIC_USER']
            password = app.config['ELASTIC_PASSWORD']
            crt = app.config['ELASTIC_SSL_CRT']
        except Exception as e:
            print(e)
        else:
            if url[:5] == "https":
                self.client = Elasticsearch(url,
                                    ca_certs=crt,
                                    basic_auth=(user, password)
                                )
            else:
                self.client = Elasticsearch(url,
                                            basic_auth=(user, password)
                                            )

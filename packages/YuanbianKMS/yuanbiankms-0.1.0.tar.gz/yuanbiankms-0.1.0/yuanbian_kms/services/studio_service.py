# -*- coding=utf-8 -*-
from xp_cms.extensions import db, nosql
from .base_service import XPService


class StudioService(XPService):
    db_name = "mall_center"
    collection_name = "studios"

    def __init__(self):
        self.collection = nosql.mongo_client.select_collection(self.db_name, self.collection_name)
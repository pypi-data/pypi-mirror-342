# -*- coding=utf-8 -*-
from abc import ABC, abstractmethod


class AbstractLogin(ABC):
    @abstractmethod
    def login(self, *args, **kwargs):
        pass

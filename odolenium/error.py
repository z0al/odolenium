#! python3
# -*- coding: utf-8 -*-

class OdoleniumError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


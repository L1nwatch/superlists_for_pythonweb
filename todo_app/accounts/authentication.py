#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 自定义认证函数
"""

import requests
import logging
from django.conf import settings
from django.contrib.auth import get_user_model

__author__ = '__L1n__w@tch'

PERSONA_VERIFY_URL = "https://verifier.login.persona.org/verify"
User = get_user_model()
logger = logging.getLogger(__name__)


class PersonaAuthenticationBackend(object):
    def authenticate(self, assertion):
        logging.warning("entering authenticate function")
        response = requests.post(
            PERSONA_VERIFY_URL,
            data={"assertion": assertion, "audience": settings.DOMAIN}
        )

        logging.warning("got response from persona")
        logging.warning(response.content.decode())

        if response.ok and response.json()["status"] == "okay":
            email = response.json()["email"]
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return User.objects.create(email=email)
        else:
            logger.warning("Persona says no. Json was: {}".format(response.json()))

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None


if __name__ == "__main__":
    pass

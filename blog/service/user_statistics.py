from django.db import models
from datetime import datetime
import uuid
import requests


class StatsSnUser(models.Model):
    """
    Модель регистраций посетителя по UUID и id в социальной сети
    """
    uuid = models.CharField(max_length=40)
    sn_uid = models.IntegerField()
    sn_type = models.CharField(max_length=2)
    created = models.DateTimeField()


class SocialNetworkStats:

    COOKIE_UUID_KEY = 'vslr_uuid'

    def __init__(self, request, response):
        self.request = request
        self.response = response
        self.session = requests.Session()

    @staticmethod
    def generate_uuid():
        return uuid.uuid1()

    def get_uuid_from_cookie(self):
        #cookies = self.session.cookies.get_dict()
        return self.request.COOKIES.get(self.COOKIE_UUID_KEY)

    def set_uuid_to_cookie(self, uuid):
        self.response.set_cookie(self.COOKIE_UUID_KEY, uuid)
        pass

    def get_uuid(self):
        uuid_from_cookie = self.get_uuid_from_cookie()
        if uuid_from_cookie is not None:
            return uuid_from_cookie
        uuid = self.generate_uuid()
        self.set_uuid_to_cookie(uuid)
        return uuid

    def registry(self, sn_uid, sn_type):
        uuid = self.get_uuid()
        StatsSnUser(
            uuid=uuid,
            sn_uid=int(sn_uid),
            sn_type=sn_type,
            created=datetime.now()
        ).save()

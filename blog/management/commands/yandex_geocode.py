from django.core.management.base import BaseCommand
import urllib.request
import json

import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class Command(BaseCommand):
    def handle(self, *args, **options):
        query = Sber1_Train.objects.filter(_lat__isnull=False, _lon__isnull=False, city_name__isnull=True)
        #print(query.query)
        for obj in query.all()[0:10000]:
            city_name = self.get_city_name_by_longlat(obj._lon, obj._lat)
            if city_name is False:
                print(obj._id, '- fail')
                continue
            obj.city_name = city_name
            obj.save()
            print(obj._id, '- OK!')

    @staticmethod
    def get_city_name_by_longlat(longitude, latitude):
        if longitude is None or latitude is None:
            return False
        url = 'https://geocode-maps.yandex.ru/1.x/?format=json&geocode='\
              + str(longitude) \
              + ',' \
              + str(latitude)+'&kind=locality&results=1'
        with urllib.request.urlopen(url) as f:
            data = json.loads(f.read().decode('utf-8'))
            return data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name']

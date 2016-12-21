from django.core.management.base import BaseCommand


class Command(BaseCommand):

    TRELLO_APP_KEY = '54634'

    def add_arguments(self, parser):
        #parser.add_argument('method', nargs='+', type=str)
        #parser.add_argument('user_id', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        #print(options['method'][0])
        #print(type(options['user_id'][0]))
        pass
import vk_api
import psycopg2

conn = psycopg2.connect(database='microblog', user='postgres', password='123', host='localhost')
cur = conn.cursor()


request = vk_api.request('wall.get')
request.set_param('domain', 'just_str')
request.set_param('count', 100)
request.set_param('offset', 0)
request.exec()

items = request.get_response()

#print(items.http_response)

import json
#for i in json.load(open('crawler-user-agents.json')):
for i in json.load(open('c1.json')):
  for match in i['instances']:
    if 'yandex.com' in match:
      print(match)

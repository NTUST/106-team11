import json
import requests
import time as t

class Crawler(object):
    def movie(self):
        self.data = []

        now = t.strftime("%Y-%m-%d")
        theater = "8" #東南亞秀泰
        res = requests.get("https://api.showtimes.com.tw/1/events/listForCorporation/"+theater+"?date="+now+"&limit=2000")
        doc = json.loads(res.text)

        for event in doc['payload']['events']:
            for program in doc['payload']['programs']:
                if(str(event['programId']) == str(program['id'])):
                    name=str(program['name'])
        date=str(event['startedAt'])[5:10]
        hour=int(str(event['startedAt'])[11:13])+8
        min=str(event['startedAt'])[14:16]

        time=''

        if(hour==24):
            hour=0
        if(hour<10):
            time+='0'

        time+=str(hour)
        time+=':'
        time+=min

        for venue in doc['payload']['venues']:
            if(str(event['venueId'])==str(venue['id'])):
                room=str(venue['room'])

        item=''
        item+=name
        item+='='
        item+=room
        item+='='
        item+=date
        item+='='
        item+=time
        self.data.append(item)

        self.data.sort()
        for d in self.data :
            print (d)

        return self.data

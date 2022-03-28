import schedule
import time
import json

def job():
    print(time.strftime("%H:%M:%S"))
    if time.strftime("%H:%M:%S")== '00:00:00':
        print("yay")
        with open("list.json","r") as f:
            json_data = json.loads(f.read())
        
        for player in json_data.keys():
            json_data[player]["energy"]+=1

        if len(json_data) == 0:
            return

        with open("list.json","w") as f:
            new_json = json.dumps(json_data, indent=4)
            f.write(new_json)

schedule.every(1).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
import requests
import json
import pprint
import time
import random
from datetime import datetime
from twilio.rest import Client

<script type='text/javascript' src='config.js'></script>


account_sid = config.MY_KEY
auth_token = config.SECRET_KEY
PROJECT_TOKEN = config.PROJECT_TOKEN
api_key = config.API_KEY

count = 0

while True:

    run_url = "https://www.parsehub.com/api/v2/projects/{0}/run".format(PROJECT_TOKEN)

    # Run the project
    r = requests.post(run_url, data=params)

    j = r.json()
    run_token = j['run_token']

    # Pause and wait for parseHub to gather the data
    time.sleep(120)

    get_run_url = "https://www.parsehub.com/api/v2/runs/{0}".format(run_token)

    # Returns the run object for a given run
    r = requests.get(get_run_url, params=params)

    j = r.json()
    status = j['status']

    # Loops that waits for run to complete before getting the data
    while str(status)!='complete':
        print('Waiting for run to finish')
        time.sleep(120)
        r = requests.get(get_run_url, params=params)
        j = r.json()
        status = j['status']

    data_url = "https://www.parsehub.com/api/v2/runs/{0}/data".format(run_token)

    #Get data for a run
    d = requests.get(data_url, params=params)
    j = d.json()

    # Sleep if empty JSON response
    if d.text=="{\n}":
        print("Empty JSON response. Skipping to next run after sleep.")
        time.sleep(60)
        continue

    count = count+1
    print("Count = {0}".format(count))
    registered = j["Registered"]
    if str(registered)!="Closed":
        print("***************************")
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("Class is open")
        print("***************************")
        # Send the alert SMS
        message = client.messages.create(to="+19092476022", from_="+19096394737", body="Math 229 is now open! Here's a link https://my.usc.edu/")
        # Print out the json
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(d.json())
        print('Sleeping for an hour')
        time.sleep(3600)
    else:
        print("---------------------------")
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("Class is full")
        print("---------------------------")

    # Sleep for 1-2 minutes randomly
    t = random.randint(100,250)
    print("Sleeping for {0} minutes".format(int(t/60)))
    time.sleep(t)

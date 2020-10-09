import logging
import json
import os
import requests
import base64
import datetime
from flask_cors import CORS

from flask import Flask, request, jsonify;

app = Flask(__name__)
CORS(app)
logger = logging.getLogger(__name__)

@app.route('/get-access-token', methods=['POST'])
def get_access_token():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    auth_code = data.get("auth_code")
    email = data.get("email") # may need to change to dummy 

    params = {
        "grant_type" : "authorization_code",
        "code" : "{}".format(auth_code),
        "redirect_uri" : "https://cfg-2020.web.app",
    }
    
    auth = "{}:{}".format(os.environ.get("CLIENT_ID"), os.environ.get("SECRET"))
    auth_encoded = base64.b64encode(auth.encode('ascii')).decode('ascii')
    
    
    headers = {
        "Authorization" : "Basic {}".format(auth_encoded)
    }

    resp = requests.post("https://zoom.us/oauth/token", params=params, headers=headers).json()
    
    return resp

@app.route('/make-recurring-meeting', methods=['POST'])
def make_recurring():
    data = request.get_json()
    access_token = data.get("access_token")
    email = data.get("email")
    headers = {
        "Content-Type" :"application/json",
        "Authorization" : "Bearer {}".format(access_token)
    }

    request_body = {
        "topic": "For JA meeting",
        "type": 3,
        "start_time": "{}".format(datetime.datetime.now()),
        "duration": 60,
        # "schedule_for": "string",
        "timezone": "Asia/Hong_Kong",
        # "password": "string",
        # "agenda": "string",
        "recurrence": {
            "type": 2, #weekly
            "repeat_interval": 2, # every 2 weeks
            "weekly_days": "1", # set to monday
            "end_times": 8, # recur 8 times
        },
        "settings": {
            "host_video": False,
            "participant_video": False,
            "cn_meeting": False,
            "in_meeting": False,
            "join_before_host": False,
            "mute_upon_entry": True,
            "watermark": False,
            "use_pmi": False,
            "approval_type": 0,
            "registration_type": 1,
            "audio": "voip",
            "registrants_email_notification": True
        }
    }

    url = "https://api.zoom.us/v2/users/{}/meetings".format(email)
    resp = requests.post(url, headers=headers).json()

    result = {
        "start_url" :resp.get("start_url"),
        "join_url" : resp.get("join_url")
    }
    return jsonify(result)

@app.route('/get-attendance', methods=['POST'])
def get_attendance():
    data = request.get_json()
    access_token = data.get("access_token")
    meetingId = data.get("meetingId")
    
    params = {
        "page_count" : 30 
    }

    headers = {
        "Content-Type" :"application/json",
        "Authorization" : "Bearer {}".format(access_token)
    }


    url = "https://api.zoom.us/v2/report/meetings/{}/participants".format(meetingId)
    resp = requests.post(url, params=params, headers=headers).json()

    result = {
        "participants" : resp.get("participants")
    }
    return jsonify(result)




if __name__ == "__main__":
    app.run(port=5000, debug=True)



#!/usr/bin/env python3
"""Stage one API design"""

from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)


def get_day():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[datetime.utcnow().weekday()]

def get_utc_time():
    current_time = datetime.utcnow()
    return current_time.strftime("%Y-%m-%dT%H:%M:%SZ")

def get_github():
    repo_url = ""
    file_url = ""
    return f"{repo_url}/{file_url}/"

def validate_utc_time():
    utc_time = datetime.strptime(get_utc_time(), "%Y-%m-%dT%H:%M:%SZ")
    valid_range = timedelta(minutes=2)
    return datetime.utcnow() - valid_range <= utc_time <= datetime.utcnow() + valid_range

@app.route('/api', methods=['GET'])
def get_info():
    slack_name = request.args.get('slack_name')
    track = request.args.get("track")

    if not slack_name or not track:
        return jsonify({"Error": "Missing slack_name or track parameters"})
    if not validate_utc_time():
        return jsonify({"error": "Invalid UTC time"}), 400
    github_file_url = get_github()
    github_repo_url = ""

    response = {
        "slack_name": slack_name,
        "current_day": get_day(),
        "utc_time": get_utc_time(),
        "track": track,
        "github_file_url": github_file_url,
        "github_repo_url": github_repo_url,
        "status_code": 200
    }

if __name__ == "__main__":
    app.run(debug=True)
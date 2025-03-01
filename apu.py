import json
import random
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Remaining API request count
remain_count = 20  

# API for fetching player info
TOPUP_API_URL = 'https://topup.pk/api/auth/player_id_login'
HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36'
}

@app.get("/like")
def like(uid: str):
    """Fetch player info and region."""
    global remain_count

    if not uid.isdigit():
        raise HTTPException(status_code=400, detail="Invalid UID. Please provide a numeric UID.")

    if remain_count <= 0:
        raise HTTPException(status_code=403, detail="No remaining uses available.")

    data = {'app_id': 100067, 'login_id': uid}
    response = requests.post(TOPUP_API_URL, headers=HEADERS, data=json.dumps(data))

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"API request failed. Status: {response.status_code}")

    data_json = response.json()
    nickname = data_json.get('nickname', 'not found')
    region = data_json.get('region', 'not found')

    if nickname == 'not found' or region == 'not found':
        raise HTTPException(status_code=500, detail="Invalid response from API.")

    remain_count -= 1
    return {
        "PLAYER_UID": uid,
        "PLAYER_NICKNAME": nickname,
        "DAY_OF_LIKE": "NULL",
        "DAY_AFTER_LIKE": random.randint(10, 40),
        "PLAYER_REGION": region,
        "MESSAGE": "Join our usage group: https://t.me/Freefirevisit1000"
    }

@app.get("/visit")
def visit(region: str, uid: str):
    """Check visit status."""
    global remain_count

    if remain_count <= 0:
        raise HTTPException(status_code=403, detail="No remaining uses available.")

    api_url = f"https://ariiflexlabs.vercel.app/send_visit?uid={uid}&region={region}"
    response = requests.get(api_url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to send visit request.")

    data = response.json()
    success_message = data.get("Success", "UNKNOWN").upper()

    remain_count -= 1
    return {
        "YOUR_UID": uid,
        "VISIT_STATUS": success_message,
        "MESSAGE": "Join our group: https://t.me/Freefirevisit1000"
    }

@app.get("/remain")
def get_remain():
    """Get remaining request count."""
    return {"remaining_requests": remain_count}

@app.post("/setremain")
def set_remain(new_count: int):
    """Update remaining request count."""
    global remain_count
    remain_count = new_count
    return {"message": f"Remaining uses updated to {remain_count}."}

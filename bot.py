from flask import Flask, render_template, request, jsonify

import requests

import json

import os

from datetime import datetime, timedelta

import sqlite3



app = Flask(__name__, template_folder='templates')



DATABASE = 'free_uids.db'



def init_db():

    conn = sqlite3.connect(DATABASE)

    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS uids

                 (uid TEXT PRIMARY KEY, expiry TEXT)''')

    conn.commit()

    conn.close()



init_db()



def get_db():

    conn = sqlite3.connect(DATABASE)

    return conn



def get_discord_token():
    """Fetch Discord bot token from Pastebin"""
    try:
        response = requests.get('https://pastebin.com/raw/J9YMj5px')
        if response.status_code == 200:
            token = response.text.strip()
            return token
        return None
    except:
        return None



def send_discord_webhook(uid, is_premium=False):

    token = get_discord_token()

    if not token:

        print("Failed to fetch Discord token")

        return False

    

    channel_id = '1482836987873591426'

    url = f'https://discord.com/api/v10/channels/{channel_id}/messages'

    headers = {

        'Authorization': f'Bot {token}',

        'Content-Type': 'application/json'

    }

    if is_premium:

        title = "🚀 PREMIUM ACCESS GRANTED"

        time_value = "Custom"  # Since premium has variable days

    else:

        title = "🚀 FREE ACCESS GRANTED"

        time_value = "2 Days"

    

    embed = {

        "title": title,

        "color": 0x00FF00,

        "fields": [

            {"name": "👤 UID", "value": f"`{uid}`", "inline": True},

            {"name": "⏳ Time", "value": f"`{time_value}`", "inline": True},

            {"name": "📅 Status", "value": "✅ Successfully Added", "inline": False}

        ]

    }

    

    data = {"embeds": [embed]}

    requests.post(url, headers=headers, json=data)



def check_pastebin():

    try:

        response = requests.get('https://pastebin.com/raw/jj1pZfNu')

        if response.status_code == 200:

            content = response.text.strip().upper()

            return 'ON' in content

        return False

    except:

        return False



@app.route('/')

def home():

    if check_pastebin():

        return render_template('Free UID ADD site.html')

    else:

        return render_template('Free Uid Disable.html')



@app.route('/free_add', methods=['POST'])

def free_add():

    if not check_pastebin():

        return jsonify({'success': False, 'message': 'System offline'})

    

    uid = request.form.get('uid')

    if not uid:

        return jsonify({'success': False, 'message': 'UID required'})

    

    days = 2  # Free is 2 days

    try:

        response = requests.get(f'http://46.250.239.109:6020/uid?add={uid}&days={days}')

        if response.status_code == 200:

            # Store in db

            expiry = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')

            conn = get_db()

            c = conn.cursor()

            c.execute('INSERT OR REPLACE INTO uids (uid, expiry) VALUES (?, ?)', (uid, expiry))

            conn.commit()

            conn.close()

            send_discord_webhook(uid, is_premium=False)

            return jsonify({'success': True, 'message': 'UID added for 2 days'})

        else:

            return jsonify({'success': False, 'message': 'Failed to add UID'})

    except Exception as e:

        return jsonify({'success': False, 'message': str(e)})



@app.route('/health')

def health():

    return jsonify({"status": "ok"})



if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5001, debug=True)



if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5001, debug=True)
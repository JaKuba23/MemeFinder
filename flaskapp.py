#!/bin/python3

from flask import Flask, render_template, jsonify
import requests
import json

app = Flask(__name__)

def get_meme():
    """
    Fetch a random meme from meme-api.com.
    Returns:
        tuple: (meme image url, subreddit name)
    """
    url = "https://meme-api.com/gimme"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        meme_large = data.get("preview", [data.get("url")])[-2] if "preview" in data else data.get("url")
        subreddit = data.get("subreddit", "unknown")
        return meme_large, subreddit
    except Exception as e:
        #Fallback image and subreddit if API fails
        return "/static/fallback.png", "API error"

@app.route('/')
def index():
    """
    Main page: shows a random meme.
    """
    meme_pic, subreddit = get_meme()
    return render_template("meme_index.html", meme_pic=meme_pic, subreddit=subreddit)

@app.route('/api')
def meme_api():
    meme_pic, subreddit = get_meme()
    return jsonify({'meme_pic': meme_pic, 'subreddit': subreddit})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

import requests
import json
import re


url = "https://api.play.ht/api/v2/cloned-voices"

headers = {
    'AUTHORIZATION': '278485edc78846328dd3dd883d5e1edb',
    'X-USER-ID': 'TtmGFJ2K5NX4xgEd7bprs7XDrZ33',
    'accept': 'text/event-stream',
    'content-type': 'application/json'
}

response = requests.get(url, headers=headers)

print(response.text)

















# kanye_id = 's3://voice-cloning-zero-shot/60ec47bc-6e13-4684-9340-a5e6a1d53f88/kanye-west/manifest.json'


# url = "https://api.play.ht/api/v2/tts"

# payload = {
#     "text": """Let's get lost tonight
# You could be my black Kate Moss tonight """"",
#     "voice": kanye_id,
#     "output_format": "mp3",
#     "voice_engine": "PlayHT2.0"
# }
# headers = {
#     'AUTHORIZATION': '278485edc78846328dd3dd883d5e1edb',
#     'X-USER-ID': 'TtmGFJ2K5NX4xgEd7bprs7XDrZ33',
#     "accept": "text/event-stream",
#     "content-type": "application/json",
#     "Content-Location": "/celeb_audio"
# }

# response = requests.post(url, json=payload, headers=headers)

# response_text = response.text

# # Regular expression to find the URL
# match = re.search(r'"url":"([^"]+)"', response_text)
# if match:
#     mp3_url = match.group(1)
#     print(mp3_url)
# else:
#     print("URL not found in the response.")
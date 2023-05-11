import re
import requests
import json
import isodate

def get_video_duration(video_id):
    """
    Returns the duration of a YouTube video given its video ID.
    """
    api_key = 'AIzaSyDwwnyJr7tboh0Ofo9rl8v_uRqeizc5OtM'
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=contentDetails'
    response = requests.get(url)
    data = json.loads(response.text)
    duration = data['items'][0]['contentDetails']['duration']
    duration_str = duration
    duration = isodate.parse_duration(duration_str)
    total_seconds = duration.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)


    return minutes, seconds



total_minutes = 0
total_seconds = 0
with open('links.txt','r') as f:
    for line in f:


        # Extract the video ID from the URL
        video_id = re.findall(r'embed/([\w-]+)', line)[0]

        # Get the duration of the video
        minutes, seconds = get_video_duration(video_id)

        total_minutes+=minutes
        total_seconds+=seconds

minutes = total_seconds // 60
total_seconds = total_seconds % 60

total_minutes += minutes

hours = total_minutes // 60

total_minutes = total_minutes % 60

print(f'The total duration of this course is {hours} hours, {total_minutes} minutes, and {total_seconds} seconds.')




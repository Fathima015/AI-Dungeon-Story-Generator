import os
from datetime import datetime

def save_story(story, genre, index):
    if not os.path.exists("stories"):
        os.makedirs("stories")

    filename = f"stories/story_{genre.lower()}_{datetime.now().strftime('%H%M%S')}_{index+1}.txt"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(story)
    return filename

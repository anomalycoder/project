import json

def load_course_content(path="app/data/content.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_discourse_posts(path="app/data/discourse.json"):
    with open(path, "r", encoding="utf-8") as f:
        posts = json.load(f)
    return "\n\n".join([post.get("title", "") + "\n" + post.get("content", "") for post in posts])

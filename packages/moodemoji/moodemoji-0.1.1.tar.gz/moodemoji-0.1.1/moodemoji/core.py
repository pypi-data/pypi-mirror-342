# moodemoji/core.py

MOOD_EMOJIS = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "excited": "🤩",
    "tired": "😴",
    "love": "❤️",
    "confused": "😕"
}

def mood_to_emoji(mood: str) -> str:
    return MOOD_EMOJIS.get(mood.lower(), "🤔")  # Default if not found

def list_moods() -> list:
    return list(MOOD_EMOJIS.keys())

class MoodInterpreter:
    def __init__(self, default_mood: str = "happy"):
        self.default_mood = default_mood.lower()

    def get_emoji(self, mood: str = None) -> str:
        mood_key = (mood or self.default_mood).lower()
        return MOOD_EMOJIS.get(mood_key, "🤔")

    def set_mood(self, mood: str):
        self.default_mood = mood.lower()

    def get_supported_moods(self) -> list:
        return list(MOOD_EMOJIS.keys())

# Keep your function-based API too if you want
def mood_to_emoji(mood: str) -> str:
    return MOOD_EMOJIS.get(mood.lower(), "🤔")

def list_moods() -> list:
    return list(MOOD_EMOJIS.keys())
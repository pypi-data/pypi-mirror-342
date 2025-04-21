# tests/test_core.py

from moodemoji import mood_to_emoji, list_moods, MoodInterpreter

def test_mood_to_emoji():
    assert mood_to_emoji("happy") == "😊"
    assert mood_to_emoji("unknown") == "🤔"

def test_list_moods():
    assert "happy" in list_moods()

def test_mood_interpreter_class():
    mi = MoodInterpreter("sad")
    assert mi.get_emoji() == "😢"
    assert mi.get_emoji("excited") == "🤩"
    mi.set_mood("tired")
    assert mi.get_emoji() == "😴"
    assert "love" in mi.get_supported_moods()

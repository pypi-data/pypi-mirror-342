import pytest
from telugu_stopwords import tsw, rmtsw

def test_get_stopwords_telugu():
    ts = tsw()
    stopwords = ts.get_stopwords(script="telugu")
    assert "మరియు" in stopwords
    assert len(stopwords) > 0

def test_get_stopwords_english():
    ts = tsw()
    stopwords = ts.get_stopwords(script="english")
    assert "mariyu" in stopwords
    assert len(stopwords) > 0

def test_remove_stopwords():
    text = "నేను ఈ రోజు చాలా సంతోషంగా ఉన్నాను"
    cleaned = rmtsw(text, script="telugu")
    assert "నేను" not in cleaned
    assert "సంతోషంగా" in cleaned

def test_add_stopwords():
    ts = tsw()
    ts.add_stopwords(["నీవు"], script="telugu")
    assert "నీవు" in ts.get_stopwords(script="telugu")
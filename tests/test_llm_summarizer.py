import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from llm_summarizer import summarize_news

def test_summarize_news():
    # Test with a mock response or empty key handling
    summary = summarize_news("RBI holds interest rates steady.")
    assert isinstance(summary, str)
    assert len(summary) > 0

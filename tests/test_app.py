import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app import get_app_title

def test_app_title():
    assert get_app_title() == "NSE Market Assistant"

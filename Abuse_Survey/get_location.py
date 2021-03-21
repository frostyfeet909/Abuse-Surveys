# Provides the absolute file path to Abuse_Survey
from os.path import dirname, realpath


def get_location():
    """
    Returns the absolute file path to Abuse_Survey
    """
    return dirname(realpath(__file__))

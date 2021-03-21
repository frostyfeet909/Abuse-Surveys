import unittest
from unittest.mock import patch
from sys import path


def run():
    path.insert(1, './')
    import Abuse_Survey
    Abuse_Survey.abuse_survey_monkey(
        1, 2, 'XQ6J57B', protections=False, verbosity=0)


if __name__ == '__main__':
    run()

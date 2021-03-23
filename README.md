# Abuse Surveys
https://youtu.be/jeIkZlzENbY Love u Ewan (^з^)-☆Chu!!\
A set of OOP python programs to abuse online surveys.\
Currently randomly answers survey monkey questions with random sentances, mitigates the browser protection and is multithreaded for performance.

## Installation

1. Install the latest stable version of [python3](https://www.python.org/downloads/).
2. Install the remaining packages in requirements and setup the file strucutre by running `setup.py`:

   ```bash
   python setup.py
   ```

3. Install the latest stable version of the selenium [chrome webdriver](https://chromedriver.chromium.org/downloads) and place it in `Abuse_Survey/webdrivers`.

## Usage

```python
import Abuse_Survey
Abuse_Survey.abuse_survey_monkey(2, 2, 'XQ6J57B')
# Start abuse on survey monkey with two processes, repeating twice.
```

```python
import Abuse_Survey
Abuse_Survey.run()
# Start a text UI for the same thing
```

## License

me no know

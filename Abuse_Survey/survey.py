# Program to abuse surveys - Random Checkboxes + Random Written answers
from threading import Lock, Thread
from os.path import join, isfile, dirname, realpath
from time import time
from json import load as json_load
from json import dump as json_dump


lock_file = Lock()


class Survey(Thread):
    """
    Abstract base class for survey destorying
    """

    def __init__(self, survey, ID, repeats, protect=False, verbose=1):
        """
            survey - Survey webaddress : String
            ID - UUID : Integer
            repeats - No. of survey rpeats : Integer > 0
            protect - Does survey have protection enabled : Boolean
            verbose - How verbose do you want to be (format: 0-2) : Integer
        """
        Thread.__init__(self)  # Threaded
        self.ID = ID
        self.survey_type = None
        self.protect = protect
        self.survey = survey
        self.choices = {}
        self.repeats = repeats
        self.iteration = 1
        self.driver = None  # Selenium webdriver object
        self.active = False
        self.verbose = verbose
        self.start_time = time()

    def setup(self):
        pass

    def run(self):
        pass

    def add_choice(self, question_ID, element_ID):
        """
        Add the selected answer to the respective question in the choices nested Dict
            question_ID - The respective question ID
            element_ID - The element ID for the chosen answer
            question_ID,element_ID -> 
        """
        if question_ID not in self.choices.keys():
            self.choices[question_ID] = {}
        if element_ID not in self.choices[question_ID].keys():
            self.choices[question_ID][element_ID] = 1
        else:
            self.choices[question_ID][element_ID] += 1

    def save_choices(self):
        """
        Save the survey choices
        """
        if self.verbose >= 2:
            print("[*]%i: Saved" % self.ID)

        base_dir = dirname(realpath(__file__))
        file_loc = join(base_dir,
                        "results", self.survey_type, self.survey + ".json")

        # Open and save the results - One thread access at a time
        if not isfile(file_loc):
            data = {}
        else:
            lock_file.acquire()
            with open(file_loc, "r") as file:
                data = json_load(file)
            lock_file.release()

        data_keys = data.keys()

        # For question in choices
        for question in self.choices.keys():
            if question not in data_keys:
                data[question] = {}

            data_keys_keys = data[question].keys()  # Data answers

            # For answer to question
            for answer in self.choices[question].keys():
                if answer not in data_keys_keys:
                    data[question][answer] = 0

                data[question][answer] += self.choices[question][answer]

        lock_file.acquire()
        with open(file_loc, "w") as file:
            json_dump(data, file)
        lock_file.release()

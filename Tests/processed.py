# Program to abuse surveys - Random Checkboxes + Random Written answers
import re
from multiprocessing import Process, Lock
from time import sleep, time
from random import choice, randint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from get_sentence import get_sentence
from Time_Lock import Time_Lock


# Constants
SLEEP_TIME = 2
CHROME_DRIVER_PATH = 'C:/Users/algie/Documents/chrome/chromedriver'
# verbosity = 1  # Level of verbosity (format: 0-2)
lock_file = Lock()


class Survey(Process):
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
        Process.__init__(self)  # Threaded
        self.ID = ID
        self.protect = protect
        self.start_time = time()
        self.survey = survey
        self.choices = []
        self.repeats = repeats
        self.iteration = 1
        self.driver = None  # Selenium webdriver object
        self.active = False
        self.verbose = verbose

    def setup(self):
        pass

    def run(self):
        pass


class Survey_Monkey(Survey):
    """
    Class to abuse SurveyMonkey
    """

    def __init__(self, survey, ID, repeats, protect=False, verbose=1):
        """
            survey - Survey webaddress : String
            ID - UUID : Integer
            repeats - No. of survey rpeats : Integer > 0
            protect - Does survey have protection enabled : Boolean
            verbose - How verbose do you want to be (format: 0-2) : Integer
        """
        super().__init__(survey, ID, repeats, protect, verbose)
        self.lock = Time_Lock()

    def setup(self):
        """
        Setup selenium webdriver
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("-incognito")

        try:
            # Setup and connect to survey
            self.driver = webdriver.Chrome(
                executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options)
            self.driver.get(
                'https://www.surveymonkey.co.uk/r/%s' % self.survey)
            if self.verbose <= 0:
                self.driver.minimize_window()
            self.active = True
            if self.verbose >= 2:
                print("[*]%i: Driver setup" % self.ID)

        except:
            self.active = False
            if self.verbose >= 1:
                print("[!!]%i: Driver couldn't start" % self.ID)

    def refresh(self):
        """
        Refresh active webdriver
        """
        try:
            self.driver.get(
                'https://www.surveymonkey.co.uk/r/%s' % self.survey)
            # self.driver.minimize_window()
            self.active = True
            if self.verbose >= 2:
                print("[*]%i: Driver refreshed" % self.ID)

        except:
            self.active = False
            if self.verbose >= 1:
                print("[!!]%i: Driver couldn't refresh" % self.ID)

    def run(self):
        """
        Setup webdriver and go through logic to answering a survey
        """
        self.setup()
        while self.active:
            time_initial = time()
            question_IDs = self.find_question_IDs()

            self.clear_buttons()

            # Answer all questions on page
            if question_IDs is not None:
                for question_ID in question_IDs:
                    self.answer(question_ID)
                    self.clear_buttons()
            if self.verbose >= 2:
                print("[*]%i: Questions answered" % self.ID)

            # Try to go to next page otherwise finish the survey
            if not self.next_page():
                ended = self.end_survey()
                time_elapsed = str(round(time()-time_initial))

                # If successful save results
                if ended:
                    self.save_choices(time_elapsed)

                if self.verbose >= 1:
                    print("[*]%i: Round %i has Finished it took: %s seconds" %
                          (self.ID, self.iteration, time_elapsed))

                self.restart()
            else:
                if self.verbose >= 2:
                    print("[*]%i: Next page" % self.ID)

    def clear_buttons(self):
        """
        Tries to confirm all buttons on the current page
            -> Bool
        """
        while True:
            button_cleared = self.confirm_button()
            if not button_cleared:
                return True

    def find_question_IDs(self):
        """
        Find the IDs of all questions on the current page
            question_IDs - List of question IDs on the current page : List
            -> question_IDs
        """
        # Get current page html
        self.lock.acquire()
        html = self.driver.page_source
        self.lock.release()

        # Find question IDs in html
        pattern = 'data-question-id="([0-9]+)"'
        prog = re.compile(pattern)
        question_IDs = prog.findall(html)

        if len(question_IDs) == 0:
            if self.verbose >= 1:
                print("[!]%i: Questions not found" % self.ID)
            return None

        if self.verbose >= 2:
            print("[*]%i: Question IDs gathered" % self.ID)
        return question_IDs

    def find_answers(self, question_ID):
        """
        Find the element IDs relating to the question ID
            question_ID - The ID for the current question : String
            answers - Element IDs relating to the question (format: question_ID+'_'+element_ID) : List
            question_ID -> answers
        """
        # Get current page html
        self.lock.acquire()
        html = self.driver.page_source
        self.lock.release()

        # Find element IDs in html
        pattern = 'id="(' + question_ID + '_?[0-9]*[a-z]*)"'
        prog = re.compile(pattern)
        answers = prog.findall(html)

        if len(answers) == 0:
            if self.verbose >= 1:
                print("[!]%i: Answers not found for %s" %
                      (self.ID, question_ID))
            answers = None

        if self.verbose >= 2:
            print("[*]%i: Answer IDs gathered for %s" % (self.ID, question_ID))
        return answers

    def answer(self, question_ID):
        """
        Attempts to identify the regarded question type and answer it by referring it to the correct subroutine
            question_ID - The ID for the current question : String
            question_ID -> Boolean
        """
        if self.verbose >= 2:
            print("[*]%i: Finding an answer" % self.ID)
        answer_IDs = self.find_answers(question_ID)

        # question_ID is located a answer_IDs[0], some may be referenced as elements (only if it is the only answer)
        if len(answer_IDs) > 1:
            answer_IDs.pop(0)

        # Try to get the first answer element
        try:
            answer = self.driver.find_element_by_id(answer_IDs[0])
        except NoSuchElementException:
            return True
        except:
            if self.verbose >= 1:
                print("[!]%i: Something went wrong" % self.ID)
            return False

        # Identify the question type
        element_type = answer.get_attribute('class')
        if element_type.startswith("checkbox-button"):
            return self.do_checkbox(answer_IDs)
        elif element_type.startswith("radio-button"):
            return self.do_multichoice(answer_IDs)
        elif element_type.startswith("textarea"):
            return self.do_comment(answer)
        else:
            if self.verbose >= 1:
                print("[!]%i: Unknown question type" % self.ID)
            return False

    def do_checkbox(self, element_IDs):
        """
        Attempts to answer the checkbox
            element_IDs - A list of all element IDs for the current question : List
            element_IDs -> Boolean
        """
        if self.verbose >= 2:
            print("[*]%i: Doing CheckBox" % self.ID)
        checkbox = []

        # Identify if there is an 'other' textbox
        if "_other" in element_IDs[-1]:
            other_ID = element_IDs.pop()
        else:
            other_ID = None

        # Weighted randomised checkboxs
        for _ in range(0, len(element_IDs)):
            if randint(0, len(element_IDs)-1) == 0:
                checkbox.append(True)
            else:
                checkbox.append(False)

        # Check at least one checkbox is checked
        if True not in checkbox:
            i = randint(0, len(element_IDs)-1)
            checkbox[i] = True

        # Go through all elements and check them based on checkbox
        for element_ID_i in range(0, len(element_IDs)):
            if checkbox[element_ID_i]:
                element_ID = element_IDs[element_ID_i]
                element = self.driver.find_element_by_id(element_ID)
                self.lock.acquire()
                element.click()
                self.lock.release()
                self.choices.append(element_ID)

                # If 'other' is checked answer the textbox
                if element_ID_i == len(element_IDs)-1 and other_ID is not None:
                    element = self.driver.find_element_by_id(other_ID)
                    self.lock.acquire()
                    element.send_keys(get_sentence())
                    self.lock.release()

        if self.verbose >= 2:
            print("[*]%i: CheckBox answered" % self.ID)
        return True

    def do_multichoice(self, element_IDs):
        """
        Attempts to answer the multiple choice
            element_IDs - A list of all element IDs for the current question : List
            element_IDs -> Boolean
        """
        if self.verbose >= 2:
            print("[*]%i: Doing MultiChoice" % self.ID)

        # Identify if there is an 'other' textbox
        if "_other" in element_IDs[-1]:
            other_ID = element_IDs.pop()
        else:
            other_ID = None

        # Select a random multi-choice
        element_ID_i = randint(0, len(element_IDs)-1)
        element_ID = element_IDs[element_ID_i]
        element = self.driver.find_element_by_id(element_ID)
        element.click()
        self.lock.acquire()
        self.choices.append(element_ID)
        self.lock.release()

        # If 'other' is checked answer the textbox
        if element_ID_i == len(element_IDs)-1 and other_ID is not None:
            element = self.driver.find_element_by_id(other_ID)
            self.lock.acquire()
            element.send_keys(get_sentence())
            self.lock.release()

        if self.verbose >= 2:
            print("[*]%i: MultiChoice annswered" % self.ID)
        return True

    def do_comment(self, element):
        """
        Attempts to answer the comment box
            element - The comment box element : selenium object
            element -> Boolean
        """
        if self.verbose >= 2:
            print("[*]%i: Doing CommentBox" % self.ID)
        self.lock.acquire()
        element.send_keys(get_sentence())
        self.lock.release()

        if self.verbose >= 2:
            print("[*]%i: CommentBox answered" % self.ID)
        return True

    def click_button(self, text_list):
        """
        Goes through the text_list, trying to click any available buttons with the same name
            text_list - A list of possible button names : List
            text_list -> Boolean
        """
        for text in text_list:
            # Try to acquire the button element
            try:
                button = self.driver.find_element_by_xpath(
                    "//button[contains(text(), ' %s')]" % text)
            except NoSuchElementException:
                pass
            else:
                # Try to click the button element
                try:
                    self.lock.acquire()
                    button.click()
                    self.lock.release()
                except ElementNotInteractableException:
                    pass
                else:
                    if self.verbose >= 2:
                        print("[*]%i: %s button clicked" % (self.ID, text))
                    return True

        if self.verbose >= 2:
            print("[!]%i: Button not found" % self.ID)
        return False

    def confirm_button(self):
        """
        Try to click a confirm button
            -> Boolean
        """
        text_list = set(["ok", "OK", "Ok", "Confirm", "confirm", "CONFIRM"])
        return self.click_button(text_list)

    def next_page(self):
        """
        Try to click a next page button
            -> Boolean
        """
        text_list = set(["Next", "nxt", "next", "NEXT"])
        return self.click_button(text_list)

    def end_survey(self):
        """
        Try to click a done button
            -> Boolean
        """
        text_list = set(["Done", "DONE", "done"])
        button_clicked = self.click_button(text_list)

        if not button_clicked:
            if self.verbose >= 1:
                print("[!!]%i: No done button" % self.ID)

        return button_clicked

    def shutdown(self):
        """
        Shutdown the selenium webdriver
        """
        if self.verbose >= 2:
            print("[*]%i: Shutdown" % self.ID)
        self.driver.quit()
        self.active = False

    def save_choices(self, time_elapsed):
        """
        Save the survey choices
            time_elapsed - Time taken to complete the survey (format: 2dp seconds) : String
        """
        if self.verbose >= 2:
            print("[*]%i: Saved" % self.ID)
        # ID: time choice1 choice2 ...
        text = str(self.ID) + ": " + time_elapsed + \
            " " + " ".join(self.choices)

        # Open and save the results - One thread access at a time
        lock_file.acquire()
        with open("results_%s.txt" % self.survey, "a") as file:
            file.write(text)
            file.write("\n")
        lock_file.release()

    def restart(self):
        """
        Restart the webdriver based on the type of protections
        """
        if self.iteration < self.repeats:
            if self.verbose >= 2:
                print("[*]%i: Restarting" % self.ID)
            self.iteration += 1
            self.choices = []

            # No protections refresh otherwise full restart
            if not self.protect:
                self.refresh()
            else:
                self.shutdown()
                self.setup()

        else:
            self.shutdown()
            elapsed = str(round((time()-self.start_time)/60))
            if self.verbose >= 1:
                print("[*]%i: Monkey destroyed, took: %s minutes" %
                      (self.ID, elapsed))


def run(process_no, repeat_no, survey, verbosity=1, protections=False):
    """
    Run the processes
        process_no - Number of processes/windows
        repeat_no - Number of times one process should run
        survey - Webaddress for the survey
        verbosity - Level of verbosity
        protections - Does the survey have protections
    """
    processes = []

    for i in range(1, process_no+1):
        processes.append(Survey_Monkey(
            survey, i, repeat_no, protect=protections, verbose=verbosity))

    for i in range(0, process_no):
        processes[i].start()

    for i in range(0, process_no):
        processes[i].join()

    if self.verbose >= 1:
        print("[*] Monkey has been ruined")


if __name__ == "__main__":
    run(1, 1, 'XQ6J57B', verbosity=0)
    print("Finished 1")
    run(2, 2, 'XQ6J57B', verbosity=0)
    print("Finished 2")

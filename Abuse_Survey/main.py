# Main program to build and run classes

def abuse_survey_monkey(process_no, repeat_no, survey, verbosity=1, protections=False):
    """
    Multithreads/process survey monkey abuse
        process_no - Number of processes/windows : Integer > 0
        repeat_no - Number of times one process should run : Integer > 0
        survey - Webaddress for the survey : String
        verbosity - Level of verbosity : Integer (0-2)
        protections - Does the survey have protections : Boolean
    """
    from Abuse_Survey import survey_monkey

    processes = []

    for i in range(1, process_no+1):
        processes.append(survey_monkey.Survey_Monkey(
            survey, i, repeat_no, protect=protections, verbose=verbosity))

    for i in range(0, process_no):
        processes[i].start()

    for i in range(0, process_no):
        processes[i].join()

    if verbosity >= 1:
        print("[*] Monkey has been ruined")


def run():
    """
    Text UI
    """
    choice = ""

    while choice.lower() != ("exit" or "q" or "quit"):
        print("Pick a survey provider:")
        print("[1] - Survey Monkey")
        choice = input(">> ")
        print("\n")

        if choice == "1":
            process_no = input("process_no: ")
            repeat_no = input("repeat_no: ")
            survey = input("survey: ")
            print("\n")
            abuse_survey_monkey(process_no, repeat_no, survey)
            break
        else:
            print("Try again!")
            print("\n")

    print("Bye!")


if __name__ == "__main__":
    run()

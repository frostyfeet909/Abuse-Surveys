from os.path import join, isfile, isdir, dirname, realpath
from os import mkdir
from subprocess import call
from sys import executable
from importlib import import_module


def get_location():
    """
    Returns the absolute file path
    """
    return dirname(realpath(__file__))


def make_dirs():
    modules = ['survey_monkey']
    location = join(get_location(), "Abuse_Survey")

    if not isdir(location):
        print("Abuse_survey not found")
        return False

    results = join(location, "results")
    if not isdir(results):
        mkdir(results)
        print("Made: %s" % results)

    for module in modules:
        result = join(location, "results", module)
        if not isdir(result):
            mkdir(result)
            print("Made: %s" % result)

    webdrivers = join(location, "webdrivers")
    if not isdir(webdrivers):
        mkdir(webdrivers)
        print("Made: %s" % webdrivers)

    print("Structure done")
    return True


def install_modules():
    try:
        with open("requirements.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("requirements.txt not found")
        return False

    for line in lines:
        line = line.strip()
        print("Importing: %s" % line)

        try:
            import_module(line)
        except ImportError:
            print("Attempting to install: %s" % line)
            try:
                call([executable, "-m", "pip", "install", line])
            except:
                print("Could not install: %s" % line)
            else:
                print("Installed: %s" % line)


def run():
    make_dirs()
    install_modules()


if "__main__" == __name__:
    run()

"""
Chatbot Autograder - Updated 11/05/2017
Please use this file to test your Chatbot class.

https://www.python.org/dev/peps/pep-0008/
function_names and variable:
lowercase with words separated by underscores as necessary to improve readability.
Class names should normally use the CapWords convention (yea!).
"Private" viariables start with _
Spaces are the preferred indentation method.
80 characters per line - Is this the 1980's?
I have not used a line printer since college

Usage: chatbotTester.py -f faq -l <log filename>
"""


import sys, getopt, json
import Chatbot


def ChatbotAutograder(script_filename, faq_filename, log_filename):
    print(__doc__.split('.')[0])

    try:
        with open(script_filename, encoding='utf-8') as json_data:
            autograder_test_script_as_list_of_dicts = json.load(json_data)
    except:
            print("Failure opening AutograderScript json file")
            return 1

    try:
        chatbot = Chatbot.Chatbot(faq_filename)
    except FileNotFoundError:
        print("Could not find FAQ.")
        return 1

    if log_filename:
        print("Loggin to file: "+log_filename)
        log_file = open(log_filename, "w")

    score = 0.0
    correct = 0
    wrong = 0
    idk = 0

    for qa_dict in autograder_test_script_as_list_of_dicts:
        tr = chatbot.input_output(qa_dict["questions"][0])
        try:
            response = tr.split('\n')[0]
        except:
            print("WHUT")

        # response = tr.split('\n')[0]
        action = "0.0"
        if "replace" in qa_dict:
            replace = qa_dict["replace"]
        else:
            replace = ""

        if response == qa_dict["response"]:
            score += 1.0
            correct += 1
            action = "1.0"
            chatbot.user_feedback(True, replace)
        else:
            score -= 0.5
            action = "-0.5"
            wrong += 1
            chatbot.user_feedback(False, replace)

        if log_filename:
            log_file.write("\nTest Question: "+qa_dict["questions"][0])
            log_file.write("\nAgent Response: "+response)
            log_file.write("\nTest Answer: "+qa_dict["response"])
            log_file.write("\nTest Replace: "+replace)
            log_file.write("\nAction: "+action)
            log_file.write("\nWrong: " + str(wrong))
            log_file.write("\nCorrect: " + str(correct))
            log_file.write("\n")

    log_file.close()
    print("Score:", score)


def main(argv):
    # https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    faq_filename = ''
    log_filename = ''
    script_filename = ''
    try:
        opts, args = getopt.getopt(argv, "hs:f:l:", ["script=", "faq=", "log="])
    except getopt.GetoptError:
        print("Usage: chatbotAutograder.py -s script -f faq -l <log filename>")
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print("Usage: chatbotAutograder.py -s script -f faq -l <log filename>")
            sys.exit()
        elif opt in ("-f", "--faq"):
            faq_filename = arg
        elif opt in ("-l", "--log"):
            log_filename = arg
        elif opt in ("-s", "--script"):
            script_filename = arg

    if not faq_filename:
        print("Usage: chatbotAutograder.py -s script -f faq -l <log filename>")
        sys.exit(2)

    if not script_filename:
        print("Usage: chatbotAutograder.py -s script -f faq -l <log filename>")
        sys.exit(3)

    return ChatbotAutograder(script_filename, faq_filename, log_filename)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
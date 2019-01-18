#
# This little game use the SpeechRecognition package 3.8.1 and PyAudio to use the
# computer's microphones as input device to receive voice sounds, recognize them and
# make the game of guessing 5 random words from a pre-defined list with a number o 3 attempts.
# The words in sound must match with the list of predefined words in order to win the game.
#
#   Written by Jaime Gutierrez in 24/08/2018


import random
import time

import speech_recognition as SpeechR

def recognize_speech_from_mic(recognizer,microphone):
    """
    @Transcribe speech to recorded from microphone

    Returns a dictionary with three keys:

    "Success": Boolean value indicating if the API was succesful.
    "Error" : 'None' if no error, otherwise an error message will appear.
    "Transcription" 'None' if speech could not be transcribed
    """

    #Check that recognizer and microphone arguments are appropiate type
    if not isinstance(recognizer,SpeechR.Recognizer):
        raise TypeError("Warning: 'recognizer' must be a 'Recognizer' instance.")

    if not isinstance(microphone,SpeechR.Microphone):
        raise TypeError("Warning: 'microphone' must be 'Microphone' instance.")

    #   Adjust the recognizer sensitivity to ambient noise and record audio
    #   from the microphone.
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    #   Set up the response object
    response = {
        ""
        "success" : True,
        "error" : None,
        "transcription" : None
    }

    #   Try recognizing the speech in the recording
    #   if a RequestError or UnknowValueError exception is caught,
    #       update the response object accordingly

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except SpeechR.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except SpeechR.UnknownValueError:
        #  Speech was untelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__" :
    #   Set the list of words, maxnumber of tries, and prompt limit

    List_words = ["berry", "pine", "damson", "raspberry","oak"]
    Num_tries = 3
    Prompt_limit = 5

    #   Create recognizers and mic instances
    recognizer = SpeechR.Recognizer()
    microphone = SpeechR.Microphone()

    # Get a random word from the list
    word = random.choice(List_words)

    # Make format to the instructions string

    instructions = (

        "Welcome to the wonderful game of guessing your favorite fruit! \n"
        "These are the fruits that are coming to my electronic mind right now:\n"
        "{words}\n"
        "You have {n} attempts to guess which one is.\n"
        "Have fun!\n"
    ).format(words = ', '.join(List_words), n = Num_tries)

    # Show instructions and wait 3 seconds before starting the game

    print(instructions)
    time.sleep(3)

    for i in range (Num_tries):
        # Get the guess from the user.
        #   Transciption -> Break out the loop and continue
        #   No transcription and API request failed -> break loop and continue
        #   If API succed but no transcription -> Re-prompt the user to say their guess again. Repeat to fill
        #   'Prompt_limit' times.

        for j in range (Prompt_limit):
            print('Guess {}. Go ahead, speak!'.format(i+1))
            guess = recognize_speech_from_mic(recognizer,microphone)
            if guess ["transcription"]:
                break
            if not guess ["success"]:
                break
            print("I din't catch that. Could you speak a bit louder, please?\n")

        #   If an error occurred, stop the game.
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        #Show the user the transcription
        print(" You said: {}".format(guess["transcription"]))

        #   Determine if guess is correct and if any attempts remain
        Guess_correct = guess["transcription"].lower() == word.lower()
        more_tries = i < Num_tries - 1

        # Determine if the user has won the game
        #   if not, repeat the loop if there are still more attempts
        #   if no attempts are left, is game over.
        if Guess_correct:
            print("Correct! You win, congratulations!".format(word))
            break
        elif more_tries:
            print("Wrong! Try again. \n ")
        else:
            print("How bad, I was thinking of '{}'.\n".format(word))
            print("Game over.")
            break


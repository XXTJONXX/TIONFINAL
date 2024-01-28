import speech_recognition as sr
class Speechrecognition:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.UP = ["up", "above", "aloft", "elevated", "skyward", "upward", "overhead", "high", "ascendant", "onward",
                   "upstairs", "cup", "pup", "sup", "cusp", "pup", "hiccough", "kup", "pup", "rup", "thrup", "tup",
                   "yup", ]  # generated with chatgpt
        self.DOWN = ["down", "descend", "lower", "drop", "decline", "descending", "sink", "fall", "town", "brown",
                     "clown", "frown", "crown", "gown", "hound", "pound", "round", "sound", "bound",
                     "wound"]  # generated with chatgpt, evaluated by me
        self.RIGHT = ["right", "east", "eastward", "starboard", "light", "fight", "bite", "sight", "knight", "height",
                      "might", "tight", "write", "bright"]  # generated with chatgpt, evaluated by me
        self.LEFT = ["left", "west", "cleft", "bereft", "theft", "heft", "deft", "craft", "lefty", "weft", "shaft",
                     "thrift"]  # generated with chatgpt, evaluated by me



    def recognize_speech(self):
        print("Speech recognition activated, wait one second ")
        with self.microphone as listen:
            self.recognizer.adjust_for_ambient_noise(listen)
            print("Say something:")
            audio = self.recognizer.listen(listen, timeout=2, phrase_time_limit=5)  # Adjust timeout as needed
        try:
            speech = self.recognizer.recognize_google(audio)
            print("You said:", speech)

            words_list = speech.split()
            print(words_list)
            action_list = []
            for word in words_list:
                if word in self.DOWN:
                    print("Recognized down")
                    action_list.append([0, 1])
                if word in self.UP:
                    print("Recognized up")
                    action_list.append([0, -1])
                if word in self.RIGHT:
                    print("Recognized right")
                    action_list.append([1, 0])
                if word in self.LEFT:
                    print("Recognized left")
                    action_list.append([-1, 0])
            return action_list
        except sr.WaitTimeoutError:
            print("Too slow talking")
        except sr.RequestError as e:
            print(f"Could not connect to the Google Speech Recognition API: {e}")
        except sr.UnknownValueError:
            print("Couldn't understand")
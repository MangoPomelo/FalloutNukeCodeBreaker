import re
import os
import time
import sys


def is_encompassed_by(list_a, list_b):
    for item in list_a:
        if item in list_b:
            list_b.remove(item)
        else:
            return False
    return True


def slow_print(string, sleep_time=0.01, end='\n'):
    for l in string:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(sleep_time)

    if end == '\n':
        print('')
    elif end == '':
        pass


def program_exit():
    os.system('cls')
    os.system('color 07')
    exit()


class CodeBreaker:
    def __init__(self):
        self.hint = ''
        self.wordlist = [line.strip().lower() for line in open('./words.txt')]
        self.transceivers = {}

    def load_tranceivers(self, found_transceivers):
        lower_cased = {(k.lower(), v) for k, v in found_transceivers.items()}
        self.transceivers.update(lower_cased)

    def decipher(self, hint):
        hint = hint.lower()
        pattern = "^" + hint.replace("_", "\w") + "$"
        keywords = [w for w in self.wordlist if re.match(pattern, w)]

        slow_print("Possible Launch Codes:")
        for keyword in keywords:
            # Generate corresponding alphabet
            alphabet = 'abcdefghijklmnopqrstuvwxyz'
            new_alphabet = alphabet
            for letter in keyword:
                new_alphabet = new_alphabet.replace(letter, '')
            new_alphabet = keyword + new_alphabet

            # Transfer the transceivers from original alphabet into new alphabet
            selected_letters = ''
            for letter in self.transceivers.keys():
                co_letter = alphabet[new_alphabet.index(letter)]
                selected_letters += co_letter

            # Use dictonary order to find the unscrambled word
            alphabetical_ordered = sorted(selected_letters)
            scrambleds = []
            for w in self.wordlist:
                if len(sorted(w)) == 8 and is_encompassed_by(alphabetical_ordered, sorted(w)):
                    # Check if every letter is legal
                    if re.match('^[a-z]+$', w): scrambleds.append(w)
            
            for scrambled in scrambleds:
                code = []
                # Decipher: Code pieces --[new_ab, ab]--> Scrambled --> Unscrambled --[ab, new_ab]--> Encoded word --[Code pieces]--> Code
                for letter in scrambled:
                    code.append(str(self.transceivers.get(new_alphabet[alphabet.index(letter)], "_")))
                code = ''.join(code)
                slow_print("[%s] (Unscrambled: %s)" % (code, scrambled), 0.005)


def main():
    os.system('cls')
    os.system('color 0a')
    slow_print("[Nuclear Code Break Terminal]\n\n")
    slow_print("- Version: 1.01 -\n")
    print("-" * 35)
    slow_print("Initializing...\n"); time.sleep(1)
    breaker = CodeBreaker()
    # Enter Enclave's keyword
    slow_print("Enter the keyword from enclave's terminal. If a letter is unknown, put an underscore mark.\nFor example, FLO_CH__T_NG.\n", end="")
    while True:
        hint = input("> ")
        if hint: break

    # Enter found transceivers
    found_transceivers = {}
    slow_print("Enter the letter/number pairs you've found, like A-9.\nThe uncertainty depends on the amount of pairs you give. Full eight pieces are recommended.\nPress Ctrl + C to stop.")
    while len(found_transceivers) < 8:
        try:
            pair = input("> ")
            letter, num = pair.split('-')
            found_transceivers[letter] = num
        except ValueError:
            slow_print("Format Error, please enter again.")
        except KeyboardInterrupt:
            breaker.load_tranceivers(found_transceivers)
            slow_print("\nTransceivers have been loaded.")
            break
    
    breaker.load_tranceivers(found_transceivers)
    slow_print("\nDeciphering, please wait...\n")
    breaker.decipher(hint)

    os.system('pause')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        program_exit()

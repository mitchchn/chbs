#!/usr/bin/env python
"""
correcthorse.py: Generates passphrases that are long, secure and memorable,
using true random numbers from RANDOM.org

Author: Mitchell Cohen (mitch.cohen@me.com)
Created: April 15 2014
Version: 0.2

The word-matching algorithm and included wordlists are from Diceware:
http://world.std.com/~reinhold/diceware.html

Diceware is a trademark of Arnold G Reinhold.

The name and inspiration for this program comes from an xkcd comic:
http://xkcd.com/936/

xkcd is written by Randall Munroe.

"""

import os
import argparse
import random
import distutils.util
import randomapi

# Constants
DICEWARE_WORD_LENGTH = 5
DEFAULT_NUM_WORDS = 5
DICE_MIN = 1
DICE_MAX = 6
WORDLIST_DEFAULT_FILENAME = "wordlist.asc"
APIKEY_PATH = "apikey"
API_BETA_URL = "https://api.random.org/api-keys/beta"

# RANDOM.org API
true_random = randomapi.RandomJSONRPC
api_key = ""

# Variables
dir = os.path.dirname(__file__)


def pseudo_random_integers(n, min, max):
    random_integers = [random.randint(min, max) for n in range(0, n)]
    return random_integers


def true_random_integers(n, min, max):
    random_integers = true_random.generate_signed_integers(n, min, max)
    return random_integers


def roll_dice(reps, sets, randomizer=true_random_integers):
    """
    Simulates sets of multiple dice rolls
    """
    random_function = randomizer
    data = random_function(n=reps * sets, min=DICE_MIN, max=DICE_MAX)

    dicerolls = ["".join(str(x) for x in data[i:i + reps])
             for i in range(0, len(data), reps)]

    return dicerolls


def match_dice_rolls(wordlist, dicerolls):
    return [wordlist[roll] for roll in dicerolls]


def chomp(s):
    return s[:-1] if s.endswith('\n') else s


def random_digit():
    digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    return random.choice(digits)


def random_symbol():
    symbols = ['@', '#', '!', '%', '$', '&', '*']
    return random.choice(symbols)

# Don't need to use the true random seed for the random caps/digits/symbols.
# It's just a convenience feature for passwords that require it.


def make_random_caps(wordlist):
    index = random.randint(0, len(wordlist) - 1)
    word_to_capitalize = wordlist[index]
    if not word_to_capitalize[0].isdigit():
        word_to_capitalize = word_to_capitalize.capitalize()
        wordlist[index] = word_to_capitalize
    return wordlist


def append_random_digit(wordlist):
    index = random.randint(0, len(wordlist) - 1)
    word_to_append = wordlist[index]
    if not word_to_append[-1].isdigit():
        word_to_append = "{}{}".format(word_to_append, random_digit())
    wordlist[index] = word_to_append
    return wordlist


def append_random_symbol(wordlist):
    index = random.randint(0, len(wordlist) - 1)
    word_to_append = wordlist[index]
    new_word = "{}{}".format(word_to_append, random_symbol())
    wordlist[index] = new_word
    return wordlist

# Amend the basic passphrase with optional requirements


def compile_passphrase(matched_words, options_dict):
    # Sanitize non-printing characters
    clean_list = [chomp(word) for word in matched_words]

    if options_dict["digit"]:
        clean_list = append_random_digit(clean_list)

    if options_dict["caps"]:
        clean_list = make_random_caps(clean_list)

    if options_dict["sym"]:
        clean_list = append_random_symbol(clean_list)

    sanitized_passphrase = "".join(
        clean_list) if options_dict["no_spaces"] else " ".join(clean_list)
    return sanitized_passphrase

# Command-line parser


def buildParser():
    parser = argparse.ArgumentParser(
        description=
"""Generates passphrases that are long, secure and memorable,
using true random numbers from RANDOM.org"""
    )

    # Flags
    parser.add_argument("-n", type=int,
                        nargs=1,
                        default=[DEFAULT_NUM_WORDS],
                        help="generate the specified number of random words (default: {})".format(DEFAULT_NUM_WORDS))
    #parser.add_argument("-o", nargs=1, help="write output to a file")
    parser.add_argument(
        "-w", nargs=1, help="use an alternate Diceware word list")
    parser.add_argument("-P", action="store_true",
                        help="use the offline pseudo-random number generator instead (much less secure!)")
    parser.add_argument(
        "-S", help="hide status messages (except errors)", action="store_true")

    # Optional password requirements
    requirements = parser.add_argument_group(
        "additional password requirements")
    requirements.add_argument("-no-spaces", action="store_true",
                              help="don't leave spaces between words")
    requirements.add_argument("-caps", action="store_true",
                              help="force one word to begin with an uppercase letter")
    requirements.add_argument("-sym", action="store_true",
                              help="force one word to end with a random symbol")
    requirements.add_argument("-digit", action="store_true",
                              help="force one word to end with a random digit (0-9)")
    return parser


def load_wordlist(wordlist_path):
    wordlist = {}
    with open(wordlist_path) as fileIn:
        rows = (line.split('\t') for line in fileIn if line[0].isdigit())
        try:
            wordlist = {row[0]: row[1] for row in rows}

        except:
            raise Exception(
                """
Can't parse the wordlist file. Please make sure there are no formatting
errors and that the file is in the Diceware format
(tab-separated with index numbers).
""")
    if len(wordlist) is 0:
        raise Exception("The wordlist file appears to be empty.")
    return wordlist


def main():
    global true_random
    global api_key

    parser = buildParser()

    # Parse the arguments
    args = parser.parse_args()
    number_of_words = args.n[0]
    phrase_length = number_of_words * DICEWARE_WORD_LENGTH
    wordlist_filename = os.path.join(dir, WORDLIST_DEFAULT_FILENAME)
    wordlist_path = os.path.realpath(
        "".join(args.w)) if args.w else wordlist_filename
    verbose = False if args.S else True

    options_dict = {"no_spaces": args.no_spaces,
                    "caps": args.caps,
                    "sym": args.sym,
                    "digit": args.digit}

    # If the user wants to use the online randomizer, they better have an API
    # key
    if not args.P and not api_key:
        api_filename = os.path.join(dir, APIKEY_PATH)
        try:
            with open(api_filename) as fileIn:
                api_key = chomp(fileIn.readline())
        except IOError:
            print "Please place a valid RANDOM.org API key in a file named '{}'".format(APIKEY_PATH)
            print "You can get your own beta key at: {}".format(API_BETA_URL)
            exit(1)

    if not args.P:
        true_random = true_random(api_key)

    # Are we using pseudo-random or random numbers?
    random_function = pseudo_random_integers if args.P else true_random_integers

    # Load the wordlist
    if verbose:
        print "Using wordlist: '{}'...".format(wordlist_path) if args.w else "Using default wordlist..."
    try:
        wordlist = load_wordlist(wordlist_path)
    except IOError:
        print "Couldn't load the wordlist file."
        exit(1)
    except Exception as error:
        print error
        exit(1)

    # Getting true random numbers involves making a JSON request to RANDOM.org
    if random_function is true_random_integers:
        if verbose:
            print "Requesting {} true random integers....".format(
            number_of_words * DICEWARE_WORD_LENGTH)
        try:
            dicerolls = roll_dice(reps=DICEWARE_WORD_LENGTH,
                   sets=number_of_words, randomizer=true_random_integers)
        except KeyError as error:
            print error
            print "Invalid API Key"
            exit(1)
        except Exception as error:
            print error
            print "Couldn't download data from RANDOM.org."
            query = raw_input(
                "Use the pseudo-random number generator instead? (y/N)")
            answer = False
            try:
                answer = distutils.util.strtobool(query)
            except Exception:
                exit(1)
            if not answer:
                exit(1)
            else:
                dicerolls = roll_dice(reps=DICEWARE_WORD_LENGTH,
                                      sets=number_of_words, randomizer=pseudo_random_integers)
        print "OK."
        # Verify the signatue
        print "Verifying SHA-512 signature with RANDOM.org...."
        if true_random.verify_signature():
            print "OK."
        else:
            print "FAIL: The server returned 'false.' The data may have been tampered with."
    else:  # We are using the system's built-in RNG
        if verbose:
            print "Using pseudo-random generator (less secure)..."
        dicerolls = roll_dice(reps=DICEWARE_WORD_LENGTH,
                              sets=number_of_words, randomizer=pseudo_random_integers)

    matched_words = match_dice_rolls(
        wordlist=wordlist, dicerolls=dicerolls)
    print compile_passphrase(matched_words, options_dict)

if __name__ == '__main__':
    main()

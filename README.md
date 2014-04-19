correcthorse.py
====

**correcthorse.py** generates passphrases that are long, secure and memorable,
using true random numbers from RANDOM.org.

Why do "true" random numbers matter? Fact is, computers are terrible at being random. They just can't do it. Computer-generated random numbers are always based on a seed, such as the system time. If you know the seed, you can reproduce the "random" information. RANDOM.org addresses this limitation by basing its random seed on [atmospheric radio noise](http://www.random.org/faq/#Q1.4), providing us with the closest thing possible to truly random computed data.

This command-line tool retrieves true random numbers from RANDOM.org over an SSL connection. It then matches those numbers against a list of over 7000 words, creating passphrases with at least [64 bits](http://world.std.com/%7Ereinhold/dicewarefaq.html#howlong) of entropy. Although these passphrases are made up entirely of basic English words, they are more secure and harder to break than shorter passwords (even cryptic passwords filled with symbols and digits). They're also much easier to remember.


Dependencies
------------

**py-jsonpc**: the official Python JSON-RPC implementation, used here to make secure requests from RANDOM.org. To install it: `pip install python-jsonrpc`


Usage
-----

`python correcthorse.py --help` brings up the help menu.

Running `python correcthorse.py` with no other options will generate a passphrase with five random words. By default, the random numbers used to select words are downloaded over SSL from RANDOM.org. __To use this service, you must have a (free) API key. Acquire yours at: [https://api.random.org/api-keys/beta](https://api.random.org/api-keys/beta)__. Copy the key and paste it into a file named 'apikey'.

You can bypass the online service and use Python's pseudo-random number generator with the `-P` flag. Note that these results are not truly random, and passphrases created with this method should not be used to secure anything important.

The number of words in the passphrase can be set with the `-n [num]` flag.

Some optional flags let you specify additional requirements for the passphrase: currently, these include `-caps`, `-no-spaces` and `-digit` and `-symbol`.

Acknowledgements
----------------

correcthorse.py is an implementation of [Diceware](http://world.std.com/~reinhold/diceware.html).

Diceware is a trademark of Arnold G Reinhold.

The name and inspiration come from an [xkcd comic](http://xkcd.com/936/).

xkcd is penned by Randall Munroe.

<a href="http://xkcd.com/936/">
![xkcd 936](http://imgs.xkcd.com/comics/password_strength.png)
</a>



Disclaimer
----------

Long passphrases consisting of unrelated dictionary words are theoretically secure -- far more-so than typical passwords. They're also far easier to recall. That said, I cannot take responsibility for any data loss or security breaches that arise from usage of this tool. Please use common sense when signing up for online services, and always take advantage of two-factor authentication if it's available.
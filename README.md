correcthorse.py
====

**correcthorse.py** generates passphrases that are long, secure and memorable,
using true random numbers from RANDOM.org.



Dependencies
------------

**py-jsonpc**: The official Python JSON-RPC implementation, used here to make secure requests from RANDOM.org. To install it: `pip install python-jsonrpc`


Usage
-----

`python correcthorse.py --help` brings up the help menu.

Running `python correcthorse.py` with no other options will generate a passphrase with five random words. By default, the random numbers used to select words are downloaded over SSL from RANDOM.org. To use this service, you must have a (free) API key. Acquire yours at: [https://api.random.org/api-keys/beta](https://api.random.org/api-keys/beta). Place it in a file named 'apikey'.

You can bypass the online service and use the built-in pseudo-random number generator with the `-P` flag. Note that these results are not truly random, and passphrases created with this method should not be used to secure anything important.

The number of words in the passphrase can be set with the `-n [num]` flag.

Some optional flags let you specify additional requirements for the passphrase: currently, these include `-caps`, `-no-spaces` and `-digit` and `-symbol`.

Acknowledgements
----------------

The word-matching algorithm and included wordlists are from Diceware:

[http://world.std.com/~reinhold/diceware.html](http://world.std.com/~reinhold/diceware.html)

Diceware is a trademark of Arnold G Reinhold.

The name and inspiration for this program come from an xkcd comic:

[http://xkcd.com/936/](http://xkcd.com/936)

xkcd is written by Randall Munroe.


Disclaimer
----------

Long passphrases consisting of unrelated dictionary words are theoretically secure -- far more-so than typical passwords. They're also far easier to recall. That said, I cannot take responsibility for any data loss or security breaches that arise from usage of this tool. Please use common sense when signing up for online servies, and always take advantage of two-factor authentication if it's available.
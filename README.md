correcthorse.py
================

**correcthorse.py** generates passphrases that are long, secure and memorable,
using true random numbers from RANDOM.org.

###Why do "true" random numbers matter?###

Computers are terrible at being random. In fact, they just can't do it. Computer-generated random numbers are always based on a seed, such as the system time. If you know the seed, you can reproduce the "random" information. RANDOM.org addresses this limitation by basing its random seed on [atmospheric radio noise](http://www.random.org/faq/#Q1.4), providing us with the closest thing possible to truly random computed data.

__correcthorse.py__ retrieves true random numbers from RANDOM.org over an SSL connection. Then it matches those numbers against a list of over 7000 words, building passphrases with at least [64 bits](http://world.std.com/%7Ereinhold/dicewarefaq.html#howlong) of entropy.

###What's a passphrase?###

A passphrase is a password that doesn't suck as much. A good passphrase consists of 4-6 short, common words that aren't related but that can be recalled with a mnemonic or mental image. Something like: <a href="#xkcd">__correct horse battery staple__</a>. 

Although passphrases are made up entirely of normal English words, they are more secure and harder to break than typical short passwords (even cryptic passwords filled with symbols and digits). They're also much easier to memorize. Passphrases work swimmingly with a password manager like [1Password](https://agilebits.com/onepassword), which can store them and fill them in automatically on sites you visit.



Dependencies
------------

**py-jsonrpc**: the official Python JSON-RPC implementation, used here to make secure requests from RANDOM.org. To install it: `pip install python-jsonrpc`


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

<a name="xkcd">xkcd</a> is penned by Randall Munroe.

<a href="http://xkcd.com/936/">
![xkcd 936](http://imgs.xkcd.com/comics/password_strength.png)
</a>



Disclaimer
----------

Long passphrases consisting of unrelated dictionary words are theoretically secure -- far more-so than typical passwords. They're also far easier to recall. That said, I cannot take responsibility for any data loss or security breaches that arise from using this tool. Please use common sense when making and saving passwords and when signing up for online services with your personal data, and always take advantage of [two-factor authentication](http://www.pcmag.com/article2/0,2817,2456400,00.asp) if it's available.
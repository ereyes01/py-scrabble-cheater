# Scrabble Cheater's Toolbox

I admit it, I cheat at Scrabble from time to time. In order to mitigate the
public shame of this shocking revelation, I have shared the tools I use to aid
my cheating. At least if I cheat, I can help others cheat, too. Then, we can
all holds hands and cheat together. And we all win.

Now that I've gotten that off my chest, here's how you use these utilities to
cheat and win at Scrabble. These are crude tools you use in the Python shell.
I prefer IPython, but you can use your favorite REPL, write scripts, or be a 
prude and lose... whatever makes you feel good.

### Generating Your Scrabble Word Dictionary

Most Linux systems have a dictionary at `/usr/share/dict/words`. I found that
this dictionary has a mix of uppercase/lowercase, has words with apostrophies, 
and has words with other fancy punctuation, accent marks, etc. These are
obviously no help for Scrabble, whose words are case-insensitive and do not
allow for any sort of punctuation. Therefore I wrote a utility that sanitizes
the dictionary file of your choosing such that it only contains words suitable
for Scrabble, in lowercase.

To generate a Scrabble dictionary in the current directory:

```
$ gen_dict.py /usr/share/dict/words ./dict
```

This command creates a local file called `dict` containaing the sanitized
Scrabble-friendly dictionary.

##### DISCLAIMER: The resulting file may not exactly match the official Scrabble dictionary!!! It only sanitizes the words down to valid letters!

### Cheating

Now finally, the good part. The `ScrabbleCheater` class helps you cheat using
your sanitized Scrabble dictionary file. Let's build an object of this class 
using our `dict: file in our favorite Python REPL (IPython in this case):

```
In [1]: import words

In [2]: c = words.ScrabbleCheater(path="./dict")
```

Objects of this class contain a field called `words`. Initially, it contains a
list of all the words in the Scrabble dictionary. Let's now assume that we've
drawn the current hand in Scrabble:

`ZXJVATES`

Let's see all the words we can build from these letters, sorted by Scrabble score:

```
In [3]: c.find("zxjvates")
Out[3]: [u'zeta', u'vex', u'zest', u'texas', u'taxes', u'jest', u'axes', u'jets', u'tax', u'tex', u'sax', u'jet', u'z', u'sex', u'axe', u'ex', u'ax', u'xe', u'stave', u'j', u'vesta', u'x', u'vats', u'vest', u'save', u'vase', u'vets', u'vast', u'ave', u'vet', u'vat', u'eva', u'va', u'av', u'vs', u'seat', u'sate', u'east', u'teas', u'v', u'eats', u'set', u'sea', u'tea', u'sat', u'eat', u'ate', u'eta', u'ats', u'as', u'es', u'ts', u'st', u'ta', u'se', u'at', u't', u'a', u'e', u's']
```

That's nice. But now, suppose that we want to hit a double-word score. In doing
so, we have to connect our letters with the existing word "NOW" on the board.
We'd like to see all the combinations possible with our letters, plus the "NOW"
already played on the board:

```
In [5]: c.find("zxjvatesnow").ends_with("now")
Out[5]: [u'snow', u'now']
```

Not too many options with our current set of letters... "snow" is the only
possiblity of such a play.

As we look elsewhere on the board, we find that "MA" has been played, and we
have empty tiles on either side that we could potentially use. what are the
possibilties?

```
In [7]: c.find("zxjvatema").contains("ma")
Out[7]: [u'amaze', u'maze', u'max', u'maj', u'mate', u'mat', u'mae', u'ma']
```

The to-scoring play "amaze" is intriguing. Turns out the "e" Lands on a
triple-word-score tile. How much is this play worth?

```
In [8]: words.word_score("amaze") * 3
Out[8]: 48
```

48 points!! Zing!!!

Now I look so smart.

If you have a set of letters that can be formed into a larger set of words, you
can chain constraints to further whittle down the possibilities:

```
In [14]: c.find("rsssstttlnaaaeeeiiiioooouuuubmmgzpp").contains("tt").starts_with("g").ends_with("s")
Out[14]: [u'gazetteers', u'gazettes', u'guttersnipes', u'gluttonous', u'glottises', u'gutturals', u'garottes', u'gluttons', u'grottoes', u'glitters', u'glottis', u'grottos', u'gutters']
```

This example illustrates the 4 supported operations/constraints supported in
the `ScrabbleCheater` library:

- find(letters - str)
  - Given a set of letters, find all the possible words from those letters.
    Sort results by word score.
- starts_with(prefix - str)
  - Filter the object's words to the ones that start with the given prefix. Sort
    results by word score.
- ends_with(suffix - str)
  - Filter the object's words to the ones that end with the given suffix. Sort
    results by word score.
- contains(substring - str)
  - Filter the object's words to the ones that contain the given substring.
    Sort results by word score.

And that's the basics! I may add some more operations (like a way to help with
parallel rows of letters to form >1 words in a play). If I have time. If anyone
is in a rush, please fork and PR!

Have fun cheating!

### Running the Tests

I take my cheating very seriously. All the available constraints have
accompanying unit tests. To run the tests, you must have pytest installed.
These steps below can get you going:

```
$ virtualenv ~/scrabble-cheat-env
$ . ~/scrabble-cheat-env/bin/activate
$ pip install -r requirements.txt
$ py.test -v
```

Now, you can have full confidence in your cheating tools!

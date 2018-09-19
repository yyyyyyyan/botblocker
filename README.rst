botblocker
==========

Python program to identify and block your bot followers on Twitter

Requires 3.4 <= Python <= 3.7

Getting Started
---------------

These instructions will get you a copy of the project up and running on
your local machine for development and testing purposes.

Installing
~~~~~~~~~~

**Only if you use Python >= 3.7, you have to run this command first:**

::

   sudo pip install https://github.com/tweepy/tweepy/archive/master.zip

Now, no matter what Python version you're using (if it fits the requirement), the easiest way is installing using pip:

::

   sudo pip install botblocker

You can also clone this project using git:

::

   git clone https://github.com/yanorestes/botblocker.git
   cd botblocker
   python setup.py install

Preparation
-----------

At first, setting things up to botblocker may sound overcomplicated.
However, following this step-by-step tutorial will ensure an easy
proceedment! Still, this “hard” part of the tutorial will have to be
followed only once ;)!

1 - Getting your Twitter Developer Account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As I’m providing the complete code of this project, I can’t let you guys
use my API keys, so you need to get them yourselves. This is how you do
it:

-  Access `this link <https://developer.twitter.com/en/apply/user>`__ to
   associate your Twitter profile with a developer account
-  Click in ``Continue``
-  Check “I am requesting access for my own personal use”
-  Type in your username on the field below
-  Select the country you live and press ``Continue``
-  Check “Consumer / end-user experience”
-  In the textbox below, type something similar to the following example
   (note that it is better not to copy the whole text, so that your
   application will be approved faster):

::

   The project I'm building aims to identify and block follower bots. It is based on programming language Python, using Tweepy to connect to Twitter API and Botometer to identify bots. The project gives the user mutiple options on identifying and blocking the bots, resulting in a clean and simple usage. Botometer analizes each profile basing itself on the tweets and the specs of the profile, to, then, calculate a result (a score from 0 to 5; the higher, the more likely it is that the profile is indeed a bot). None of the results are shared with anyone or kept with us.

-  Check ``No`` and click ``Continue``
-  Scroll through the terms of service and check the “read and agree”
   box
-  Click on “Submit application”
-  Check your email account and confirm your email
-  Wait for your Developer Account to get approved

2 - Getting your Twitter API Keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once your Developer Account gets approved, you can pass on to creating
an app:

-  Access `this link <https://developer.twitter.com/en/apps/create>`__
   to register your app
-  Chose an authentic name to your app and fill the first field
-  In the textbox below, type something similar to the following
   example:

::

   Python program to identify and block your bot followers on Twitter.

-  Paste https://github.com/yanorestes/botblocker on the field below
-  Skip to the last textbox and type in something similar to the
   following example:

::

   The project I'm building aims to identify and block follower bots. It is based on programming language Python, using Tweepy to connect to Twitter API and Botometer to identify bots. The project gives the user mutiple options on identifying and blocking the bots, resulting in a clean and simple usage.

-  Click on ``Create`` and confirm

You will be redirected to your app’s page. Then:

-  Access the “Keys and tokens” tab
-  Save the two keys under “Consumer API keys” somewhere. The first is
   your Consumer Key and the second is your Consumer Secret Key. You
   will need both of them later configuring botblocker:

.. image:: https://cdn.pbrd.co/images/HEvDXKu.png

3 - Getting your Mashape API Key
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With your Twitter API keys in hands, you’ll only have to get your
Mashape API Key. Follow these steps in order to do so:

-  Access `this link <https://market.mashape.com/>`__ and register an
   account (I recommend signing up with GitHub, but there are other
   options)
-  If you have a credit card available (**you won’t have to pay a single
   dollar, don’t worry!**), access `this
   link <https://market.mashape.com/OSoMe/botometer-pro>`__, click on
   ``Pricing`` and subscribe to the Basic Free Plan. If you don’t, you
   can use `this link <https://market.mashape.com/OSoMe/botometer>`__.
   The first link will (probably) make the program run faster.
-  On `this link <https://market.mashape.com/OSoMe/botometer>`__, copy
   your personal “X-Mashape-Key” on the request example code and save
   somewhere:

.. image:: https://my.mixtape.moe/nqkagq.png

Using
-----

Now it’s time to finally run botblocker! Botblocker you’ll go through
all of your followers and calculate a “bot score” of them. The score
goes from 0 to 5. The higher the score, the more likely is the chance
the profile is a bot. The default behaviour is to automatically block every profile identified as a bot.

If you installed the package using pip, you can simply run botblocker in
the command line:

::

   botblocker [-h] [-c] [--noblock] [--saveallowlist] [--softblock] [--report] [-l {1,2,3}] -u USER [-v]

These are the parameters you can use:

-  ``-h`` or ``--help`` - Shows a help message and exit
-  ``-c`` or ``--config`` - (Re)configure usage settings. At least once,
   you’ll have to do this.
-  ``--noblock`` - Don’t block anyone automatically. This is not recommended, especially for profiles with lots of followers, as you may lose all the running progress if you exit early.
-  ``--saveallowlist`` - Save users identified as non-bots to an
   allowlist. Recommended.
-  ``--softblock`` - Do soft block (block and unblock right after)
-  ``-r`` or ``--report`` - Report users identified as bots to Twitter
-  ``-l {1,2,3}`` or ``-level {1,2,3}`` - Choose level of rigorosity to
   use to identify bots. Level 1 only consider bots those with score >=
   4, level 2 (default) considere those with score >= 3 and level 3
   considere those with score >= 2.5.
-  ``-u USER`` or ``-user USER`` - The Twitter username you want to run
   botblocker for. Required.
-  ``-v`` or ``--version`` - Get the current version of botblocker

You can also run the script directly by ``botblocker.py``:

::

   python -W ignore -m botblocker [-h] [-c] [--noblock] [--saveallowlist] [--softblock] [--report] [-l {1,2,3}] -u USER [-v]

Contributing
------------

I’m accepting pull requests that improve speed and legibility of the
code.

Authors
-------

-  **Yan Orestes** - *Initial work* -
   `yanorestes <https://github.com/yanorestes>`__

License
-------

This project is licensed under the MIT License - see the
`LICENSE <https://github.com/yanorestes/botblocker/blob/master/LICENSE.txt>`__
file for details.

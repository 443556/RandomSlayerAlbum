Random Slayer Album
===================

As a longstanding Slayer fan and relative newcomer to Python, I've had great fun writing some code that generates a randomised Slayer album.


Instructions
------------
Copy the code, navigate to directory where the file lives, then execute "python random_slayer_album.py" in terminal/command window.


Notes & Caveats
---------------

**NOTE 17 APR 2018**
Added handling of sorts for the broken webscrape URL; the get_data() method remains in place for posterity.
Found the requisite data files locally; they've been committed to the repo.
**END NOTE**

This program is heavily dependent on a BeautifulSoup webscrape. The necessary scrape will be conducted the first time the program is executed; this will take in the region of 60-90 seconds. Subsequent executions will be much quicker.

The randomly generated material will for the most part be nonsense, but will also be very funny by times.

Text formatting is 5 words per line, skip a line every verse/fourth line; the last verse of every track will usually contain less than 20 words.

Some of the scraped words are poorly punctuated/spelt, aren't even words etc...

This is just a simple, fun, program; absolutely no disrespect or copyright infringement is intended.

**TODO**
'Haunting the Chapel' (1984) not included due to it being an EP and not a full LP? WHAT?

That's a feeble excuse - really need to include it, as it contains some of their best tracks






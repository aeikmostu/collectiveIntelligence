__author__ = 'amouskite'

import feedparser
import re

# Returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
    print(url)
    # Parse the feed
    d = feedparser.parse(url)
    wc = {}
    # Loop over all the entries
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description
        # Extract a list of words
        words = getwords(e.title + ' ' + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1
    if 'feed' in d.keys() and 'title' in d['feed']:
        return d['feed']['title'], wc
    else:
        return None
def getwords(html):
    # Remove all the html tags
    txt = re.compile(r'<[^>]+>').sub('', html)
    # Split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    # Convert to lowercase
    return [word.lower for word in words if word != '']

# Get words from blogs
apcount = {}
wordcounts = {}
feedlist = file('feedlist.txt')
feedlistNumber=0
for feedurl in feedlist:
    wordcountresult = getwordcounts(feedurl)
    if wordcountresult is None:
        continue
    feedlistNumber += 1
    title, wc = wordcountresult
    wordcounts[title] = wc
    for word, count in wc.items():
        apcount.setdefault(word, 0)
        if count > 1:
            apcount[word] += 1

# Ignore rare and very common words
wordlist = []
print(apcount)
for w, bc in apcount.items():
    frac = float(bc)/feedlistNumber
    if 0.1 < frac < 0.5:
        wordlist.append(w)

# Generate file
out = file('blogdata.txt', 'w')
out.write('Blog')
for word in wordlist:
    out.write('\t%s' % word)
out.write('\n')
for blog, wc in wordcounts.items():
    out.write(blog)
    for word in wordlist:
        if word in wc:
            out.write('\t%d' % wc[word])
        else:
            out.write('\t0')
    out.write('\n')


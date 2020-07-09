#!/usr/bin/env python3
import sys
import os
import re
import requests

USAGE = """
Usage: %s sticker-page
""" % sys.argv[0]

if len(sys.argv) != 2:
    print(USAGE)
    sys.exit(1)

r = requests.get(sys.argv[1])

# sticker pack id
sid = re.search('product/(\\d+)', sys.argv[1]).group(1)
print('Scraping %s...' % sid)
if not os.path.exists(sid):
    os.mkdir(sid)

# scrape sticker links
links = re.finditer('stickershop/v1/sticker/(\\d+)', r.text)
done = []
for x in links:
    if x.group(1) not in done:
        link = 'https://stickershop.line-scdn.net/stickershop/v1/sticker/%s/iPhone/sticker@2x.png' % x.group(1)
        print('Getting %s' % link)
        r = requests.get(link)
        with open('%s/%s.png' % (sid, x.group(1)), 'wb') as f:
            f.write(r.content)
        done.append(x.group(1))

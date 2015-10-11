import os
import gfsoso
import aolsearch
import googlesearch
import bingsearch
import hxgoogle

#searchEngine = googlesearch.google
#searchEngine = aolsearch.google
#searchEngine = bingsearch.google

if os.environ.has_key('search_engine'):
	search_engine = os.environ['search_engine']
else:
	search_engine = 'hxgoogle'

if search_engine == 'gfsoso':
	google = gfsoso.google
elif search_engine == 'google':
 	google = googlesearch.google
elif search_engine == 'aol':
 	google = aolsearch.google
elif search_engine == 'bing':
 	google = bingsearch.google
elif search_engine == 'hxgoogle':
        google = hxgoogle.google
else:
	google = hxgoogle.google

searchEngine = google


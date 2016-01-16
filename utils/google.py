import os
import gfsoso
import aolsearch
import googlesearch
import bingsearch
import hxgoogle
import hxgoogle2
import hxgoogle3

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
elif search_engine == 'hxgoogle2':
        google = hxgoogle2.google
elif search_engine == 'hxgoogle3':
        google = hxgoogle3.google
else:
	google = hxgoogle2.google

searchEngine = google


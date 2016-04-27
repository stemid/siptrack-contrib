# Objectsearch

Searches all objects in [Siptrack](https://github.com/sii/siptrackweb) recursively for an attribute and its value. Siptrack by default only indexes a few attributes so this tool enables you to slowly search for any attribute value. 

The attribute value argument takes wildcards like [fname](https://docs.python.org/2/library/fnmatch.html).

# Usage

See ``./objectsearch.py --help`` for more info. 

The -T argument is the least finished feature, right now it defaults to D which is devices. I've hard coded class types ``device`` and ``device category`` to the D type so that's all it can search for. 

Adding more object types and their class types is trivial.

## Output

Output is also subject to change but right now it's CSV with semicolon as separator and a simple header naming each column even if there are no results.

## Example

    python objectsearch.py -c ../siptrack_live.cfg -d 'Sweden:Stockholm' -A model -V 'UCS*'

Show all devices with a model attribute that starts with UCS. 

    python objectsearch.py -c ../siptrack_live.cfg -d 'Sweden:Stockholm' -A model -V 'UCS*' --no-csv-header | sed -n 's/^\([[:digit:]]*\);.*/http:\/\/siptrack.localhost\/display\/\1/p'

Search for all devices with a model attribute matching UCS and create siptrack-links from the OID.

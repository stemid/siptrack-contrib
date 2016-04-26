# Objectsearch

Searches all objects in Siptrack recursively for an attribute and its value. 

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


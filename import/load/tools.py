#!/usr/bin/env python
"""
common tools for load scripts
"""
import os, re
import simplejson
import web
from settings import db

_stripterms = ['the', 'corporation', 'corp', 'incorporated', 'inc']
r_plain = re.compile(r'[a-z ]+')
def stemcorpname(name):
    """
    >>> stemcorpname('The Boeing Corp.')
    'boeing'
    >>> stemcorpname('SAIC Inc.')
    'saic'
    """
    name = name.lower()
    name = ''.join(r_plain.findall(name))
    name = ' '.join(x for x in name.split() if x not in _stripterms)
    return name

_districtcache = {}
def districtp(district):
    """
    Return the watchdog ID for the represenative of `district`.
    """
    if not _districtcache:
        reps = simplejson.load(file('../data/load/politicians/index.json'))
        for repid, rep in reps.iteritems():
            if rep['district_id'] in _districtcache:
                _districtcache[rep['district_id']].append(repid)
            else:
                _districtcache[rep['district_id']] = [repid]
    
    return _districtcache.get(district) or []

def getWatchdogID(district, lastname):
    watchdog_ids = filter(lambda x: lastname.lower().replace(' ', '_') in x, districtp(district))
    if len(watchdog_ids) == 1:
        return watchdog_ids[0]
    return None


_govtrackcache = {}
_opensecretscache = {}
def _fill():
    for pol in db.select('politician', what='id, govtrackid, opensecretsid'):
        _govtrackcache[pol.govtrackid] = str(pol.id)
        _opensecretscache[pol.opensecretsid] = str(pol.id)
        
def govtrackp(govtrack_id):
    """
    Return the watchdog ID for a person's `govtrack_id`.
    
        >>> govtrackp('400114')
        'michael_f._doyle'
        >>> print govtrackp('aosijdoisad') # ID we don't have
        None
    """
    if not _govtrackcache: _fill()
    return _govtrackcache.get(govtrack_id)

def opensecretsp(opensecrets_id):
    """
    Returns the watchdog ID for a person's `opensecrets_id`.
    """
    if not _opensecretscache: _fill()
    return _opensecretscache.get(opensecrets_id)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

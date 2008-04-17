#!/usr/bin/env python
"Unit tests for code in webapp.py."
import re, time, simplejson, pprint
import webapp
import urllib, web

def ok(a, b): assert a == b, (a, b)
def ok_re(a, b): assert re.search(b, a), (a, b)

def time_thunk(thunk):
    start = time.time()
    rv = thunk()
    return time.time() - start, rv

def test_find():
    "Test /us/."
    headers = {'Accept': 'text/html'}
    ok(webapp.app.request('/', headers=headers).status[:3], '200')

    # A ZIP code within a single congressional district.
    resp = webapp.app.request('/us/?zip=94070', headers=headers)
    ok(resp.status[:3], '303')
    ok(resp.headers.get('Location'), 'http://0.0.0.0:8080/us/ca-12')

    # A ZIP code in Indiana that crosses three districts.
    resp = webapp.app.request('/us/?zip=46131', headers=headers)
    ok(resp.status[:3], '200')
    ok_re(resp.data, '/us/in-04')
    ok_re(resp.data, 'Stephen Buyer')   # rep for IN-04 at the moment
    ok_re(resp.data, '/us/in-05')
    ok_re(resp.data, '/us/in-06')
    assert '/us/in-07' not in resp.data, resp.data
    
    # Test for LEFT OUTER JOIN: district row with no corresponding politician row.
    resp = webapp.app.request('/us/?zip=70072', headers=headers)
    ok(resp.status[:3], '200')
    ok_re(resp.data, '/us/la-01')       # no rep at the moment

    # Test for /us/ listing of all the districts and reps.
    # Takes 9-12 seconds on my machine, I think because it's
    # retrieving the district outline data from MySQL.  Takes nearly
    # 1s on watchdog.net.
    reqtime, resp = time_thunk(lambda: webapp.app.request('/us/',
                                               headers=headers))
    print "took %.3f sec to get /us/" % reqtime
    ok(resp.status[:3], '200')
    ok_re(resp.data, '/us/in-04')
    ok_re(resp.data, 'Stephen Buyer')
    ok_re(resp.data, '/us/la-01')       # LEFT OUTER JOIN test
    assert '(Rep.  )' not in resp.data

def test_state():
    "Test state pages such as /us/nm.html."
    resp = webapp.app.request('/us/nm.html')
    ok(resp.status[:3], '200')
    ok_re(resp.data, 'href="/us/nm-01"')
    assert '/us/NM-01' not in resp.data # the uppercase URLs aren't canonical
    ok_re(resp.data, 'href="/us/nm-02"')
    ok_re(resp.data, 'href="/us/nm-03"')
    assert '/us/nm-04' not in resp.data

    # JSON
    resp = webapp.app.request('/us/nm.json')
    ok(resp.status[:3], '200')
    # Copied and pasted from current output; hope it's right.  See
    # below about perils of writing unit tests afterwards.
    ok(simplejson.loads(resp.data),
       [{     'code': 'NM',
          'fipscode': '35',
              'name': 'New Mexico',
            'status': 'state',
              'type': 'State',
               'uri': 'http://watchdog.net/us/nm',
         'wikipedia': 'http://en.wikipedia.org/wiki/New_Mexico'}])

    # JSON obtained with Accept header.
    rsp2 = webapp.app.request('/us/nm', headers={'Accept': 'application/json'})
    ok(rsp2.data, resp.data)

    #@@ I'd write an N3 test but I'm too sleepy to Google up an N3
    # parser right now.

def test_district():
    "Test district pages such as /us/nm-02."
    headers = {'Accept': 'text/html'}
    resp = webapp.app.request('/us/nm-02', headers=headers)
    ok(resp.status[:3], '200')
    ok_re(resp.data, r'69,598 sq\. mi\.')  # the district's area
    ok_re(resp.data, 'href=".*/us/nm"')

    # JSON
    resp = webapp.app.request('/us/nm-02.json', headers=headers)
    ok(resp.status[:3], '200')
    ok(resp.headers['Content-Type'], 'application/json')
    payload = simplejson.loads(resp.data)
    ok(len(payload), 1)
    district = payload[0]
    # I hope these are right.  I just copied them from the current
    # output --- this is a problem with doing unit tests after the
    # fact.  I omitted floating-point numbers (poverty_pct,
    # center_lat, center_lng) and the outline.
    expected = dict(
        almanac = 'http://nationaljournal.com/pubs/almanac/2008/people/nm/rep_nm02.htm',
        area_sqmi = 69598,
        cook_index = 'R+6',
        est_population = 625204,
        est_population_year = 2005,
        median_income = 29269,
        name = 'NM-02',
        state = 'http://watchdog.net/us/nm',
        type = 'District',
        uri = 'http://watchdog.net/us/nm-02',
        wikipedia = "http://en.wikipedia.org/wiki/New_Mexico's_2nd_congressional_district",
        zoom_level = 6,
        voting = True,
    )

    for k, v in expected.items():
        ok(district[k], v)
    #pprint.pprint(payload)

def test_webapp():
    "Test the actual watchdog.net webapp.app app."
    test_state()
    test_district()
    test_find()                         # slow

def main():
    test_webapp()


if __name__ == '__main__': main()
import scraperwiki
import json
import sqlite3

# Get the JSON
json = json.loads(scraperwiki.scrape('https://wahl.tagesspiegel.de/2017/api/candidates/dump'))

candidates = []

for candidate in json['result']:

    facebook_urls = []

    for link in candidate['links']:
        if link['type'] == 'facebook':
            facebook_urls.append(link['url'])

    candidate = {
        'id': candidate['id'],
        'name': unicode(candidate['name']['forename'] + ' ' + candidate['name']['surname']),
        'area_id': candidate['election']['district'],
        'area_type_description': 'District',
        'facebook_urls': ', '.join(facebook_urls)
    }

    candidates.append(candidate)

    print 'Parsed candidate: ' + candidate['name']

try:
    scraperwiki.sqlite.execute('DELETE FROM data')
except sqlite3.OperationalError:
    pass
scraperwiki.sqlite.save(
    unique_keys=['id'],
    data=candidates)

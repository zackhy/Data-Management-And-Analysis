import json

with open('yelp_academic_dataset.json') as inf, open('businessdata.tsv', 'w') as ouf:
    ouf.write('\t'.join(['name', 'city', 'state', 'stars', 'review_count', 'main_category']))
    ouf.write('\n')

    for line in inf:
        js = json.loads(line.encode('utf-8'))
        if js['type'] == 'business':
            try:
                category = js['categories'][0]
            except:
                category = 'NA'
            outstr = '\t'.join([
                js['name'],
                js['city'],
                js['state'],
                str(js['stars']),
                str(js['review_count']),
                category]).encode('utf-8')

            ouf.write(outstr)
            ouf.write('\n')

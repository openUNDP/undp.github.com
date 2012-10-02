import requests, csv, json
#from xml.etree.ElementTree import ElementTree
#from lxml import etree
#from lxml import objectify

hdi = csv.DictReader(open('hdi-csv-test.csv', 'rb'), delimiter = ',', quotechar = '"')
geo = csv.DictReader(open('country-centroids.csv', 'rb'), delimiter = ',', quotechar = '"')

hdi_sort = sorted(hdi, key = lambda x: x['hdi2011'], reverse = True)
country_sort = sorted(geo, key = lambda x: x['iso3'])

years = [1980,1985,1990,1995,2000,2005,2006,2007,2008]
current_year = 2011

row_count = 0
rank = 0
hdi_index = []
for val in iter(hdi_sort):
    row_count = row_count + 1
    change = []
    change_year = {}
    for y in years:
        if val['hdi%d' % y] != '':
            change_year = float(val['hdi%d' % current_year]) - float(val['hdi%d' % y])
            if len(change) == 0:
                change.append(change_year)
                
    if len(change) == 0:
        change.append("")
    for ctry in country_sort:
        if ctry['name'] == val['country']:
            if val['hdi2011'] == "":
                g = {
                    "id": ctry['iso3'],
                    "name": val['country'],
                    "hdi": "",
                    "health": "",
                    "income": "",
                    "education": "",
                    "change": change[0],
                    "rank": "n.a."
                }
            else:
                if ctry['iso3'].rfind("A-",0,2) == 0:
                    g = {
                        "id": ctry['iso3'],
                        "name": val['country'],
                        "hdi": float(val['hdi2011']),
                        "health": float(val['health2011']),
                        "income": float(val['income2011']),
                        "education": float(val['ed2011']),
                        "change": change[0],
                        "rank": "n.a."
                    }
                else:
                    rank = rank + 1
                    g = {
                        "id": ctry['iso3'],
                        "name": val['country'],
                        "hdi": float(val['hdi2011']),
                        "health": float(val['health2011']),
                        "income": float(val['income2011']),
                        "education": float(val['ed2011']),
                        "change": change[0],
                        "rank": rank
                    }
            hdi_index.append(g)

print "Processing..."
print "Processed %d rows" % row_count
hdi_index_sort = sorted(hdi_index, key = lambda x: x['rank'])
print hdi_index_sort
hdi_writeout = json.dumps(hdi_index_sort, sort_keys=True, indent=4)

hdi_out = open('../api/hdi.json', 'wb')
hdi_out.writelines(hdi_writeout)
hdi_out.close()

hdi_csv = open('test/hdi-index-test.csv', 'wb')
fieldnames = ('id','name','hdi','health','income','education','change','rank')
writer = csv.DictWriter(hdi_csv, fieldnames=fieldnames)
headers = dict( (n,n) for n in fieldnames)
writer.writerow(headers)
for i in hdi_index:
    writer.writerow(i)
hdi_csv.close()


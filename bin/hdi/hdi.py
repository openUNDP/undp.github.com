import requests, csv, json
#from xml.etree.ElementTree import ElementTree
#from lxml import etree
#from lxml import objectify

hdi = csv.DictReader(open('hdi-csv-clean.csv', 'rb'), delimiter = ',', quotechar = '"')
geo = csv.DictReader(open('../process_files/country-centroids.csv', 'rb'), delimiter = ',', quotechar = '"')

hdi_sort = sorted(hdi, key = lambda x: x['hdi2011'], reverse = True)
country_sort = sorted(geo, key = lambda x: x['iso3'])

years = [1980,1985,1990,1995,2000,2005,2006,2007,2008,2011]
current_year = 2011

row_count = 0
rank = 0
hdi_index = []
for val in iter(hdi_sort):
    row_count = row_count + 1
    hdi_total = []
    hdi_health = []
    hdi_ed = []
    hdi_inc = []
    change = []
    change_year = {}
    for y in years:
        if val['hdi%d' % y] != '':
            hdi_total.append([y,float(val['hdi%d' % y])])
            hdi_health.append([y,float(val['health%d' % y])])
            hdi_ed.append([y,float(val['ed%d' % y])])
            hdi_inc.append([y,float(val['income%d' % y])])
            if y != current_year:
                change_year = float(val['hdi%d' % current_year]) - float(val['hdi%d' % y])
                if len(change) == 0:
                    change.append(change_year)
                
    if len(change) == 0:
        change.append("")
    for ctry in country_sort:
        if ctry['name'] == val['country']:
            if val['hdi%d' % current_year] == "":
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
                        "hdi": hdi_total,
                        "health": hdi_health,
                        "income": hdi_inc,
                        "education": hdi_ed,
                        "change": change[0],
                        "rank": "n.a."
                    }
                else:
                    rank = rank + 1
                    
                    g = {
                        "id": ctry['iso3'],
                        "name": val['country'],
                        "hdi": hdi_total,
                        "health": hdi_health,
                        "income": hdi_inc,
                        "education": hdi_ed,
                        "change": change[0],
                        "rank": rank
                    }
            hdi_index.append(g)

print "Processing..."
print "Processed %d rows" % row_count
hdi_index_sort = sorted(hdi_index, key = lambda x: x['rank'])
print hdi_index_sort
hdi_writeout = json.dumps(hdi_index_sort, sort_keys=True, separators=(',',':'))

hdi_out = open('../api/hdi.json', 'wb')
hdi_out.writelines(hdi_writeout)
hdi_out.close()

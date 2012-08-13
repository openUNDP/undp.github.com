import csv, sys, json

##########################
# Process Region index
# Open file
regions = csv.DictReader(open('csv/undp-regions-index.csv', 'rb'), delimiter = ',', quotechar = '"')

regions_sort = sorted(regions, key = lambda x: x['id'])

row_count = 0
for row in regions_sort:
    row_count = row_count + 1

print "Processing..."
print "Processed %d rows" % row_count
region_writeout = json.dumps(regions_sort, sort_keys=True, indent=4)

region_out = open('index/region-index.json', 'wb')
region_out.writelines(region_writeout)
region_out.close()

##########################
# Process Project ID index
# Open index csv
project_id = csv.DictReader(open('csv/undp-projectid-index.csv', 'rb'), delimiter = ',', quotechar = '"')
# Sort file
project_id_sort = sorted(project_id, key = lambda x: x['id'])

row_count = 0
for row in project_id_sort:
    row_count = row_count + 1

print "Processing..."
print "Processed %d rows" % row_count
proj_writeout = json.dumps(project_id_sort, sort_keys=True, indent=4)

project_out = open('index/project-id-index.json', 'wb')
project_out.writelines(proj_writeout)
project_out.close()


##########################
# Process Subproject ID index
# Open index csv
subproject_id = csv.DictReader(open('csv/undp-subprojectid-index.csv', 'rb'), delimiter = ',', quotechar = '"')
# Sort file
subproject_id_sort = sorted(subproject_id, key = lambda x: x['id'])

row_count = 0
for row in subproject_id_sort:
    row_count = row_count + 1

print "Processing..."
print "Processed %d rows" % row_count
subproj_writeout = json.dumps(subproject_id_sort, sort_keys=True, indent=4)

subproject_out = open('index/subproject-id-index.json', 'wb')
subproject_out.writelines(subproj_writeout)
subproject_out.close()


##########################
# Process Donor index
# Open index csv
donor = csv.DictReader(open('csv/undp-donor-index.csv', 'rb'), delimiter = ',', quotechar = '"')
# Sort file
donor_sort = sorted(donor, key = lambda x: x['id'])

row_count = 0
for row in donor_sort:
    row_count = row_count + 1

print "Processing..."
print "Processed %d rows" % row_count
donor_writeout = json.dumps(donor_sort, sort_keys=True, indent=4)

donor_out = open('index/donor-index.json', 'wb')
donor_out.writelines(donor_writeout)
donor_out.close()


##########################
# Process Focus Area index
# Open index csv
focus = csv.DictReader(open('csv/undp-focus-area-index.csv', 'rb'), delimiter = ',', quotechar = '"')
# Sort file
focus_sort = sorted(focus, key = lambda x: x['id'])

row_count = 0
for row in focus_sort:
    row_count = row_count + 1

print "Processing..."
print "Processed %d rows" % row_count
focus_writeout = json.dumps(focus_sort, sort_keys=True, indent=4)

focus_out = open('index/focus-area-index.json', 'wb')
focus_out.writelines(focus_writeout)
focus_out.close()


##########################
# Process Operating Unit index
# Open index csv
ou = csv.DictReader(open('csv/undp-operating-unit-index.csv', 'rb'), delimiter = ',', quotechar = '"')
# Sort file
ou_sort = sorted(ou, key = lambda x: x['id'])

row_count = 0
for row in ou_sort:
    row_count = row_count + 1

print "Processing..."
print "Processed %d rows" % row_count
ou_writeout = json.dumps(ou_sort, sort_keys=True, indent=4)

ou_out = open('index/operating-unit-index.json', 'wb')
ou_out.writelines(ou_writeout)
ou_out.close()


##########################
# Process Corporate Outcome index
# Open index csv
outcome = csv.DictReader(open('csv/undp-outcome-index.csv', 'rb'), delimiter = ',', quotechar = '"')
# Sort file
outcome_sort = sorted(outcome, key = lambda x: x['id'])

row_count = 0
for row in outcome_sort:
    row_count = row_count + 1

print "Processing..."
print "Processed %d rows" % row_count
outcome_writeout = json.dumps(outcome_sort, sort_keys=True, indent=4)

outcome_out = open('index/outcome-index.json', 'wb')
outcome_out.writelines(outcome_writeout)
outcome_out.close()
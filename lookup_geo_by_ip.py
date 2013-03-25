import sys
import geoip
import cx_Oracle

orp_db = 'usr/pwd@host.com.au:1521/service'

sql_template = """
select trunc(occurred_at), ip_address, count(*)
from primary_event partition (%s)
--where classified_by_rule_id is NOT null --CLASSIFIED
where classified_by_rule_id is null -- NO_RULES
group by trunc(occurred_at), ip_address
having count(*) > 20
order by 1
"""

def main(argv):
	test_mode = False
	sql_param = ''

	if len(argv) >= 1:
		out_filename = argv[0]

		if len(argv) > 1:
			sql_param = argv[1]

			if len(argv) > 2:
				if argv[2] == '-t' or argv[1] == '--test':
					test_mode = True
	else:
		out_filename = raw_input('Params: output_filename [ql_param] [test_or_not]')

	sql = sql_template % sql_param

	print 'connecting to DB...'
	conn = cx_Oracle.connect(orp_db)

	print 'executing DB query:\n', sql

	cursor = conn.cursor()
	cursor.execute(sql)

	out_file = open(out_filename, 'w')

	print 'writing lookup results...'
	num_records = 0

	#Quick TEST
	if test_mode:
		for _ in range(10):
			row = cursor.fetchone()
			write_line(row, out_file)
			num_records += 1
	#ALL RECORDS
	else:
		rows = cursor.fetchall()
		for row in rows:
			write_line(row, out_file)
			num_records += 1

	out_file.close()
	conn.close()

	print "wrote %d records!\n\n" % num_records

def write_line(in_row, out):
	date = in_row[0]
	ip = in_row[1]
	count = in_row[2]
	country = geoip.country(ip)
	if country == '':
		country = '--'

	line = "%s,%s,%s,%d\n" % (date.strftime('%Y-%m-%d'), ip, country, count)
	out.write(line)


if __name__ == "__main__":
   main(sys.argv[1:])

import os

command_template = 'lookup_geo_by_ip.py %s %s'
partition_month = 'pn201208'
# output_dir = './output/classified/'
output_dir = './output/no_rules/'
start_day = 1
end_day = 24

print 'batch: ', command_template, partition_month, 'start_day=', start_day, 'end_day=', end_day

for day in range(start_day, end_day+1):
	partition = partition_month + ("%02d" % day)
	command = command_template % (output_dir + partition + '.csv', partition)
	print 'running:', command
	os.system('python ' + command)





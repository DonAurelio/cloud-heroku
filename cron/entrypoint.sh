#!/bin/bash

cronfile=/etc/cron.d/cron

rm -f cron.log
rm -f $cronfile

mkfifo cron.log

cat /dev/null > $cronfile
for cronvar in ${!CRON_*}; do
	cronvalue=${!cronvar}
	echo "Installing $cronvar"
	echo "$cronvalue >> /usr/src/app/cron.log 2>&1" >> $cronfile
done
echo >> $cronfile # Newline is required

# Run the cron when the container starts
cron

# Print the output
# tail -f cron.log
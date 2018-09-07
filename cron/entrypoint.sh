#!/bin/bash

cronfile=/etc/cron.d/cron

rm -f /usr/src/app/cron.log
rm -f $cronfile

# mkfifo /usr/src/app/cron.log
touch /usr/src/app/cron.log

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
tail -f /usr/src/app/cron.log
# watch /usr/src/app/cron.log
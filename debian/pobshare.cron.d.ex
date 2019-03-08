#
# Regular cron jobs for the pobshare package
#
0 4	* * *	root	[ -x /usr/bin/pobshare_maintenance ] && /usr/bin/pobshare_maintenance

#!/usr/bin/python

import logging
import os

MOTIONCAM_PATH='/var/lib/motion'

def deleteOldFiles():
	global MOTIONCAM_PATH
	now = time.time()
	cutoff = now - (1 * 86400)  # 1 day

	files = os.listdir(MOTIONCAM_PATH)
	for xfile in files:
			if os.path.isfile( MOTIONCAM_PATH+ "/" + xfile ):
					t = os.stat( MOTIONCAM_PATH+ "/" + xfile )
					c = t.st_ctime

					# delete file if older than 1 day
					if c < cutoff:
							os.remove(MOTIONCAM_PATH + "/" + xfile)


logging.basicConfig(filename='/var/log/motionCam.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.INFO)
logging.info('motion detected')

os.chdir(MOTIONCAM_PATH)
files = filter(os.path.isfile, os.listdir(MOTIONCAM_PATH))
files = [os.path.join(MOTIONCAM_PATH, f) for f in files] # add path to each file
files.sort(key=lambda x: os.path.getmtime(x))
logging.info(files[0])




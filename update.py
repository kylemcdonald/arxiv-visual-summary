#!/usr/bin/env python
import feedparser
import subprocess
import dateutil.parser
import pickle
import json
import sys
import re
import os

def mkdirp(dirname):
	subprocess.call(['mkdir', '-p', dirname])

def get_matches(dirname, extensions):
	for root, dirnames, filenames in os.walk(dirname):
		for filename in filenames:
			lower = filename.lower()
			for extension in extensions:
				if lower.endswith(extension):
					yield os.path.join(root, filename)


rss_url = 'http://export.arxiv.org/rss/cs'
doc = feedparser.parse(rss_url)
cur_update = doc['date']
prev_update = None
memory_file = 'memory.pkl'
try:
	with open(memory_file, 'r') as f:
		prev_update = pickle.load(f)
except IOError:
	pass
if prev_update != None and prev_update == cur_update:
	print 'Not updating.'
	sys.exit(0)
print 'Updating.'
with open(memory_file, 'w') as f:
	pickle.dump(cur_update, f)

date_id = dateutil.parser.parse(cur_update).strftime('%d%m%y')
mkdirp('metadata')
with open('metadata/' + date_id + '.json', 'w') as f:
	json.dump(doc['items'], f)

cache_dir = '.cache/'
image_dir = 'images/' + date_id + '/'
mkdirp(image_dir)
extensions = ['pdf', 'jpg', 'jpeg', 'gif', 'png', 'eps']
for item in doc['items']:
	title = item['title']
	if re.search('arXiv:.+v1', title) is None:
		print 'Skipping ' + title
		continue
	print 'Downloading ' + title
	url = item['link']
	source_url = re.sub('abs', 'e-print', url)
	item_id = re.sub('.+abs/', '', url)
	tar_file = cache_dir + item_id + '.tar.gz'
	print 'Processing ' + url + ' / ' + item_id + ' / ' + source_url
	subprocess.call(['curl', '-L', '-o', tar_file, source_url])
	subprocess.call(['tar', '-x', '-f', tar_file, '-C', cache_dir])
	subprocess.call(['rm', tar_file])
	mkdirp(cache_dir)
	for i, filename in enumerate(get_matches(cache_dir, extensions)):
		print '\t' + filename
		output_name = image_dir + '{}_{}.png'.format(item_id, i)
		subprocess.call(['convert', filename, '-resize', '65536@', output_name])
	subprocess.call(['rm', '-rf', cache_dir])
subprocess.call(['fdupes', '-dN', image_dir])

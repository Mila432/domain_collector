# -*- coding: utf-8 -*-
from datetime import datetime
import functools
import hashlib
import io
import os
import re
import requests
import sys
import time
import zipfile

def save(data,file):
	with io.open(file, 'a', encoding='utf8') as thefile:
		thefile.write('%s\n'%unicode(data))

def sha256_file(file_path,chunk_size=65336):
	assert isinstance(chunk_size, int) and chunk_size > 0
	digest = hashlib.sha256()
	with open(file_path, 'rb') as f:
		[digest.update(chunk) for chunk in iter(functools.partial(f.read, chunk_size), '')]
	return digest.hexdigest()

def isUsed(hash):
	try:
		return hash in open('used.txt').read()
	except:
		return False

def rm(f):
	os.remove(f)
	
def dlA():
	r=requests.get('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip',headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'})
	zfile = open('tmp_a.zip', 'wb')
	zfile.write(r.content)
	zfile.close()
	hash=sha256_file('tmp_a.zip')
	if not isUsed(hash):
		zip_ref = zipfile.ZipFile('tmp_a.zip', 'r')
		zip_ref.extract('top-1m.csv')
		zip_ref.close()
		work=[]
		with open('top-1m.csv') as f:
			content = f.readlines()
			content = [x.strip().split(',')[-1] for x in content]
			print len(content)
			save('\n'.join(content),datetime.now().strftime('%Y%m%d_%H_%M_alexa.txt'))
		save(hash,'used.txt')
		rm('top-1m.csv')
	rm('tmp_a.zip')

def dlU():
	r=requests.get('http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip',headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'})
	zfile = open('tmp_u.zip', 'wb')
	zfile.write(r.content)
	zfile.close()
	hash=sha256_file('tmp_u.zip')
	if not isUsed(hash):
		zip_ref = zipfile.ZipFile('tmp_u.zip', 'r')
		zip_ref.extract('top-1m.csv')
		zip_ref.close()
		work=[]
		with open('top-1m.csv') as f:
			content = f.readlines()
			content = [x.strip().split(',')[-1] for x in content]
			print len(content)
			save('\n'.join(content),datetime.now().strftime('%Y%m%d_%H_%M_umbrella.txt'))
		save(hash,'used.txt')
		rm('top-1m.csv')
	rm('tmp_u.zip')

def dlM():
	r=requests.get('http://downloads.majestic.com/majestic_million.csv',headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'})
	work=[]
	zfile = open('tmp_m.csv', 'wb')
	zfile.write(r.content)
	zfile.close()
	hash=sha256_file('tmp_m.csv')
	if not isUsed(hash):
		for line in r.content.split('\n'):
			if '.' in line:
				work.append(line.split(',')[2])
		save(hash,'used.txt')
		save('\n'.join(work[1:]),datetime.now().strftime('%Y%m%d_%H_%M_majestic.txt'))
	rm('tmp_m.csv')
	
def getW():
	for i in os.listdir('.'):
		if 'txt' == i.split('.')[-1] and not 'used' in i:
			yield i

def m():
	wor=[]
	for fi in getW():
		with open(fi) as f:
			print 'working with %s'%(fi)
			for line in f:
				try:
					line=re.sub('.*,','',line.rstrip())
					wor.append(line.encode('utf-8'))
				except:
					continue
	with_du= len(wor)
	print with_du
	wor=list(set(wor))
	print 'removed %s dups'%(with_du-len(wor))
	try:
		rm('clean.csv')
	except:
		pass
	save('\n'.join(wor),'clean.csv')

if __name__ == "__main__":
	while(1):
		try:
			print 'hello'
			dlA()
			print 'done alexa'
			dlM()
			print 'done majestic'
			dlU()
			print 'done umbrella'
			m()
		except:
			pass
		time.sleep(14400)
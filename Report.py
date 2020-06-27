

#########################################################
# Name           : Facebook Auto Report <cookie method>  #
# File           : report.py                             #
# Author         : renairu                               #
# Github         : https://github.com/renairu            #
# Facebook       : https://www.facebook.com/renalawaw    #
# Telegram       : https://t.me/jemb0t                   #
# Python version : 2.7                                   #
#########################################################

import requests, os, sys, re
from bs4 import BeautifulSoup as parser
from multiprocessing.pool import ThreadPool

session=requests.session()

os.system('clear')
base_url='https://mbasic.facebook.com'

class Report(object):
	def __init__(self, url):
		self.base_url=url
		self.post=[]
		self.sukses=0
		self.gagal=0
		self.loop=0

	def sessionLog(self):
		config={}
		cookie=open('sess.log', 'r').read()
		config['cookie']={
			'cookie': cookie
		}
		config['ua']={
			'User-Agent':'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko; googleweblight) Chrome/38.0.1025.166 Mobile Safari/535.19'
		}
		return config

	def requestGet(self, url):
		return session.get(url, headers=self.sessionLog()['ua'], cookies=self.sessionLog()['cookie']).text.encode('utf-8')

	def requestPost(self, url, data):
		return session.post(url, headers=self.sessionLog()['ua'], cookies=self.sessionLog()['cookie'], data=data).text.encode('utf-8')

	def getPostProfile(self, url):
		stop=False
		while True:
			response=self.requestGet(url)
			bs=parser(response, 'html.parser')
			for x in bs.find_all('a', string='Cari Dukungan atau Laporkan Postingan', href=True):
				self.post.append(self.base_url+x['href'])
				if len(self.post)==self.max or len(self.post) > self.max:
					stop=True
					break
			sys.stdout.write('\r  \033[1;93m[*] Mengambil postingan %s/%s ' %(str(len(self.post)), str(self.max)))
			sys.stdout.flush()
			if stop==False:
				if 'Lihat Berita Lain' in str(bs):
					next=bs.find("a", string="Lihat Berita Lain")["href"]
					url=self.base_url+next
				else:break
			else:break

	def getPostGroup(self, url):
		stop=False
		while True:
			response=self.requestGet(url)
			bs=parser(response, 'html.parser')
			for x in bs.find_all('a', string='Lainnya', href=True):
				self.post.append(self.base_url+x['href'])
				if len(self.post)==self.max or len(self.post) > self.max:
					stop=True
					break
			sys.stdout.write('\r  \033[1;93m[*] Mengambil postingan %s/%s ' %(str(len(self.post)), str(self.max)))
			sys.stdout.flush()
			if stop==False:
				if 'Lihat Postingan Lainnya' in str(bs):
					next=bs.find("a", string="Lihat Postingan Lainnya")["href"]
					url=self.base_url+next
				else:break
			else:break

	def getPostFp(self, url):
		stop=False
		while True:
			response=self.requestGet(url)
			bs=parser(response, 'html.parser')
			for x in bs.find_all('a', string='Cari Dukungan atau Laporkan Postingan', href=True):
				self.post.append(self.base_url+x['href'])
				if len(self.post)==self.max or len(self.post) > self.max:
					stop=True
					break
			for x in bs.find_all('a', string='Cari Dukungan atau Laporkan Video', href=True):
				self.post.append(self.base_url+x['href'])
				if len(self.post)==self.max or len(self.post) > self.max:
					stop=True
					break
			sys.stdout.write('\r  \033[1;93m[*] Mengambil postingan %s/%s ' %(str(len(self.post)), str(self.max)))
			sys.stdout.flush()
			if stop==False:
				if 'Tampilkan lainnya' in str(bs):
					next=bs.find("a", string="Tampilkan lainnya")["href"]
					url=self.base_url+next
				else:break
			else:break

	def daftarGroup(self):
		idg=[]
		print('')
		response=self.requestGet(self.base_url+'/groups/?seemore')
		bs=parser(response, 'html.parser')
		for x in bs.find_all('li'):
			href=x.find('a')
			id = re.findall('/groups/(.*?)\?', href['href'])[0]
			idg.append(id)
			print('  \033[1;93m[-] %s \033[1;92m###\033[1;93m %s \033[0m'%(str(id), str(href.text.encode('utf-8'))))
		if len(idg)==0:
			print('  \033[1;91m[!] Anda belum bergabung dengan grups\033[0m')
		exit(0)

	def report1(self, args):
		try:
			response=self.requestGet(args)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			form = {
				'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'tag':'hate_speech'
			}
			response=self.requestPost(self.base_url+action, form)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			form = {
				'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'tag':'hate_speech_something_else'
			}
			response=self.requestPost(self.base_url+action, form)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			if 'RESOLVE_PROBLEM_REDIRECT' in str(bs):
				form = {
					'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'RESOLVE_PROBLEM_REDIRECT'
				}
				response=self.requestPost(self.base_url+action, form)
				bs=parser(response, 'html.parser')
				fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
				jazoest=bs.find('input', {'name':'jazoest'})['value']
				for x in bs('form'):action=x['action']
				form = {
					'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'offensive'
				}
				response=self.requestPost(self.base_url+action, form)
				bs=parser(response, 'html.parser')
				fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
				jazoest=bs.find('input', {'name':'jazoest'})['value']
				for x in bs('form'):action=x['action']
				if 'Apa yang salah dengan foto ini?' in str(bs):
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'annoying'
					}
					response=self.requestPost(self.base_url+action, form)
					bs=parser(response, 'html.parser')
					fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
					jazoest=bs.find('input', {'name':'jazoest'})['value']
					for x in bs('form'):action=x['action']
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'REPORT_CONTENT'
					}
					response=self.requestPost(self.base_url+action, form)
					if 'Anda telah mengirimkan laporan.' in str(response): self.sukses+=1
					else: self.gagal+=1
				elif 'Apa yang salah dengan kiriman ini?' in str(bs):
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'hatespeech'
					}
					response=self.requestPost(self.base_url+action, form)
					bs=parser(response, 'html.parser')
					fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
					jazoest=bs.find('input', {'name':'jazoest'})['value']
					for x in bs('form'):action=x['action']
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'individual'
					}
					response=self.requestPost(self.base_url+action, form)
					bs=parser(response, 'html.parser')
					fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
					jazoest=bs.find('input', {'name':'jazoest'})['value']
					for x in bs('form'):action=x['action']
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'harassing_someone_else'
					}
					response=self.requestPost(self.base_url+action, form)
					bs=parser(response, 'html.parser')
					fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
					jazoest=bs.find('input', {'name':'jazoest'})['value']
					for x in bs('form'):action=x['action']
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'REPORT_CONTENT'
					}
					response=self.requestPost(self.base_url+action, form)
					if 'Anda telah mengirimkan laporan.' in str(response): self.sukses+=1
					else: self.gagal+=1
				elif 'Apa yang salah dengan postingan ini?' in str(bs):
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'hatespeech'
					}
					response=self.requestPost(self.base_url+action, form)
					bs=parser(response, 'html.parser')
					fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
					jazoest=bs.find('input', {'name':'jazoest'})['value']
					for x in bs('form'):action=x['action']
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'againstbelief'
					}
					response=self.requestPost(self.base_url+action, form)
					bs=parser(response, 'html.parser')
					fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
					jazoest=bs.find('input', {'name':'jazoest'})['value']
					for x in bs('form'):action=x['action']
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'REPORT_CONTENT'
					}
					response=self.requestPost(self.base_url+action, form)
					if 'Anda telah mengirimkan laporan.' in str(response): self.sukses+=1
					else: self.gagal+=1
				else: self.gagal+=1
			elif 'FRX_PROFILE_REPORT_CONFIRMATION' in str(bs):
				form = {
					'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'FRX_PROFILE_REPORT_CONFIRMATION'
				}
				response=self.requestPost(self.base_url+action, form)
				bs=parser(response, 'html.parser')
				fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
				jazoest=bs.find('input', {'name':'jazoest'})['value']
				for x in bs('form'):action=x['action']
				form = {
					'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'checked':'yes', 'action':'Laporkan'
				}
				response=self.requestPost(self.base_url+action, form)
				if 'Dikirimkan ke Facebook untuk Ditinjau' in str(response): self.sukses+=1
				else: self.gagal+=1
			else: self.gagal+=1
		except: self.gagal+=1
		self.loop+=1
		sys.stdout.write('\r  \033[1;93m[*] Prosess %s/%s sukses:-%s gagal:-%s\033[0m  '%(str(self.loop), str(len(self.post)), str(self.sukses), str(self.gagal)))
		sys.stdout.flush()

	def report2(self, args):
		try:
			response=self.requestGet(args)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			form = {
				'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'RESOLVE_PROBLEM'
			}
			response=self.requestPost(self.base_url+action, form)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			form = {
				'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'tag':'hate_speech'
			}
			response=self.requestPost(self.base_url+action, form)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			form = {
				'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'tag':'hate_speech_something_else'
			}
			response=self.requestPost(self.base_url+action, form)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			if 'RESOLVE_PROBLEM_REDIRECT' in str(bs):
				form = {
					'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'RESOLVE_PROBLEM_REDIRECT'
				}
				response=self.requestPost(self.base_url+action, form)
				bs=parser(response, 'html.parser')
				fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
				jazoest=bs.find('input', {'name':'jazoest'})['value']
				for x in bs('form'):action=x['action']
				form = {
					'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'offensive'
				}
				response=self.requestPost(self.base_url+action, form)
				bs=parser(response, 'html.parser')
				fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
				jazoest=bs.find('input', {'name':'jazoest'})['value']
				for x in bs('form'):action=x['action']
				if 'Apa yang salah dengan foto ini?' in str(bs):
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'annoying'
					}
					response=self.requestPost(self.base_url+action, form)
					bs=parser(response, 'html.parser')
					fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
					jazoest=bs.find('input', {'name':'jazoest'})['value']
					for x in bs('form'):action=x['action']
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'REPORT_CONTENT'
					}
					response=self.requestPost(self.base_url+action, form)
					if 'Dikirimkan ke Facebook untuk Ditinjau' in str(response): self.sukses+=1
					else: self.gagal+=1
				elif 'Apa yang salah dengan kiriman ini?' in str(bs):
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'hatespeech'
					}
					response=self.requestPost(self.base_url+action, form)
					bs=parser(response, 'html.parser')
					fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
					jazoest=bs.find('input', {'name':'jazoest'})['value']
					for x in bs('form'):action=x['action']
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'individual'
					}
					response=self.requestPost(self.base_url+action, form)
					bs=parser(response, 'html.parser')
					fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
					jazoest=bs.find('input', {'name':'jazoest'})['value']
					for x in bs('form'):action=x['action']
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'harassing_someone_else'
					}
					response=self.requestPost(self.base_url+action, form)
					bs=parser(response, 'html.parser')
					fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
					jazoest=bs.find('input', {'name':'jazoest'})['value']
					for x in bs('form'):action=x['action']
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'REPORT_CONTENT'
					}
					response=self.requestPost(self.base_url+action, form)
					if 'Dikirimkan ke Facebook untuk Ditinjau' in str(response): self.sukses+=1
					else: self.gagal+=1
				elif 'Apa yang salah dengan postingan ini?' in str(bs):
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'hatespeech'
					}
					response=self.requestPost(self.base_url+action, form)
					bs=parser(response, 'html.parser')
					fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
					jazoest=bs.find('input', {'name':'jazoest'})['value']
					for x in bs('form'):action=x['action']
					form = {
						'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'REPORT_CONTENT'
					}
					response=self.requestPost(self.base_url+action, form)
					if 'Dikirimkan ke Facebook untuk Ditinjau' in str(response): self.sukses+=1
					else: self.gagal+=1
				else: self.gagal+=1
			elif 'FRX_PROFILE_REPORT_CONFIRMATION' in str(bs):
				form = {
					'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'FRX_PROFILE_REPORT_CONFIRMATION'
				}
				response=self.requestPost(self.base_url+action, form)
				bs=parser(response, 'html.parser')
				fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
				jazoest=bs.find('input', {'name':'jazoest'})['value']
				for x in bs('form'):action=x['action']
				form = {
					'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'checked':'yes', 'action':'Laporkan'
				}
				response=self.requestPost(self.base_url+action, form)
				if 'Dikirimkan ke Facebook untuk Ditinjau' in str(response): self.sukses+=1
				else: self.gagal+=1
			else: self.gagal+=1
		except: self.gagal+=1
		self.loop+=1
		sys.stdout.write('\r  \033[1;93m[*] Prosess %s/%s sukses:-%s gagal:-%s\033[0m  '%(str(self.loop), str(len(self.post)), str(self.sukses), str(self.gagal)))
		sys.stdout.flush()

	def report3(self, args):
		try:
			response=self.requestGet(args)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			form = {
				'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'tag':'hate_speech'
			}
			response=self.requestPost(self.base_url+action, form)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			form = {
				'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'tag':'hate_speech_something_else'
			}
			response=self.requestPost(self.base_url+action, form)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			if 'RESOLVE_PROBLEM_REDIRECT' in str(bs):
				form = {
					'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'RESOLVE_PROBLEM_REDIRECT'
				}
				response=self.requestPost(self.base_url+action, form)
				bs=parser(response, 'html.parser')
				fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
				jazoest=bs.find('input', {'name':'jazoest'})['value']
				for x in bs('form'):action=x['action']
				form = {
					'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'offensive'
				}
				response=self.requestPost(self.base_url+action, form)
				bs=parser(response, 'html.parser')
				fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
				jazoest=bs.find('input', {'name':'jazoest'})['value']
				for x in bs('form'):action=x['action']
				form = {
					'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'pornography'
				}
				response=self.requestPost(self.base_url+action, form)
				bs=parser(response, 'html.parser')
				fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
				jazoest=bs.find('input', {'name':'jazoest'})['value']
				for x in bs('form'):action=x['action']
				form = {
					'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'REPORT_CONTENT'
				}
				response=self.requestPost(self.base_url+action, form)
				if 'Dikirimkan ke Facebook untuk Ditinjau' in str(response): self.sukses+=1
				else: self.gagal+=1
			elif 'FRX_PROFILE_REPORT_CONFIRMATION' in str(bs):
				form = {
					'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'FRX_PROFILE_REPORT_CONFIRMATION'
				}
				response=self.requestPost(self.base_url+action, form)
				bs=parser(response, 'html.parser')
				fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
				jazoest=bs.find('input', {'name':'jazoest'})['value']
				for x in bs('form'):action=x['action']
				form = {
					'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'checked':'yes', 'action':'Laporkan'
				}
				response=self.requestPost(self.base_url+action, form)
				if 'Dikirimkan ke Facebook untuk Ditinjau' in str(response): self.sukses+=1
				else: self.gagal+=1
			else: self.gagal+=1
		except: self.gagal+=1
		self.loop+=1
		sys.stdout.write('\r  \033[1;93m[*] Prosess %s/%s sukses:-%s gagal:-%s\033[0m  '%(str(self.loop), str(len(self.post)), str(self.sukses), str(self.gagal)))
		sys.stdout.flush()

	def profileReport(self):
		id=str(raw_input('\n  \033[1;93m[*] Masukan ID target: '))
		self.max=int(raw_input('  \033[1;93m[*] Berapa banyak (ex:10): '))
		response=self.requestGet(self.base_url+'/'+id)
		bs=parser(response, 'html.parser')
		if 'Halaman Tidak Ditemukan' in str(bs) or 'Konten Tidak Ditemukan' in str(bs):
			exit('\n  \033[1;91m[!] Profile tidak ditemukan\033[0m')
		url=self.base_url+'/'+id+'?v=timeline'
		self.getPostProfile(url)
		if len(self.post) < self.max:
			print('\n  \033[1;93m[*] Hanya bisa mengambil %s postingan'%(str(len(self.post))))
		print('\n  \033[1;93m[*] Melaporkan profile \033[1;91m%s\033[0m '%bs.title.text)
		try:
			tombol=bs.find('a', string='Lainnya')['href']
			response=self.requestGet(self.base_url+tombol)
			tombol=bs.find('a', string='Cari Dukungan atau Laporkan Profil')['href']
			response=self.requestGet(self.base_url+tombol)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			form = {
				'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'tag':'profile_fake_name'
			}
			response=self.requestPost(self.base_url+action, form)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			form = {
				'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'FRX_PROFILE_REPORT_CONFIRMATION'
			}
			response=self.requestPost(self.base_url+action, form)
			bs=parser(response, 'html.parser')
			for x in bs('form'):action=x['action']
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			form = {
				'fb_dtsg':fb_dtsg, 'jazoest':jazoest,
				'checked':'yes', 'action':'Laporkan'
			}
			self.requestPost(self.base_url+action, form)
			print('  \033[1;92m[*] Berhasil dilaporkan')
		except:print('  \033[1;91m[!] Gagal :(\033[0m')
		if len(self.post)==0:
			exit('  \033[1;91m[!] Tidak ada post untuk dilaporkan :(\033[0m')
		print('  \033[1;93m[*] Mulai melaporkan postingan...')
		m=ThreadPool(10)
		m.map(self.report1, self.post)
		exit('\n  \033[1;93m[*] Done\033[0m')

	def groupReport(self):
		print('\n  \033[1;91m(?) Anda harus bergabung dengan group target.')
		id=str(raw_input('\n  \033[1;93m[*] Masukan ID groups: '))
		self.max=int(raw_input('  \033[1;93m[*] Berapa banyak (ex:10): '))
		response=self.requestGet(self.base_url+'/groups/'+id+'?view=info')
		bs=parser(response, 'html.parser')
		if 'Halaman Tidak Ditemukan' in str(bs) or 'Konten Tidak Ditemukan' in str(bs):
			exit('\n  \033[1;91m[!] Group tidak ditemukan\033[0m')
		url=self.base_url+'/groups/'+id
		self.getPostGroup(url)
		if len(self.post) < self.max:
			print('\n  \033[1;93m[*] Hanya bisa mengambil %s postingan'%(str(len(self.post))))
		print('\n  \033[1;93m[*] Melaporkan groups \033[1;91m%s\033[0m '%bs.title.text)
		try:
			tombol=bs.find('a', string='Laporkan Grup')['href']
			response=self.requestGet(self.base_url+tombol)
			bs=parser(response, 'html.parser')
			for x in bs.find_all('a'):
				if '/rapid_report/?' in str(x):
					href=x['href']
					break
			response=self.requestGet(self.base_url+href)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			form = {
				'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'tag':'hate_speech'
			}
			response=self.requestPost(self.base_url+action, form)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			form = {
				'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'REPORT_CONTENT'
			}
			response=self.requestPost(self.base_url+action, form)
			if 'Terima kasih sudah melaporkan grup ini' in str(response):
				print('  \033[1;92m[*] Berhasil dilaporkan')
			else:print('  \033[1;91m[!] Gagal :(\033[0m')
		except:print('  \033[1;91m[!] Gagal :(\033[0m')
		if len(self.post)==0:
			exit('  \033[1;91m[!] Tidak ada post untuk dilaporkan :(\033[0m')
		print('  \033[1;93m[*] Mulai melaporkan postingan...')
		m=ThreadPool(10)
		m.map(self.report2, self.post)
		exit('\n  \033[1;93m[*] Done\033[0m')

	def fpReport(self):
		id=str(raw_input('\n  \033[1;93m[*] Masukan ID fans page: '))
		self.max=int(raw_input('  \033[1;93m[*] Berapa banyak (ex:10): '))
		response=self.requestGet(self.base_url+'/'+id)
		bs=parser(response, 'html.parser')
		if 'Halaman Tidak Ditemukan' in str(bs) or 'Konten Tidak Ditemukan' in str(bs):
			exit('\n  \033[1;91m[!] Fp tidak ditemukan\033[0m')
		url=self.base_url+'/'+id
		self.getPostFp(url)
		if len(self.post) < self.max:
			print('\n  \033[1;93m[*] Hanya bisa mengambil %s postingan'%(str(len(self.post))))
		print('\n  \033[1;93m[*] Melaporkan Fp \033[1;91m%s\033[0m '%bs.title.text)
		try:
			for x in bs.find_all('a'):
				if '/pages/more/' in str(x):
					href=x['href']
					break
			response=self.requestGet(self.base_url+href)
			bs=parser(response, 'html.parser')
			tombol=bs.find('a', string='Cari Dukungan atau Laporkan Halaman')['href']
			response=self.requestGet(self.base_url+tombol)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			form = {
				'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'offensive'
			}
			response=self.requestPost(self.base_url+action, form)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			form = {
				'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'answer':'pornographic'
			}
			response=self.requestPost(self.base_url+action, form)
			bs=parser(response, 'html.parser')
			fb_dtsg=bs.find('input', {'name':'fb_dtsg'})['value']
			jazoest=bs.find('input', {'name':'jazoest'})['value']
			for x in bs('form'):action=x['action']
			form = {
				'fb_dtsg':fb_dtsg, 'jazoest':jazoest,'action_key':'REPORT_CONTENT'
			}
			response=self.requestPost(self.base_url+action, form)
			if 'Dikirimkan ke Facebook untuk Ditinjau' in str(response):
				print('  \033[1;92m[*] Berhasil dilaporkan')
			else:print('  \033[1;91m[!] Gagal :(\033[0m')
		except:print('  \033[1;91m[!] Gagal :(\033[0m')
		if len(self.post)==0:
			exit('  \033[1;91m[!] Tidak ada post untuk dilaporkan :(\033[0m')
		print('  \033[1;93m[*] Mulai melaporkan postingan...')
		m=ThreadPool(10)
		m.map(self.report3, self.post)
		exit('\n  \033[1;93m[*] Done\033[0m')

	def start(self):
		response=self.requestGet(self.base_url)
		if not 'mbasic_logout_button' in str(response):
			os.remove('sess.log')
			sys.exit('  \033[1;91m\n[WARNING] Cookies tidak valid silahkan login kembali\033[0m')
		os.system('clear')
		print(logo)
		print('''   \033[1;93m{ 01 }. Report Profile
   \033[1;93m{ 02 }. Report Group
   \033[1;93m{ 03 }. Report FP
   \033[1;93m{ 04 }. Daftar Groups
   \033[1;93m{ 00 }. Logout
''')
		pil=int(raw_input('  \033[1;97m>> '))
		if pil==1:
			self.profileReport()
		elif pil==2:
			self.groupReport()
		elif pil==3:
			self.fpReport()
		elif pil==4:
			self.daftarGroup()
		elif pil==0:
			os.remove('sess.log')
			exit('\n\033[1;91m  [*] Byee\033[0m')
		else:
			exit("\n  \033[1;91m[!] Pilihan '%s' tidak ada\033[0m"%pil)

if sys.version_info.major !=2:
	sys.exit('\n\033[1;91m  [WARNING] Silahkan gunakan python versi 2\033[0m')

main=Report(base_url)

logo=('''\n\n
  \033[1;93m####################################\033[0m
  \033[1;93m###     \033[1;92mFACEBOOK AUTO REPORT\033[0m     \033[1;93m###
  \033[1;93m####################################\n\033[0m''')

def login():
	try:
		print(logo)
		cookie = open('sess.log','r').read().strip()
		main.start()
	except IOError:
		cookie=str(raw_input('  \033[1;93m[*] Masukan cookies: ')).strip()
		headers={
			'User-Agent':'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko; googleweblight) Chrome/38.0.1025.166 Mobile Safari/535.19',
			'Cookie':cookie
		}
		cookies={
			'Cookie':cookie
		}
		response=requests.get(base_url+'/profile.php', cookies=cookies, headers=headers).text.encode('utf-8')
		if 'mbasic_logout_button' in str(response):
			response=requests.get(base_url+'/language.php', headers=headers, cookies=cookies).text.encode('utf-8')
			bs=parser(response, 'html.parser')
			href=bs.find('a', string='Bahasa Indonesia', href=True)
			try: requests.get(base_url+href['href'], headers=headers, cookies=cookies)
			except: pass
			open('sess.log', 'w').write(cookie.strip())
			main.start()
		else:
			exit('  \033[1;91m[!] Cookie tidak valid.\033[0m')

if __name__ == '__main__':
	try:
		login()
	except Exception as E:
		print("\n  \033[1;91m[!] Error '%s' \033[0m" % str(E))
		exit()

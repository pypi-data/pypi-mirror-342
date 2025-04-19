import bleach
from datetime import datetime
import pytz
import time
from urllib.parse import quote_plus as kwoot, unquote_plus as unkwoot, urlparse
import pymongo
import certifi
import re
import requests
from flask import session, abort, flash, redirect

# General function for type casting
class Casting:
	regex_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

	@classmethod
	def str_(cls, erin, default: str | None='') -> str | None:
		try:
			return str(erin)
		except:
			return default

	@classmethod
	def int_(cls, erin, default: int | None=0) -> int | None:
		try:
			return int(erin)
		except:
			return default

	@classmethod
	def float_(cls, erin, default=0.0) -> float:
		try:
			return float(erin)
		except:
			return default

	@classmethod
	def bool_(cls, erin, default=True) -> bool:
		try:
			return bool(erin)
		except:
			return default

	@classmethod
	def listint_(cls, erin, default=[]):
		try:
			for i in range(len(erin)):
				erin[i] = int(erin[i])
			return erin
		except:
			return default

	@classmethod
	def liststr_(cls, erin, default=[]):
		try:
			for i in range(len(erin)):
				erin[i] = str(erin[i])
			return erin
		except:
			return default

	@classmethod
	def cast(cls, erin, intotype, default=None) -> any:
		if intotype == int:
			if default is None:
				return cls.int_(erin)
			else:
				return cls.int_(erin, default=default)
		elif intotype == float:
			if default is None:
				return cls.float_(erin)
			else:
				return cls.float_(erin, default=default)
		elif intotype == bool:
			if default is None:
				return cls.bool_(erin)
			else:
				return cls.bool_(erin, default=default)
		return str(erin).strip()

	@classmethod
	def typecast_list(cls, l: list, t: type) -> list:
		try:
			return list(map(t, l))
		except Exception as e:
			return []

	@classmethod
	def validate_email(cls, email: str) -> bool:
		if re.fullmatch(cls.regex_email, email):
			return True
		else:
			return False

# General functions for working with time
class Timetools:
	TTIMESTRING = "%Y%m%dT%H00"
	DATETIME_LOCAL = "%Y-%m-%dT%H:%M"
	DATETIMESTRING = "%Y-%m-%d %H:%M:%S"
	DATETIMESTRING_NL = "%d-%m-%Y %H:%M:%S"
	DATESTRING = "%Y-%m-%d"
	DATESTRING_NL = "%d-%m-%Y"
	BIRTH = '1972-02-29'

	# TODO zorgen dat altijd de juiste NL tijd is.

	@classmethod
	def dtlocal_2_ts(cls, tts: str):
		try:
			dt = datetime(
				year=int(tts[0:4]),
				month=int(tts[5:7]),
				day=int(tts[8:10]),
				hour=int(tts[11:13]),
				minute=int(tts[14:16])
			)
			return int(dt.timestamp())
		except:
			return Timetools.td_2_ts(cls.BIRTH)

	@classmethod
	def dtonixzips_2_tms(cls, tts: str):
		try:
			dt = datetime(
				year=int(tts[0:4]),
				month=int(tts[5:7]),
				day=int(tts[8:10]),
				hour=int(tts[11:13]),
				minute=int(tts[14:16]),
				second=int(tts[17:19]),
				microsecond=int(tts[20:])
			)
			return int(dt.timestamp() * 1000)
		except Exception as e:
			return Timetools.td_2_ts(cls.BIRTH) * 1000

	@classmethod
	def td_2_ts(cls, datum: str) -> int:
		# convert date-string yyyy-mm-dd to seconds timestamp
		try:
			dt = datetime(
				year=int(datum[0:4]),
				month=int(datum[5:7]),
				day=int(datum[8:10]),
			)
			return int(dt.timestamp())
		except:
			return Timetools.td_2_ts(cls.BIRTH)

	@classmethod
	def tdtime_2_ts(cls, datumtijd: str) -> int:
		# convert date-string yyyy-mm-dd to seconds timestamp
		try:
			dt = datetime(
				year=int(datumtijd[0:4]),
				month=int(datumtijd[5:7]),
				day=int(datumtijd[8:10]),
				hour=int(datumtijd[11:13]),
				minute=int(datumtijd[14:16]),
				second=int(datumtijd[17:19]),
			)
			return int(dt.timestamp())
		except:
			return Timetools.td_2_ts(cls.BIRTH)

	@classmethod
	def ts_2_td(cls, timest: int, rev=False, withtime=False) -> str:
		# convert seconds to datestring yyyy-mm-dd
		if withtime:
			if rev:
				dstr = cls.DATETIMESTRING
			else:
				dstr = cls.DATETIMESTRING_NL
		else:
			if rev:
				dstr = cls.DATESTRING
			else:
				dstr = cls.DATESTRING_NL
		try:
			return datetime.fromtimestamp(timest, pytz.timezone("Europe/Amsterdam")).strftime(dstr)
		except:
			return ''

	@classmethod
	def now(cls) -> float:
		return time.time()

	@classmethod
	def now_secs(cls) -> int:
		# for normal use
		return int(cls.now())

	@classmethod
	def now_milisecs(cls) -> int:
		# for use in generating unique numbers
		return int(cls.now() * 1000)

	@classmethod
	def now_nanosecs(cls) -> int:
		# not preferred
		return int(cls.now() * 1000000)

	@classmethod
	def ts_2_datetimestring(cls, ts: int|float|None, rev=False, noseconds=False):
		if rev:
			dstr = cls.DATETIMESTRING
		else:
			dstr = cls.DATETIMESTRING_NL
		if noseconds:
			dstr = dstr[:-3]
		if ts is None:
			ts = cls.now()
		if isinstance(ts, int):
			if len(str(ts)) > 11:
				ts = ts / 1000 # nanoseconds
		if not isinstance(ts, float):
			ts = Casting.float_(ts, 0) # adding trailing zero's representing ms and ns
		return datetime.fromtimestamp(ts, pytz.timezone("Europe/Amsterdam")).strftime(dstr)

	@classmethod
	def ts_2_datestring(cls, ts: int | float | None, rev=False):
		if rev:
			dstr = cls.DATESTRING
		else:
			dstr = cls.DATESTRING_NL

		if ts is None:
			ts = cls.now()
		if isinstance(ts, int):
			if len(str(ts)) > 13:
				ts = ts / 1000000  # nanoseconds
			elif len(str(ts)) > 11:
				ts = ts / 1000  # milliseconds
		if not isinstance(ts, float):
			ts = Casting.float_(ts, 0)  # adding trailing zero's representing ms and ns
		return datetime.fromtimestamp(ts, pytz.timezone("Europe/Amsterdam")).strftime(dstr)

	@classmethod
	def now_string(cls) -> str:
		return datetime.fromtimestamp(cls.now(), pytz.timezone("Europe/Amsterdam")).strftime(cls.DATETIMESTRING)
		# return str(datetime.strptime(timestamp, cls.DATETIMESTRING))

	@classmethod
	def datetimenow(cls):
		return datetime.now()

	@classmethod
	def draaiom(cls, erin):
		# changes yyyy-mm-dd into dd-mm-yyyy and vv
		try:
			d = erin.split('-')
			return f'{d[2]}-{d[1]}-{d[0]}'
		except:
			return erin

# General functions for List and Dict manipulation
class ListDicts:
	@staticmethod
	def is_intersect(a: list, b: list) -> bool:
		# returns if values in a are also in b
		try:
			return len(set(a) & set(b)) > 0
		except:
			return False

	@staticmethod
	def all_a_in_b(needles: list, haystack: list) -> bool:
		# checks if all items a are in b.
		# a is the list with required items, b is the list to be checked
		for item in needles:
			if not item in haystack:
				return False
		return True

	@staticmethod
	def sortlistofdicts(lijst: list, sleutel: str|int, reverse=False) -> list:
		return sorted(lijst, key=lambda d: d[sleutel], reverse=reverse)


class IOstuff:
	@classmethod
	def kwoot(cls, erin):
		# also removes double spaces
		erin = re.sub(' +', ' ', erin)
		return kwoot(erin, safe='', encoding='utf-8', errors='replace')

	# ----------------- cleaning input -----------------
	@classmethod
	def normalize(cls, d: dict, empty_record: dict):
		# always gets all fields from empty record
		normalized = dict()
		for key in empty_record:
			if key in d:
				normalized[key] = d[key]
			else:
				normalized[key] = empty_record[key]
		return normalized

	@classmethod
	def unkwoot(cls, erin):
		try:
			return unkwoot(erin)
		except:
			return ''

	@classmethod
	def check_required_keys(cls, keys, reqlist) -> bool:
		# IMP ALWAYS run this before running other defs
		# checks if all required fields are in form
		return ListDicts.all_a_in_b(reqlist, keys)

	@classmethod
	def sanitize(cls, erin):
		return cls.bleken(erin, tags=[])

	@classmethod
	def bleken(cls, erin, tags=[]):
		try:
			erin = bleach.clean(erin, tags=tags, strip=True, strip_comments=True)
		except:
			pass
		if not isinstance(erin, str):
			return ''
		elif erin in ['None', 'none', 'null', 'Null']:
			erin = ''
		return erin

	# ------------- ajax functions ----------------
	@classmethod
	def ajaxify(cls, a: any) -> any:
		def iterate_list(l: list) -> list:
			for i in range(len(l)):
				if isinstance(l[i], dict):
					l[i] = iterate_dict(l[i])
				elif isinstance(l[i], list):
					l[i] = iterate_list(l[i])
				else:
					# single value
					pass
			return l
		def iterate_dict(d: dict) -> dict:
			for key in d.keys():
				if isinstance(d[key], dict):
					d[key] = iterate_dict(d[key])
				elif isinstance(d[key], list):
					d[key] = iterate_list(d[key])
				elif key == '_id':
					d[key] = str(d[key])
				else:
					# single value
					pass
			return d
		if isinstance(a, list):
			a = iterate_list(a)
		elif isinstance(a, dict):
			a = iterate_dict(a)
		# single type value
		else:
			pass
		return a

# ======= as object embedded with data for jinja only =========
class JINJAstuff:
	record = dict()
	def __init__(self, record: dict={}):
		self.record = record

	def __del__(self):
		pass

	# ------------- jinja functions only ----------------
	def _oid(self):
		try:
			return str(self.record['_id'])
		except:
			return ''

	def _kwoot(self, erin):
		# also removes double spaces
		erin = re.sub(' +', ' ', erin)
		return kwoot(erin, safe='', encoding='utf-8', errors='replace')

	def _urlsafe(self, erin):
		regex = re.compile('[^a-zA-Z0-9 ]')
		return regex.sub('', erin).replace('  ', ' ').replace(' ', '-').lower()

	def _has(self, key) -> bool:
		# key is in record
		try:
			return key in self.record
		except:
			return False

	def _is(self, key: str, val: any) -> bool:
		# compares given val with key-val in current record
		if val is None:
			return False
		return val == self.record[key]

	def _in(self, record_key: str, needle: any) -> bool:
		# checks if give value is in val (list, str, dict)
		try:
			return needle in self.record[record_key]
		except:
			return False

	def _try(self, key, default: any = '') -> any:
		# gets a key from an object if possible
		try:
			return self.record[key]
		except:
			return default

	def _trydeeper(self, key, deepkey, default: any=''):
		one = self._try(key, default=default)
		try:
			return one[deepkey]
		except:
			return one

	def _bleach(self, key, default='') -> str:
		# bleach flaptext
		tekst = self._try(key, default='')
		try:
			return bleach.clean(
				tekst,
				tags={'b', 'i', 'em', 'br', 'strong', 'small', 'h1', 'h2', 'h3', 'h4', 'h5'},
			    attributes={},
				protocols={},
				strip=True,
				strip_comments=True
			)
		except:
			return ''

	def _ajaxify(self, a: any) -> any:
		return IOstuff.ajaxify(a)

	def _get_record(self):
		return self.record

# https://codehandbook.org/pymongo-tutorial-crud-operation-mongodb/
# https://pymongo.readthedocs.io/en/stable/examples/timeouts.html
MONGOCONNECT = 'mongodb+srv://cpnitsuser:ip9NQ64UZXT75u3u@cpnitscluster.hkg1w.mongodb.net/?retryWrites=true&w=majority&appName=CpnitsCluster' #os.environ['COOK_MONGO']
class Mongo:
	client = None
	db = None
	col = ''
	whatfor = ''

	def __init__(self, collection: str='users', dbname: str="deebeebros", silent: bool=False):
		self.silent = silent
		self.col = collection
		self.dbname = dbname
		self.connect()

	def __del__(self):
		try:
			self.client.close()
		except:
			pass

	def connect(self):
		self.db = None
		try:
			self.client = pymongo.MongoClient(
				MONGOCONNECT,
				tlsCAFile=certifi.where()
			)
			self.db = self.client[self.dbname]
		except Exception as e:
			print(f"Mongo connect error {e}")
			self.client = self.db = None
		if self.isvalid():
			if not self.silent:
				print(f"Mongo [{self.dbname}] connected [{self.col}]")
		else:
			print(f"Mongo [{self.dbname}] NOT connected [{self.col}]")

	def set_collection(self, col):
		if not self.silent:
			print(f"Mongo collection: [{col}]")
		self.col = col

	def isvalid(self) -> bool:
		return not self.db is None

	def create(self, onedict, onerror = None):
		# returns a dict or onerror
		if not self.isvalid():
			print("Mongo Create not valid")
			return onerror
		try:
			col = self.db[self.col]
			res = col.insert_one(onedict)
			return res
			# return onedict['_id']
		except Exception as e:
			print("Mongo Create:", e)
			return onerror

	def read(self, where={}, select={}, onerror=None) -> list|None|bool:
		# returns a list/dict or onerror
		if not self.isvalid():
			return onerror
		try:
			col = self.db[self.col]
			res = col.find(where, select)
			if res is None:
				return onerror
			return list(res)
		except Exception as e:
			print("mongo read:", e)
			return onerror

	def read_one(self, where={}, select={}, onerror=None):
		if not self.isvalid():
			return onerror

		try:
			res = self.read(where=where, select=select, onerror=onerror)
		except Exception as e:
			return onerror
		if not isinstance(res, list):
			return onerror
		if len(res) != 1:
			# print(f"mongo read_one has no result: {where}")
			return onerror
		else:
			return res[0]

	def update_one(self, where={}, what={}, upsert=False, onerror=None):
		# IMP: returns nmumber of affected rows or onerror
		if not self.isvalid():
			return onerror
		try:
			col = self.db[self.col]
			result = col.update_one(where, what, upsert=upsert)
			# ook nuttig result.raw_result
		except Exception as e:
			print("mongo update:", e)
			return onerror
		else:
			return int(result.matched_count)

	def update_multi(self, where: dict, what: dict, arrayf=None, onerror=None):
		if not self.isvalid():
			return onerror
		try:
			col = self.db[self.col]
			if arrayf is None:
				result = col.update_many(where, what)
			else:
				result = col.update_many(where, what, array_filters=arrayf)
			# ook nuttig result.raw_result
		except Exception as e:
			print("mongo update:", e)
			return onerror
		else:
			return int(result.matched_count)

	def get_pipline(self, pipeline, onerror=None):
		if not self.isvalid():
			return onerror
		try:
			col = self.db[self.col]
			terug = list()
			for r in col.aggregate(pipeline):
				terug.append(r)
			return terug

		except Exception as e:
			print(f'Aggregate Error\n\t{e}')
			return onerror

	def aggregate(self, pipeline, onerror=None):
		return self.get_pipline(pipeline, onerror=onerror)

	def delete_single(self, filter: dict, onerror=False):
		if not self.isvalid():
			return onerror
		try:
			col = self.db[self.col]
			return col.delete_one(filter)
		except Exception as e:
			print("mongo delete single:", e)
			return onerror

	def delete_multi(self, filter: dict|None = None, onerror = False):
		if not self.isvalid():
			return onerror
		try:
			col = self.db[self.col]
			return col.delete_many(filter)
		except Exception as e:
			print("mongo delete multi:", e)
			return onerror

	def get_col(self):
		return self.db[self.col]

class GithubAuth:
	cid = 'Ov23liE43FUTNGtwGoB2'
	cs = '6876e9c14a1df30181c6ee630cd2187aa9d7b905'
	token = None
	alias = ""
	email = ""

	def __init__(self, domain):
		self.domain = domain

	def __str__(self):
		d = self._get()
		return f'<GithubAuth {str(d)}>'

	def set_token(self, token):
		self.token = token

	def get_cid(self):
		return self.cid

	def get_token(self):
		return self.token

	def get_cs(self):
		return self.cs

	def get_request_url(self):
		return f"https://github.com/login/oauth/authorize?client_id={self.cid}"

	def github_post_response(self, code):
		url = self.get_response_url()
		data = self.get_response_data(code)
		headers = self.get_response_headers()

		response = requests.post(
			url,
			data=data,
			headers=headers
		)
		try:
			# catch != 200
			self.token = Casting.str_(response.json().get('access_token'), default='')
		# print('token', oauth2_token)
		except:
			return None, None, None

		# get user data from github
		response = requests.get(
			'https://api.github.com/user',
			headers={
				'Accept': 'application/vnd.github+json',
				'Authorization': 'Bearer ' + self.token,
				'X-GitHub-Api-Version': '2022-11-28',
			},
		)
		try:
			# get !=200
			self.alias = response.json().get('login')
		except:
			return None, None, None

		# get email addresses
		response = requests.get(
			'https://api.github.com/user/public_emails',
			headers={
				'Accept': 'application/vnd.github+json',
				'Authorization': 'Bearer ' + self.token,
				'X-GitHub-Api-Version': '2022-11-28',
			},
		)
		try:
			# get !=200
			# print(response.json())
			self.email = response.json()[0]['email']
		except:
			return None, None, None

		return self.email, self.alias, self.token

	def get_response_url(self):
		return 'https://github.com/login/oauth/access_token'

	def get_response_data(self, code):
		return {
			'client_id': self.cid,
			'client_secret': self.cs,
			'code': code,
			'grant_type': 'authorization_code',
			'redirect_uri': f"{self.domain}/signup/github/response",
		}

	def get_response_headers(self):
		return {'Accept': 'application/json'}

	def get_alias_url(self):
		return 'https://api.github.com/user'

	def get_alias_email_headers(self):
		return {
			'Accept': 'application/vnd.github+json',
			'Authorization': f'Bearer {self.token}',
			'X-GitHub-Api-Version': '2022-11-28',
		}

	def get_email_url(self):
		return 'https://api.github.com/user/public_emails'

	# ============ from here on web stuff ==========
	def get_alias(self):
		return self.alias

	def get_email(self):
		return self.email

	def _get(self):
		return dict(
			alias=self.alias,
			email=self.email,
			token=self.token,
		)

	# ============ from here on session stuff ==========
	def _set(self, u: dict):
		self.alias = u['alias']
		self.email = u['email']
		self.token = u['token']

	def read_session(self):
		return session['auth']

	def from_sesion(self):
		try:
			self.alias = session['auth']['alias']
			self.email = session['auth']['email']
			self.token = session['auth']['token']
			if self.alias is not None and self.alias != "":
				return True
			else:
				self.unset_session()
				return False
		except:
			self.unset_session()
			return False

	def has_session(self):
		if 'auth' in session:
			if 'alias' in session['auth']:
				return True
		return False

	def set_session(self):
		session['auth'] = self._get()

	def unset_session(self):
		try:
			del session['auth']
		except:
			pass

class FlashAbort:
	@classmethod
	def abort(cls, code: int, flm: str, flc: str):
		cls.empty()
		flash(message=flm, category=flc)
		abort(code)

	@classmethod
	def redir(cls, url:str, flm: str, flc: str):
		cls.empty()
		flash(message=flm, category=flc)
		return redirect(url)

	@classmethod
	def empty(cls):
		try:
			session['_flashes'].clear()
		except:
			pass
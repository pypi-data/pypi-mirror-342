import pickle
import sys
from datetime import datetime
import pytz
import time
import urllib.request
import certifi
import ssl
import certifi
from urllib.parse import parse_qs
import requests
import webbrowser
import pyperclip
from colorama import Style, Fore, Back
import os
from inspect import currentframe, getframeinfo
import platformdirs

# _DOMAIN = 'http://127.0.0.1:5000'
_DOMAIN = 'https://deebeebros.com'

class Ins:
	@classmethod
	def info(cls):
		return f"[{cls.script()}|{cls.func()}|{cls.line()}]"

	@classmethod
	def script(cls):
		try:
			return getframeinfo(currentframe()).filename
		except:
			return '-'

	@classmethod
	def func(cls):
		try:
			return currentframe().f_code.co_name
		except:
			return '-'

	@classmethod
	def line(cls):
		try:
			return getframeinfo(currentframe()).lineno
		except:
			return '-'

class ErrorLogMeta(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]

class ErrorLog(metaclass=ErrorLogMeta):
	force = False

	def __init__(self):
		self.path = os.path.join(os.getcwd(), 'deebeebros.log')
		self.add('start log', Timetools.now_string(), first=True)

	def __del__(self):
		try:
			self.close_log()
		except:
			pass

	def close_log(self):
		self.add('end log', Timetools.now_string())

	def set_path(self, path):
		self.path = path

	def add(self, where: str, msg: str, first=False):
		# self.msgs.append([where, msg])
		if first:
			mode = 'w'
		else:
			mode = 'a'
		with open(self.path, mode=mode) as handle:
			handle.write(f"{where}\t{msg}\n")

class Css:
	# uses colorama for creating style in prompt
	@classmethod
	def reset(cls) -> str:
		return f"{Style.RESET_ALL}"

	@classmethod
	def normal(cls, s=None) -> str:
		if s is None:
			return f"{Style.NORMAL}"
		return f"{cls.normal()}{s}{cls.reset()}"

	@classmethod
	def jippie(cls, s=None) -> str:
		if s is None:
			return f"{Fore.BLUE}{Style.BRIGHT}"
		else:
			return f"{cls.jippie()}{s}{cls.reset()}"

	@classmethod
	def bold(cls, s=None) -> str:
		if s is None:
			return f"{Style.BRIGHT}"
		return f"{cls.bold()}{s}{cls.reset()}"

	@classmethod
	def good(cls, s=None) -> str:
		if s is None:
			return f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}"
		return f"{cls.good()}{s}{cls.reset()}"

	@classmethod
	def warning(cls, s=None) -> str:
		if s is None:
			return f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}"
		return f"{cls.warning()}{s}{cls.reset()}"

	@classmethod
	def attention(cls, s=None) -> str:
		# more serious than warn
		if s is None:
			return f"{Back.LIGHTYELLOW_EX}{Fore.BLACK}{Style.BRIGHT}"
		return f"{cls.attention()} {s} {cls.reset()}"

	@classmethod
	def wrong(cls, s=None) -> str:
		if s is None:
			return f"{Fore.LIGHTRED_EX}{Style.BRIGHT}"
		return f"{cls.wrong()}{s}{cls.reset()}"

	@classmethod
	def prompt(cls, s=None) -> str:
		if s is None:
			return f"{Fore.BLACK}{Style.BRIGHT}"
		return f"{cls.prompt()}{s}{cls.reset()}"

	@classmethod
	def log(cls) -> str:
		return f"{Fore.MAGENTA}{Style.NORMAL}"

# General function for type casting
class Casting:
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

class GithubOauth:
	cid = 'Ov23liE43FUTNGtwGoB2'
	cs = '6876e9c14a1df30181c6ee630cd2187aa9d7b905'
	user = None

	def __init__(self):
		self.domain = _DOMAIN
		self.log = ErrorLog()
		self.unset_user()

	def __str__(self):
		ustr = ", ".join(self.user)
		return f"{str}"

	def unset_user(self):
		self.user = dict(
			token=None,
			devicecode=None,
			alias=None,
			email=None,
		)

	def new_connection(self):
		if not self.git_oauth():
			self.print_connection_failed()
			self.unset_user()
			return
		self.print_connection_ok()

	def is_valid(self):
		return not self.user['token'] is None

	def git_oauth(self) -> bool:
		# request for login procedure
		try:
			req = requests.post(self.req_url(), self.req_data())
		except Exception as e:
			self.log.add(Ins.info(), str(e))
			print(Css.wrong(f"Github request not available now. Try again later {Ins.info()}."))
			return False
		try:
			req_params = parse_qs(req.text)
		except Exception as e:
			self.log.add(Ins.info(), str(e))
			print(Css.wrong(f"Github login not available now [368]. Try again later  {Ins.info()}."))
			return False
		# print(req_params, type(req_params))
		self.set_divececode(req_params['device_code'][0])

		# open webbrowser for auth
		vraag = input(Css.normal(f"{Css.attention()} Your Github login code is: {Css.reset()} {req_params['user_code'][0]} {Css.attention()} Copy to clipboard (or quit) [Y/N/Q]? {Css.reset()} "))
		if vraag.lower() == 'q':
			print(Css.warning(f"Leaving so soon?"))
			sys.exit(1)
		if vraag in ['y', 'Y']:
			pyperclip.copy(req_params['user_code'][0])
		print(Css.normal("You will be redirected to the browser to login at Github."), flush=True)
		try:
			webbrowser.open(req_params['verification_uri'][0])
		except Exception as e:
			self.log.add(Ins.info(), str(e))
			print(f"Your webbrowser does not open on demand. Please visit {req_params['verification_uri'][0]} in your browser to login at Github.")

		time.sleep(1)
		vraag = input(f"{Css.attention()} Press [Enter] when ready with Github login: {Css.reset()}")

		# get user token
		try:
			con = requests.post(self.con_url(), self.con_data())
		except Exception as e:
			self.log.add(Ins.info(), str(e))
			print(Css.wrong(f"Github authentication not available now. Try again later  {Ins.info()}."))
			sys.exit(1)
		try:
			con_params = parse_qs(con.text)
		except Exception as e:
			self.log.add(Ins.info(), str(e))
			print(Css.wrong(f"Github authentication not available now. Try again later.  {Ins.info()}"))
			sys.exit(1)

		#print(con_params, type(con_params))
		self.set_token(con_params['access_token'][0])

		self.user['alias'] = self.con_alias()
		if self.user['alias'] is None:
			print(Css.wrong(f"Github authentication not complete [no alias]. Try again later  {Ins.info()}."))
			sys.exit(1)

		self.user['email'] = self.con_email()
		if self.user['email'] is None:
			print(Css.wrong(f"Github authentication not complete [no email]. Try again later  {Ins.info()}."))
			sys.exit(1)

		# create/upsert Mongo record
		self.user = dict(
			email = self.user['email'],
			alias = self.user['alias'],
			devicecode = self.user['devicecode'],
			token = self.user['token'],
			last_auth = Timetools.now_string(),
		)
		# all good
		return True

	def print_connection_ok(self):
		print(Css.good(f"Authentication successful with [{self.user['alias']}] and [{self.user['email']}]."))

	def print_connection_failed(self):
		print(Css.wrong(f"Authentication failed"))

	def get_cid(self):
		return self.cid

	def get_token(self):
		return self.user['token']

	def get_cs(self):
		return self.cs

	def get_devicecode(self):
		return self.user['devicecode']

	def req_url(self):
		return 'https://github.com/login/device/code'

	def req_data(self):
		return {
			'client_id': self.get_cid(),
			'scope': 'user',
		}

	def set_token(self, token):
		self.user['token'] = token

	def set_divececode(self, dc):
		self.user['devicecode'] = dc

	def con_url(self):
		return 'https://github.com/login/oauth/access_token'

	def con_data(self):
		return {
			'client_id': self.get_cid(),
			'device_code': self.get_devicecode(),
			'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
		}

	def con_alias(self):
		# get user data from github
		response = requests.get(
			'https://api.github.com/user',
			headers={
				'Accept': 'application/vnd.github+json',
				'Authorization': f'Bearer {self.get_token()}',
				'X-GitHub-Api-Version': '2022-11-28',
			},
		)
		try:
			# get !=200
			return response.json().get('login')
		except:
			return None

	def con_email(self):
		# get email addresses
		response = requests.get(
			'https://api.github.com/user/public_emails',
			headers={
				'Accept': 'application/vnd.github+json',
				'Authorization': f'Bearer {self.get_token()}',
				'X-GitHub-Api-Version': '2022-11-28',
			},
		)
		try:
			return response.json()[0]['email']
		except:
			return None

	def get_repo_info(self, reponame):
		try:
			unittest_info = GithubJeex().con_repo_path(self.get_token(), reponame)
			unittest_name = unittest_info['name']
			unittest_durl = unittest_info['download_url']
			return unittest_info
		except Exception as e:
			print(f"The test file [{reponame}] does not exist")
			return None

	def get_email(self):
		return self.user['email']

	def get_alias(self):
		return self.user['alias']

	def get_user(self):
		return self.user

	def set_user(self, user):
		self.user = user

class GithubJeex:
	@staticmethod
	def con_repo_list():
		pass

	@staticmethod
	def con_repo_path(token, assignment) -> dict|None:
		log = ErrorLog()
		# gets all the info about a repo
		data = data = {
			"Accept": "application/vnd.github+json",
			"Authorization": f"Bearer {token}",
			"X-GitHub-Api-Version": "2022-11-28",
		}
		url = f'https://api.github.com/repos/jeex/jeex_public/contents/{assignment}'
		try:
			response = requests.get(
				url,
				data
			)
		except Exception as e:
			log.add(Ins.info(), str(e))
			return None
		try:
			return response.json()
		except Exception as e:
			log.add(Ins.info(), str(e))
			return None

	@staticmethod
	def con_repo_download(url, fpath) -> bool:
		log = ErrorLog()
		try:
			with urllib.request.urlopen(url, context=ssl.create_default_context(cafile=certifi.where())) as handle:
				script = handle.read().decode()
			with open(fpath, 'w') as handle:
				handle.write(script)
			return True
		except Exception as e:
			log.add(Ins.info(), str(e))
			return False

class MonApi:
	def __init__(self, gho: GithubOauth):
		self.gho = gho
		self.log = ErrorLog()

	def __str__(self):
		return str(self.gho.get_user())

	def test(self):
		url = f'{_DOMAIN}/api/update_user'
		try:
			response = requests.post(url, json=self.gho.get_user())
		except Exception as e:
			self.log.add(Ins.info(), str(e))
			print(e)
			return
		print(response.status_code)
		print(response.text)

	def local_user(self, luser: dict):
		url = f"{self.gho.domain}/api/local_user"
		try:
			response = requests.post(url, json=luser)
			return response.status_code == 200
		except Exception as e:
			self.log.add(Ins.info(), str(e))
			print(Css.wrong(f"DeeBeeBros users API not available now. Try again later. {Ins.info()}"))
			return False

	def is_user(self) -> bool:
		url = f"{self.gho.domain}/api/check_user"
		user = self.gho.get_user()
		try:
			response = requests.post(url, json=user)
			return response.status_code == 200
		except Exception as e:
			self.log.add(Ins.info(), str(e))
			print(Css.wrong(f"DeeBeeBros users API not available now. Try again later. {Ins.info()}"))
			return False

	# connects to check11 api for addressing Mongo
	def update_user(self) -> bool:
		# sets user after github oauth with email and token
		url = f"{_DOMAIN}/api/update_user"
		user = self.gho.get_user()
		try:
			response = requests.post(url, json=user)
			return response.status_code == 200
		except Exception as e:
			self.log.add(Ins.info(), str(e))
			print(Css.wrong(f"DeeBeeBros users API not available now. Try again later.  {Ins.info()}"))
			return False

	def update_check(self, check: dict) -> bool:
		# API updates/creates check in check db
		user = self.gho.get_user()
		jso = {'user': user['alias'], 'token': user['token'], 'check': check}
		url = f"{_DOMAIN}/api/update_check"
		try:
			response = requests.post(url, json=jso)
			return response.status_code == 200
		except Exception as e:
			self.log.add(Ins.info(), str(e))
			print(Css.wrong(f"DeeBeeBros checks API not available now. Try again later.  {Ins.info()}"))
			return False

class LocalUser:
	_expire = 1000 * 60 * 60 * 48 # twee dagen
	def __init__(self):
		# self._expire = 1000 * 60
		pass

	def expired(self, toens) -> bool:
		nus = Timetools.now_milisecs()
		return toens + self._expire < nus

	# keeps user data locally
	def get_path(self):
		path = platformdirs.user_data_dir("DeeBeeBros.com")
		if not os.path.isdir(path):
			os.makedirs(path)
		return os.path.join(path, "deebeebros_settings.pickle")

	def set(self, d: dict) -> bool:
		# sets user in local settings file
		nus = Timetools.now_milisecs()
		d['nus'] = nus
		try:
			with open(self.get_path(), "wb") as handle:
				pickle.dump(d, handle)
			return True
		except:
			pass
		return False

	def get(self) -> dict | None:
		# gets user from local settings file
		nus = Timetools.now_milisecs()
		try:
			with open(self.get_path(), "rb") as handle:
				d = pickle.load(handle)
			# check if expired
			if self.expired(d['nus']):
				self.remove()
				return None
			return d
		except:
			pass
		return None

	def remove(self):
		try:
			os.remove(self.get_path())
		except:
			pass


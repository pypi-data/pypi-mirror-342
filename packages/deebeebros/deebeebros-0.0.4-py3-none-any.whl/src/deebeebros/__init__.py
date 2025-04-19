import shutil
import sys
import os
import importlib.util
import pathlib
import requests

from prompt_helpers import (
	GithubOauth,
	GithubJeex,
	Casting,
	MonApi,
	Css,
	Timetools,
	ErrorLog,
	Ins,
	LocalUser,
)

dbbpath = str(pathlib.Path(__file__).parent.resolve())
if not dbbpath in sys.path:
	sys.path.insert(0, dbbpath)

_VERSION = '0.0.004'
_APP_NAME = 'deebeebros'
# _DOMAIN = 'http://127.0.0.1:5000'
_DOMAIN = 'https://deebeebros.com'
_DEV = False

def check_version():
	githuburl = "https://raw.githubusercontent.com/jeex/jeex_public/refs/heads/main/deebeebros_version.txt"
	try:
		r = requests.get(githuburl)
	except:
		return
	if r.status_code != 200:
		return
	dbb_version = r.content.decode("utf-8").strip()
	if dbb_version > _VERSION:
		print(f"{Css.warning()}This version is {_VERSION}. Upgrade with newer version {dbb_version} with: {Css.reset()}\n\tpip install deebeebros --upgrade --no-cache-dir")
		sys.exit(1)

def from_args():
	email = experiment = None
	verbose = False
	clear = False
	trace = False
	# results = False
	# forcelog = False
	for arg in sys.argv[1:]:
		if arg == '-v':
			verbose = True
			continue
		if arg == '-c':
			clear = True
			continue
		if arg == '-t':
			trace = True
			continue
		if arg.endswith('.py'):
			experiment = arg
			continue

	return experiment, verbose, trace, clear

def authenticate_user():
	# email = input("What is your email address for Github oAuth? ")
	# full connection procedure for Github
	gho = GithubOauth()
	monapi = MonApi(gho)
	local_user = LocalUser()

	# while busy prevent endless logins by storing user local
	luser = local_user.get()
	if luser is None:
		# no active token in local settings
		gho.new_connection()
		if not gho.is_valid():
			sys.exit(1)
		# update local user
		local_user.set(gho.get_user())

	elif not monapi.local_user(luser):
		# check active token in local settings with API
		gho.new_connection()
		if not gho.is_valid():
			sys.exit(1)
		# update local user
		local_user.set(gho.get_user())
	else:
		# local user
		gho.set_user(luser)
		return gho, monapi, local_user

	# TODO when public
	# if not monapi.is_user():
		# print(Css.warning(f"You're not registered to use DeeBeeBros.com. Visit {_DOMAIN} to register."))
		# sys.exit(1)
	# TODO END

	# user update in database and local
	local_user.set(gho.get_user())
	monapi.update_user()
	return gho, monapi, local_user

def download_unittest(check11pad, experiment):
	unittestname = get_unittest_name(experiment)
	print(f"Downloading unittest file for [{experiment}]...", end="")
	unittest_durl = f'https://raw.githubusercontent.com/jeex/jeex_public/main/{unittestname}'
	if not GithubJeex().con_repo_download(unittest_durl, os.path.join(check11pad, unittestname)):
		print(f" failed")
		sys.exit(1)
	print(Css.good(" ready"))

def get_unittest_name(experiment):
	return f'test_{experiment}'

def upload_test(experiment: str, check11pad: str):
	cwd = os.getcwd()
	source_path = os.path.join(cwd, experiment)
	target_path = os.path.join(check11pad, experiment)
	try:
		shutil.copy(source_path, target_path)
	except:
		print(Css.wrong(f"The file [{experiment}] does not exist in the directory [{cwd}]"))
		sys.exit(1)
	if not os.path.isfile(target_path):
		print(Css.wrong(f"The file [{experiment}] cannot be tested"))
		sys.exit(1)

def load_base_test_class(pad: str):
	try:
		# load basetest class
		specs = importlib.util.spec_from_file_location('base_test', os.path.join(pad, 'base_test.py'))
		# add to sys modules
		sys.modules['base_test'] = importlib.util.module_from_spec(specs)
		# load
		specs.loader.exec_module(sys.modules['base_test'])
	except Exception as e:
		print(Css.wrong("Base Test class is unavailable"))
		sys.exit(1)

def this_test_mod(modpath: str, modname: str):
	try:
		specs = importlib.util.spec_from_file_location(modname, modpath)
		sys.modules[modname] = importlib.util.module_from_spec(specs)
		specs.loader.exec_module(sys.modules[modname])
		return sys.modules[modname]
	except Exception as e:
		print(Css.wrong(f"The module [{modname}.py] cannot be loaded"))
		# print(e)
		sys.exit(1)

def clear_terminal():
	try:
		os.system('cls' if os.name == 'nt' else 'clear')
	except:
		pass

def run():
	log = ErrorLog()
	check_version()
	check11_pad = os.path.join(os.path.dirname(__file__), 'unittests')
	if not os.path.isdir(check11_pad):
		try:
			os.makedirs(check11_pad)
		except Exception as e:
			log.add(Ins.info(), str(e))
			print(Css.wrong('No place for testing in your computer. Contact DeeBeeBros.com'))
			sys.exit(1)

	# read all stuff from command line args
	experiment, verbose, trace, clear, = from_args()

	if clear:
		clear_terminal()

	# check experiment
	if experiment is None:
		print(Css.wrong("No valid experiment in command line args. Use: python deebeebros.py <your_experiment.py>"))
		sys.exit(1)
	cwd = os.getcwd()
	if not os.path.isfile(os.path.join(cwd, experiment)):
		print(Css.wrong(f"Invalid experiment name: [{experiment}] does not exist (in this folder)"))
		sys.exit(1)

	# set user in gho object and build connection with github
	gho, monapi, local_user = authenticate_user()
	if gho is None or monapi is None:
		print(Css.wrong(f"Authentication failed, so no DBB checks. {Ins.info()}"))
		return

	# download unittest, exits if wrong
	download_unittest(check11_pad, experiment)

	# upload the script experiment to unittests folder
	upload_test(experiment, check11_pad)

	# load test mod
	load_base_test_class(os.path.dirname(__file__))
	experiment_path = os.path.join(check11_pad, experiment)
	unittest_path = os.path.join(check11_pad, get_unittest_name(experiment))
	unittest_mod = this_test_mod(unittest_path, get_unittest_name(experiment))

	# start test class
	tm = unittest_mod.RunTest(
		experiment_path,
		experiment,
		verbose,
		trace,
	)
	# print results
	report = tm.get_report()
	percent = tm.get_score_percent()
	# print the report in the terminal
	print(tm)
	print()

	if gho is None or monapi is None:
		print(Css.wrong(f"Update to deebeebros account not possible. {Ins.info()}"))
		return
	# add results to Mongo
	check = {
		'user': gho.get_alias(),
	    'experiment': experiment,
		'checked': Timetools.now_string(),
		'percent': percent,
		'report': report
	}
	if not monapi.update_check(check):
		print(Css.wrong(f"Update to deebeebros account failed. {Ins.info()}"))
		return

	pubtoken = gho.get_token().replace('gho_', '')[::-1]
	print(Css.jippie(f"visit {_DOMAIN}/account to see your results"))
	print()

def testing_api_check(mon, report, percent, experiment):
	check = {
		'user': mon.gho.get_alias(),
		'experiment': experiment,
		'checked': Timetools.now_string(),
		'percent': percent,
		'report': report
	}
	print('update check result', mon.update_check(check))

def testing_api_user():
	# with fake data for skipping Github oauth
	gho = GithubOauth(_DOMAIN)
	gho.user = dict(
		email="dbbtest@jeex.eu",
		alias="jeex_dbb_tester",
		devicecode="1234567890",
		token="gho_jeex_dbb_tester",
		last_auth=Timetools.now_string(),
		# web_token="",
		# first_auth=Timetools.now_string(),
		# web_last_auth="",
	)
	gho.token = gho.user['token']
	gho.alias = gho.user['alias']
	gho.email = gho.user['email']
	gho.devicecode = gho.user['devicecode']
	monapi = MonApi(gho)
	print('update user result', monapi.update_user())
	return monapi

def testing_test():
	# first and test_first must be in unittests folder
	check11_pad = os.path.join(os.path.dirname(__file__), 'unittests')
	experiment = 'first.py'
	verbose = True
	trace = False
	load_base_test_class(os.path.dirname(__file__))
	experiment_path = os.path.join(check11_pad, experiment)
	unittest_path = os.path.join(check11_pad, get_unittest_name(experiment))
	unittest_mod = this_test_mod(unittest_path, get_unittest_name(experiment))

	# start test class
	tm = unittest_mod.RunTest(
		experiment_path,
		experiment,
		verbose,
		trace,
	)
	# print results
	report = tm.get_report()
	percent = tm.get_score_percent()
	print(tm)
	return report, percent, experiment

def testing_down_up_load():
	check11_pad = os.path.join(os.path.dirname(__file__), 'unittests')
	experiment = 'first.py'
	# download unittest, exits if wrong
	download_unittest(check11_pad, experiment)

	# upload the script experiment to unittests folder
	upload_test(experiment, check11_pad)

def heletest():
	log = ErrorLog()
	clear_terminal()
	log.add('poep', [1, 2, 3, 'kak'])
	testing_down_up_load()
	r, p, e = testing_test()
	mon = testing_api_user()
	testing_api_check(mon, r, p, e)

if __name__ == '__main__':
	run()




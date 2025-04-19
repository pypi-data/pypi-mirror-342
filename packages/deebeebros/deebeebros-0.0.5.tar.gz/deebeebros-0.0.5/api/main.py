import bleach
from flask import Flask, jsonify, request, flash, redirect, render_template, session, get_flashed_messages
from flask_helpers import Mongo, Casting, Timetools, JINJAstuff, GithubAuth, ListDicts, FlashAbort
from datetime import timedelta

app = Flask(__name__, static_folder='./static', template_folder='./templates')
app.config['debug'] = False
app.config['SECRET_KEY'] = 'sdjfsldfjsldfjlwifhoiwnfd'
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'lax'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_NAME'] = 'deebeebros_session'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_DOMAIN'] = None
# app.config["CACHE_TYPE"] = "null"

# TODO update_user upsert is nu true, moet false worden als client aanmelding in website klaar is

if app.config['debug']:
	_DOMAIN = 'http://127.0.0.1:5000'
else:
	_DOMAIN = 'https://deebeebros.com'

from ansi2html import Ansi2HTMLConverter
class JinjaReport(JINJAstuff):
	def _report(self):
		conv = Ansi2HTMLConverter()
		if not isinstance(self._try('report'), list):
			return ''
		report = self._try('report')
		eruit = ""
		for r in report:
			r = conv.convert(r)
			r = r.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
			eruit += '<br>' + r
		return eruit


# ============= WEB stuff ============================
@app.get("/")
def home():
	auth = GithubAuth(_DOMAIN)
	return render_template(
		'home.html',
		auth=auth,
	)

@app.get("/privacy")
def privacy():
	auth = GithubAuth(_DOMAIN)
	return render_template(
		'privacy.html',
		auth=auth,
	)

# new is only after first registration
@app.get("/new")
def get_new():
	# for making the check11 account via github, AFTER first oauth
	auth = GithubAuth(_DOMAIN)

	if len(get_flashed_messages()) == 0:
		FlashAbort.abort(404, f'It looks like you have to authenticate with Github first. Goto <a href="{auth.get_request_url()}">Github</a> to login.', "error")

	return render_template(
		'new.html',
		auth=auth,
	)

@app.post("/new")
def post_new():
	auth = GithubAuth(_DOMAIN)
	try:
		voucher = Casting.str_(request.form['voucher-code'], default=None)
		if voucher is None or voucher == '':
			FlashAbort.abort(404, "Your voucher code is invalid", "error")
	except:
		FlashAbort.abort(404, "No voucher code given", "error")

	m = Mongo(collection='users', silent=False)
	user = m.read_one(where={'status': 'new', 'voucher_code': voucher}, onerror=None)
	if user is None:
		FlashAbort.abort(404, f"You're not a known user at DeeBeeBros.com [83].", "error")

	m.set_collection("users")
	m.update_one(
		where={'status': 'new', 'voucher_code': voucher},
		what={'$set': {'status': 'active', 'voucher_code': ''}},
	)
	auth._set(user)
	auth.set_session()
	return FlashAbort.redir("/account", "You successfully registered at DeeBeeBros.com", "success")

@app.get("/account")
def account():
	auth = GithubAuth(_DOMAIN)
	if not auth.has_session():
		return redirect('/#account')
	# set data from session into autho
	auth.from_sesion()

	alias = auth.get_alias()
	m = Mongo(collection='checks', silent=False)
	checks = m.read(where={'user': alias})
	del(m)
	checks = ListDicts.sortlistofdicts(checks, 'checked', reverse=True)
	for i in range(len(checks)):
		checks[i] = JinjaReport(checks[i])

	return render_template(
		'account.html',
		auth=auth,
		j_checks=checks,
	)

@app.get("/account/logoff")
def account_logoff():
	auth = GithubAuth(_DOMAIN)
	auth.unset_session()
	return redirect('/')


# ============= SIGNUP GITHUB stuff ==============================
@app.get("/signup/github/request")
def github_request():
	print('nu ++++++++++++++++++++++++++++')
	auth = GithubAuth(_DOMAIN)

@app.get("/signup/github/response")
def github_response():
	# hier kom je alleen via een Github oauth request
	if not 'code' in request.args:
		del session['user']
		FlashAbort.abort(404, f"Authentication at Github failed [1]", "error")

	code = request.args.get('code')
	auth = GithubAuth(_DOMAIN)
	auth.unset_session()

	email, alias, web_token = auth.github_post_response(code)
	if alias is None:
		FlashAbort.abort(404, f"Authentication at Github failed [2]", "error")

	print('145 alias', email, alias, web_token)

	m = Mongo(collection='users', silent=not app.config['debug'])
	user = m.read_one(where={'alias': alias}, onerror=None)

	print('151 user', user)

	if user is None:
		# first time here
		nus = Timetools.now_string()
		voucher = f"dbb_{Timetools.now_milisecs()}"
		user = dict(
			email=email,
			alias=alias,
			devicecode='',
			token='',
			first_auth=nus,
			last_auth='',
			web_token=web_token,
			web_last_auth=nus,
			status="new",
			voucher_code=f"{voucher}",
		)
		m.set_collection("users")
		if m.update_one(
			where={'alias': alias, 'status': 'new'},
			what={'$set': user},
			upsert=True,
			onerror=None,
		) is None:
			auth.unset_session()
			return redirect('/')
		flash(message=f'Your free voucher code: {voucher}', category='success')
		del(m)
		# no session made yet, because new user
		return redirect('/new')
	else:
		# existing user
		nus = Timetools.now_string()
		what = dict(
			web_token=web_token,
			web_last_auth=nus,
		)
		m.set_collection("users")
		if m.update_one(where={'alias': alias}, what={'$set': what}, upsert=False, onerror=None) is None:
			del(m)
			FlashAbort.abort(404, "Database update failed, login possibly failed, try again later", "error")
	# add user data to auth
	auth._set(user)
	# make a session
	auth.set_session()
	del(m)
	return redirect('/account')



# ============= API stuff ==============================
def normalize_user(d: dict) -> dict|None:
	nec = ['alias', 'email', 'devicecode', 'token']
	for n in nec:
		if not n in d.keys():
			return None
	email = d['email']
	try:
		if not Casting.validate_email(email):
			return None
	except:
		return None
	try:
		alias = bleach.clean(Casting.str_(request.json.get('alias'), default=None))
		token = bleach.clean(Casting.str_(request.json.get('token'), default=None))
		devicecode = bleach.clean(Casting.str_(request.json.get('devicecode'), default=None))
	except:
		return None
	if alias is None or token is None or devicecode is None:
		return None
	user = dict(
		email=email,
		alias=alias,
		token=token,
		devicecode=devicecode,
		last_auth=Timetools.now_string(),
	)
	return user

def normalize_check(d: dict) -> dict|None:
	nec = ['user', 'checked', 'experiment', 'percent', 'report']
	for n in nec:
		if not n in d.keys():
			return None
	return d

@app.post("/api/update_user")
def update_user():
	if not request.is_json:
		return jsonify({"message": "Missing JSON in request"}), 400
	user = normalize_user(request.get_json())
	if user is None:
		return jsonify({"message": "Invalid user data [35]"}), 400

	# TODO veranderen als publiek
	user['status'] = 'active'
	user['voucher_code'] = 'prompt_123456789'

	m = Mongo(collection='users', silent=not app.config['debug'])
	r = m.update_one(where={'alias': user['alias']}, what={'$set': user}, upsert=True, onerror=0)
	del(m)
	if r is None:
		return jsonify({"message": "User update failed"}), 400

	return jsonify({"message": "User update successful"}), 200

@app.post("/api/update_check")
def update_check():
	if not request.is_json:
		return jsonify({"message": "Missing JSON in request"}), 400
	if not 'user' in request.json or not 'check' in request.json or not 'token' in request.json:
		return jsonify({"message": "Missing JSON items in request"}), 400

	alias = Casting.str_(request.json.get('user'), default="").strip()
	if alias == "":
		return jsonify({"message": "Invalid user data [159]"}), 400
	check = normalize_check(request.json.get('check'))
	if check is None:
		return jsonify({"message": "Invalid user data [162]"}), 400
	token = Casting.str_(request.json.get('token'), default="").strip()
	if token == "":
		return jsonify({"message": "Invalid user data [165]"}), 400

	print(alias, token, len(check))

	m = Mongo(collection='users', silent=not app.config['debug'])
	r = m.read_one(where={'alias': alias, 'token': token}, onerror=None)
	if r is None:
		return jsonify({"message": "User check failed"}), 400

	m.set_collection('checks')
	if None is m.update_one(where={'user': alias, 'experiment': check['experiment']}, what={'$set': check}, upsert=True, onerror=None):
		del(m)
		return jsonify({"message": "Check upsert failed"}), 400
	del(m)
	return jsonify({'ok': True}), 200

@app.post("/api/local_user")
def local_user():
	# checks if user with current token is active
	if not request.is_json:
		return jsonify({"message": "Missing JSON in request"}), 400
	user = normalize_user(request.get_json())
	if user is None:
		return jsonify({"message": "Invalid user data [35]"}), 400

	m = Mongo(collection='users', silent=not app.config['debug'])
	where = {
		'alias': user['alias'],
		'devicecode': user['devicecode'],
		'token': user['token'],
		'status': 'active',
	}
	luser = m.read_one(where=where, onerror=None)

	del (m)
	if luser is None:
		return jsonify({"message": "User check failed"}), 400
	return jsonify({'ok': True}), 200

@app.post("/api/is_user")
def is_user():
	# checks if user alias exists
	if not request.is_json:
		return jsonify({"message": "Missing JSON in request"}), 400
	user = normalize_user(request.get_json())
	if user is None:
		return jsonify({"message": "Invalid user data [35]"}), 400

	print('check user', user)
	m = Mongo(collection='users', silent=not app.config['debug'])
	muser = m.read_one(where={'alias': user['alias'], 'status': 'active'}, onerror=None)
	del(m)
	print('muser', muser)
	if muser is None:
		return jsonify({"message": "User check failed"}), 400
	return jsonify({'ok': True}), 200





# ============= Flask 404 request stuff ================
if not app.config['debug']:
	@app.errorhandler(Exception)
	def handle_error(e):
		print(e)
		return render_template(
			'404.html',
			e=str(e),
		)

@app.before_request
def before_request():
	if 'wp-admin' in request.base_url or '.php' in request.base_url:
		return redirect('https://google.com')

@app.after_request
def add_header(res):
	res.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
	res.headers["Pragma"] = "no-cache"
	res.headers["Expires"] = "-1"
	# res.headers['Last-Modified'] = Timetools.datetimenow()

	res.headers['X-Content-Type-Options'] = 'nosnif'
	res.headers[
		'Access-Control-Allow-Origin'] = 'https://deebeebros.com, http://127.0.0.1'
	res.headers['Access-Control-Allow-Methods'] = 'get, post'
	return res

if __name__ == "__main__":
	app.run(debug=False)
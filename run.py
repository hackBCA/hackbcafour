from application import app
from application import CONFIG

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=CONFIG['DEBUG'])
	
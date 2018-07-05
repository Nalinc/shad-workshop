from flask import Flask, request, render_template, make_response, send_from_directory, jsonify
from naoqi import ALProxy

app = Flask(__name__)

@app.route("/")
def index():
	# Render the template index.html from default directory(templates)
    return render_template('index.html')

@app.route('/interact', methods=['POST'])
def interact():
	# Get ip_address from form body
	naoip = request.form['ip_address']
	# this page will be rendered
	resp = make_response(render_template('play.html'))
	# Set a cookie on domain
	resp.set_cookie('ip_address', naoip)
	return resp

@app.route('/say', methods=['GET','POST'])
def say():
	# Parse query string from incoming http request
	msg = request.args.get('msg')
	naoip = request.cookies.get('ip_address')
	try:
		# tts = ALProxy("ALAnimatedSpeech", "192.168.0.106", 9559)
		tts = ALProxy("ALTextToSpeech", str(naoip), 9559)

		# msg = "\\style=joyful\\"+"^mode(contextual)"+ "\RSPD=77\ "+ str(msg).replace("'", "''");
		tts.say(str(msg))
	except Exception,e:
		print "Could not create proxy to ALTextToSpeech"
		print e
		return jsonify({"msg":"please re-connect with correct IP","success":False})

	# Return JSON from FLask
	return jsonify({"msg":msg,"success":True})

@app.route('/js/<path:path>')
def send_js(path):
	# Serve this directory
    return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
	# Serve this directory
    return send_from_directory('static/css', path)

if __name__ == '__main__':
    app.run(debug=True)
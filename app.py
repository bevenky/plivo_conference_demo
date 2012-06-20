import os
import traceback
from flask import Flask, render_template, request, Response
import plivo
app = Flask(__name__)


API_URL = "https://api.plivo.com"

AUTH_ID = ''
AUTH_TOKEN = ''


@app.route("/")
def index():
    return render_template('home.html')


@app.errorhandler(404)
def page_not_found(error):
    """error page"""
    print "%s 404" % str(request.values)
    return 'This URL does not exist', 404


@app.route('/response/conf/music/', methods=['GET', 'POST'])
def conf_music():
    try:
        print "Conf Music %s" % request.values.items()
        r = plivo.Response()
        r.addSpeak("You are currently alone in the conference. Please wait. Thank you.")
        r.addPlay("https://s3.amazonaws.com/plivocloud/music.mp3", loop=1)
        return render_template('response_template.xml', response=r)
    except Exception, e:
        print str(e)
        return "ERROR %s" % str(e)


@app.route('/response/conf/action/', methods=['GET', 'POST'])
def conf_action():
    try:
        print "Conf Action %s" % request.values.items()
        r = plivo.Response()
        r.addSpeak("you are in conference action", loop=1)
        return render_template('response_template.xml', response=r)
    except Exception, e:
        print str(e)
        return "ERROR %s" % str(e)


@app.route('/response/conf/callback/', methods=['GET'])
def conf_callback():
    print "Conf Callback %s" % str(request.args.items())
    action = str(request.args['ConferenceAction'])
    member_id = str(request.args['ConferenceMemberID'])
    print "Conf Action %s" % action
    if action == "enter":
        print "Member ID %s entered into conf" % member_id
    elif action == "exit":
        print "Member ID %s left the conference" % member_id
    elif action == "floor":
        print "Member ID %s is speaking now" % member_id
    else:
        try:
            digits = request.args.get('ConferenceDigitsMatch', None)
            conf_name = request.args.get('ConferenceName', None)
            if digits:
                member = request.args['ConferenceMemberID']
                p = plivo.RestAPI(AUTH_ID, AUTH_TOKEN, url=API_URL)
                params = {'text':'Member %s pressed %s' % (str(member), str(digits)),
                          'voice': 'MAN',
                          'conference_name': conf_name, 'member_id': 'all',
                         }
                r = p.speak_member(params)
                print str("Conf callback speak response: %s" % str(r))
                return "OK"
        except Exception, e:
            print str(e)
            for line in traceback.format_exc().splitlines():
                print str(line)
            return "ERROR %s" % str(e)


@app.route('/response/conf/', methods=['GET', 'POST'])
def conf():
    from_number = str(request.args['From'])
    print "Member with number %s entered into conf" % from_number
    try:
        print "Conf %s" % request.values.items()
        r = plivo.Response()
        r.addSpeak("Hi, welcome to plivo realtime conference demo. You will now be placed into conference.", voice="WOMAN")
        r.addConference("demo",
                enterSound="beep:1",
                waitSound="http://plivoconferencedemo.herokuapp.com/response/conf/music/",
                timeLimit=600000,
                action="http://plivoconferencedemo.herokuapp.com/response/conf/action/",
                digitsMatch="1,2,3,4",
                callbackUrl="http://plivoconferencedemo.herokuapp.com/response/conf/callback/",
                callbackMethod="GET",
                floorEvent="true")
        return render_template('response_template.xml', response=r)
    except Exception, e:
        print str(e)
        return "ERROR %s" % str(e)


if __name__ == '__main__':
    if not os.path.isfile("templates/response_template.xml"):
        print "Error : Can't find the XML template : templates/response_template.xml"
    else:
        port = int(os.environ['PORT'])
        app.run(host='0.0.0.0', port=port)



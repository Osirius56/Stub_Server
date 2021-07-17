import flask
from flask import Flask,Response,send_from_directory,request,Blueprint
from flask.wrappers import Request

events = Blueprint('events', __name__, template_folder='blueprints')
# -- EVENTS
@events.route('/hhh0',methods=["GET"])
def start():
    return Response('Signal: 0%',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhh25',methods=["GET"])
def firstQuartile():
    return Response('Signal: 25%',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhh50',methods=["GET"])
def midpoint():
    return Response('Signal: 50%',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhh75',methods=["GET"])
def thirdQuartile():
    return Response('Signal: 75%',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhh100',methods=["GET"])
def complete():
    return Response('Signal: 100%',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhhsigh=sslpk9gubSo&label=admute&ad_mt=[AD_MT]',methods=["GET"])
def mute():
    return Response('Signal: Mute',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhhsigh=sslpk9gubSo&label=adunmute&ad_mt=[AD_MT]',methods=["GET"])
def unmute():
    return Response('Signal: Unmute',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhhsigh=sslpk9gubSo&label=adrewind&ad_mt=[AD_MT]',methods=["GET"])
def rewind():
    return Response('Signal: rewind',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhhsigh=sslpk9gubSo&label=adpause&ad_mt=[AD_MT]',methods=["GET"])
def pause():
    return Response('Signal: pause',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhhsigh=sslpk9gubSo&label=adresume&ad_mt=[AD_MT]',methods=["GET"])
def resume():
    return Response('Signal: resume',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhhsigh=sslpk9gubSo&label=adfullscreen&ad_mt=[AD_MT]',methods=["GET"])
def fullscreen():
    return Response('Signal: fullscreen',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhhsigh=sslpk9gubSo&label=vast_creativeview&ad_mt=[AD_MT]',methods=["GET"])
def creativeView():
    return Response('Signal: creativeView',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhhsigh=sslpk9gubSo&label=vast_exit_fullscreen&ad_mt=[AD_MT]',methods=["GET"])
def exitFullscreen():
    return Response('Signal: exitFullscreen',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhhsigh=sslpk9gubSo&label=acceptinvitation&ad_mt=[AD_MT]',methods=["GET"])
def acceptInvitationLinear():
    return Response('Signal: acceptInvitationLinear',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhhsigh=sslpk9gubSo&label=adclose&ad_mt=[AD_MT]',methods=["GET"])
def closeLinear():
    return Response('Signal: closeLinear',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhhsigh=sslpk9gubSo&label=videoskipped&ad_mt=[AD_MT]',methods=["GET"])
def skip():
    return Response('Signal: skip',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhhsigh=sslpk9gubSo&label=video_skip_shown&ad_mt=[AD_MT]',methods=["GET"])
def video_skip_shown():
    return Response('Signal: video_skip_shown',status=200,headers={'Access-Control-Allow-Origin': '*'})


@events.route('/hhhsigh=sslpk9gubSo&label=video_engaged_view&ad_mt=[AD_MT]',methods=["GET"])
def video_engaged_view():
    return Response('Signal: video_engaged_view',status=200,headers={'Access-Control-Allow-Origin': '*'})

# @events.route('/event/<event_uri>',methods=["GET"])
# def custom_event(event_uri):
#     if request.args.get("code") == None:
#         status_code = 200
#     else :
#         status_code = request.args.get("code")
    
#     if request.args.get("msg") == None:
#         msg = "%s 200 OK" % event_uri
#     else :
#         msg = request.args.get("msg")

#     return Response(msg,status=status_code,headers={'Access-Control-Allow-Origin': '*'})

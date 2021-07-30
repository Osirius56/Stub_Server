
from methods import *
"""This stub server developed under Flask (Python) allows you to respond to the various events raised by the SmartLib.
It also offers the possibility of providing VAST / VMAP that can be published via API:
 - API '/vast/static/<id>': VAST / VMAP publication in XML format, specific and identified by an ID (can be added, modified, deleted and retrieved)
 - API '/vast/autogen': Automatic generation of a document from JSON data.
"""

# ROUTES
# -- INDEX
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    # return SERVER_INFO
    return update_uri(app.url_map)

# -- VMAP
@app.route("/vmap/")
def doc_vmap():
    with open(os.path.join(os.path.dirname(__file__),"html","vmap_info.html")) as fp:
        html = fp.read()
    html = str(html).format(stub_host=str(request.headers.get("Host")))
    return Response(html)

@app.route("/vmap/static/<id>",methods=["DELETE","PUT","GET"])
def vmap_static(id):
    output = "%s.xml" % id
    msg = deepcopy(MSG_200_OK)
    print("req.data %s " % request.data)
    if request.method == "DELETE":
        if os.path.isfile(os.path.join(VMAP_PATH,output)):
            status = 200
            try:
                os.remove(os.path.join(VMAP_PATH,output))
                msg["message"] = "%s removed sucessfully" % id
            except Exception as error:
                msg["message"] = error
        else:
            msg["message"] = "Resource not found"
            status = 404
        return Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=status)

    if request.method == "POST":
        # response = check_vmap(request.data)
        # print("resp %s" % response)
        # if response != None:
        #     return response
        
        if os.path.isfile(os.path.join(VMAP_PATH,output)):
            msg = deepcopy(MSG_409_CONFLICT)
            return Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=409)
        else:
            # try:
            with open(os.path.join(_check_path(VMAP_PATH),output), "wb") as fp:
                fp.write(request.data)
            if os.path.isfile(os.path.join(VMAP_PATH,output)):
                msg = deepcopy(MSG_201_CREATED)
                return Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=201)
            else :
                msg = deepcopy(MSG_500_INTERNAL_ERROR)
                msg["error"] =  "File %s can't be created without server error."%id
                return Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=500)
            # except Exception as err:
                # return Response(json.dumps(MSG_404_NOT_FOUND) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=500)

    if request.method == "PUT":
        pass
    if request.method == "GET":
        try:
            with open(os.path.join(VMAP_PATH,output)) as fp:
                VAST = fp.read()
            return Response(VAST, mimetype='text/xml',headers=DEFAULT_HEADERS,status=200)
        except Exception as error:
            msg = deepcopy(MSG_404_NOT_FOUND)
            msg["error"] = "VAST Not Found"
            return Response(json.dumps(msg) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=404)

@app.route("/vmap/autogen",methods=["POST","GET"])
def vmap_dynamic():
    if request.method == "PUT":
        # response = check_vmap(vmap_generate(request))
        response = Response(vmap_generate(request), mimetype='text/xml',headers=DEFAULT_HEADERS)
        # msg = MSG_200_OK
        # msg['message'] = vmap_generate(request)
        # response = Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=200)

    else:
        try:
            if request.args['type'] == "text":
                mimetype = 'text/plain'
            else :
                mimetype='text/xml'
        except Exception as err:
            mimetype = 'text/xml'

        with open(os.path.join(VMAP_PATH, VMAP_GENERATED_FILE)) as fp:
            VMAP = fp.read()
            response = Response(VMAP, mimetype=mimetype,headers=DEFAULT_HEADERS)
    return response

# -- VAST
@app.route("/vast/")
def doc_vast():
    with open(os.path.join(os.path.dirname(__file__),"html","vast_info.html")) as fp:
        html = fp.read()
    html = str(html).format(stub_host=str(request.headers.get("Host")))
    return Response(html)

@app.route('/vast/static/<id>',methods=["DELETE","PUT","GET"])
def vast_static(id):
    """ Args : no_check | activate VAST schema validation passthrough (no validation)
    """
    output = "%s.xml" % id
    msg = deepcopy(MSG_200_OK)
    print("req.data %s " % request.data)
    if request.method == "DELETE":
        if os.path.isfile(os.path.join(VAST_PATH,output)):
            status = 200
            try:
                os.remove(os.path.join(VAST_PATH,output))
                msg["message"] = "%s removed sucessfully" % id
            except Exception as error:
                msg["message"] = error
        else:
            msg["message"] = "Resource not found"
            status = 404
        return Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=status)

    if request.method == "PUT":
        try:
            request.args['no_check']
        except:
            print("no_check VAST data")
            response = check_vast(request.data)
            print("resp %s" % response)
            if response != None:
                return response
        
        if os.path.isfile(os.path.join(VAST_PATH,output)):
            msg = deepcopy(MSG_409_CONFLICT)
            return Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=409)
        else:
            # try:
            with open(os.path.join(_check_path(VAST_PATH),output), "wb") as fp:
                fp.write(request.data)
            if os.path.isfile(os.path.join(VAST_PATH,output)):
                msg = deepcopy(MSG_201_CREATED)
                return Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=201)
            else :
                msg = deepcopy(MSG_500_INTERNAL_ERROR)
                msg["error"] =  "File %s can't be created without server error."%id
                return Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=500)
            # except Exception as err:
                # return Response(json.dumps(MSG_404_NOT_FOUND) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=500)

    if request.method == "GET":
        try:
            with open(os.path.join(VAST_PATH,output)) as fp:
                VAST = fp.read()
            return Response(VAST, mimetype='text/xml',headers=DEFAULT_HEADERS,status=200)
        except Exception as error:
            msg = deepcopy(MSG_404_NOT_FOUND)
            msg["error"] = "VAST Not Found"
            return Response(json.dumps(msg) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=404)

@app.route('/vast/autogen',methods=["POST","GET"])
def vast_dynamic():
    if request.method == "POST":
        try:
            vast = vast_generate(request)
            response = check_vast(vast)
            if response == None:
                response = Response(vast, mimetype='text/xml',headers=DEFAULT_HEADERS)
        except Exception as err:
            msg = deepcopy(MSG_500_INTERNAL_ERROR)
            msg['error'] = str(err)
            response = Response(json.dumps(msg) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=500)
    elif request.method == "GET":
        with open(os.path.join(VAST_PATH, VAST_GENERATED_FILE)) as fp:
            VAST = fp.read()
            try:
                if request.args['type'] == "text":
                    mimetype = 'text/plain'
                else :
                    mimetype='text/xml'
            except Exception as err:
                mimetype = 'text/xml'
        response = Response(VAST, mimetype=mimetype,headers=DEFAULT_HEADERS)
    return response

@app.route('/event/<event_uri>',methods=["GET"])
def custom_event(event_uri):
    if request.args.get("code") == None:
        status_code = 200
    else :
        status_code = request.args.get("code")
    
    if request.args.get("msg") == None:
        msg = "%s 200 OK" % event_uri
    else :
        msg = request.args.get("msg")

    return Response(msg,status=status_code,headers=DEFAULT_HEADERS)

@app.route('/custom/',methods=["GET"])
def doc_custom():
    with open(os.path.join(os.path.dirname(__file__),"html","custom_urls_info.html")) as fp:
        html = fp.read()
    example="""{
                "status_code": 200,
                "message" : "You Win",
                "headers":{
                    "content-type": "text",
                    "my-custom-header": "test01"
                }
            }"""
    return Response(head_update(html).format(host=STUB_HOST,port=LISTEN_PORT,example=example,stub_host=str(request.headers.get("Host"))),status=200,headers=DEFAULT_HEADERS)

@app.route('/custom/<custom_uri>',methods=["GET","PUT","DELETE"])
def custom(custom_uri):
    if request.method == "DELETE":
        try:
            RESPONSES.pop(custom_uri)
        except Exception as err:
            print(err)
        return Response("%s correctly deleted" % custom_uri)

    if request.method == "PUT":
        headers = DEFAULT_HEADERS
        if "headers" in str(request.json.keys()).lower():
            headers.update(request.json["headers"])
        RESPONSES[custom_uri] = Response(request.json["message"],status=request.json["status_code"],headers=headers)
        return Response("%s set" % custom_uri,status=200,headers=DEFAULT_HEADERS)
    else :
        try:
            return RESPONSES[custom_uri]
        except:
            return Response("%s not found" % custom_uri,status=404)


if __name__ == "__main__":
    """Main script to run STUB with static confguration of ads in vast. Should include an api to change vast ads data (in version 2.0.0)
    """
    import argparse
    import json
    from collections import namedtuple
 

    parser = argparse.ArgumentParser(prog=os.path.basename(__file__))
    parser.add_argument("-f","--json-file",help="Stub default data to describe static ads to include in vast",default="data/mp4_pod_3ads.json")
    parser.add_argument("-H","--host",help="Define host (IP or DNS) for Stub server",required=False,type=str,default=STUB_HOST)
    parser.add_argument("-p","--port",help="Define port of stub (default = 80)",required=False,type=int,default=LISTEN_PORT)

    args = parser.parse_args()
    
    with open(args.json_file) as fp:
        vast_data = {"json": json.load(fp),"host":"%s:%s" % (args.host,args.port)}
    
    data = namedtuple('Struct', vast_data.keys())(*vast_data.values())
    vast_generate(data)
    app.run(host=str(args.host),port=args.port)



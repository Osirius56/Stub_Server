# import socket
# import uuid,random
# import os,xmlschema,sys,re
# import flask
# from flask import Flask,Response,send_from_directory,request,render_template
# import json
# from copy import deepcopy
# from messages import *

# from flask.wrappers import Request
# from blueprints.events import events
import constantes
from constantes import *

def _check_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)
        assert os.path.isdir(path),"%sCouldn't find or create %s %s" %(bcolors.FAIL,path,bcolors.ENDC)
    return path

# METHODS
def head_update(html):
    return html.replace("__version__",constantes.__version__).replace("__pyver__",sys.version).replace("__flask_version__",flask.__version__)

def get_validation_errors(xml, xsd_uri):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    if os.path.isfile(xml):
        with open(xml,'rb') as fp:
            xml_string = fp.read().decode('utf-8')
    elif isinstance(xml,bytes):
        xml_string = xml.decode('utf_8')
    elif isinstance(xml,str):
        xml_string = xml
    
        
    xsd_path = os.path.join(dir_path, xsd_uri)
    schema = xmlschema.XMLSchema(xsd_path)
    validation_error_iterator = schema.iter_errors(xml_string)
    
    xml_schema_error = []
    for idx, validation_error in enumerate(validation_error_iterator, start=1):
        xml_schema_error.append(f'[{idx}] path: {validation_error.path} | reason: {validation_error.reason}')
    
    return xml_schema_error

def update_uri(data):
    output = []
    docs = []
    output_matrix = []
    rx_rules = re.compile(r"Rule\s*'(?P<uri>.*)'\s*\((?P<methods>.*)\)\s*->\s*(?P<name>.*)>")
    mapping = rx_rules.findall(str(data))
    # print(mapping)
    # mapping = str(data).replace("<", "").replace(">", "").replace("Rule", "").replace("[", "").replace("]", "").replace("Map", " ").replace(")", "").replace("(", "")

    # m = mapping.split(",\n")
    # a = [re.split("(^,\s+|' | - )",z) for z in m]
    for index,data_tuple in enumerate(mapping):
        formated_data = []
        for data in data_tuple:
            data = data.replace("<","&lt;").replace(">","&gt;").replace("'","")
            formated_data.append(data)
            print("data : %s" % data)
        output_matrix.append(formated_data)
        print(output_matrix)
        if formated_data[2] not in ("index","favicon"):
            if not str(formated_data[2]).startswith("doc_") :
                output.append("<li><div>%s</div></li>" % " ".join(["<h4>"+formated_data[2]+"</h4>","<p class='methods'><code>"+formated_data[1]+"</code></p>","<p class='url'>"+formated_data[0]+"</p>"]))
                output.sort()
            else:
                docs.append("<li><div>%s</div></li>" % " ".join(["<h4><a href="+formated_data[0]+">"+formated_data[2].replace("doc_",'')+"</a></h4>","<p class='url'>"+formated_data[0]+"</p>"]))
    m = "\n".join(output)
    doc = "\n".join(docs)

    # m = ["<li>%s" % i for i in m]
    # m = "</li>".join(m)
    return SERVER_INFO.replace("__data__", "<ul>"+m.replace("'","")+"</ul>").replace("__doc__", "<ul>"+doc.replace("'","")+"</ul>")#, output_matrix

def mediafile_cdata_write(cdata):
    return "<![CDATA[%s]]>" % cdata

def mediafile_write(paramDict):
    print(paramDict)
    cdata = paramDict.pop("cdata")
    string = "<MediaFile "
    for param,value in paramDict.items():
        string = "%s %s=\"%s\"" % (string,param,value)
    string = "%s> %s </MediaFile>" % (string,mediafile_cdata_write(cdata))
    return string

def vast_generate(request, output=os.path.join(_check_path(VAST_PATH), VAST_GENERATED_FILE)):
    # add header and footer after treat all ads by for loop
    with open(os.path.join(TEMPLATE_DIR, T_VAST_HEADER)) as fp:
        header = fp.read()
    with open(os.path.join(TEMPLATE_DIR, T_VAST_FOOTER)) as fp:
        footer = fp.read()
    if request.json != None:
        if not isinstance(request.json,list):
            data_list = [request.json]
        else:
            data_list = request.json
    else:
        data_list = [DEFAULT_TEMPLATE_DATA]

    ad_list = [header, footer]

    for ad in data_list:
        assert ad["template_ad_id"]
        assert ad["skipoffset"]
        assert ad["duration"]

        if "ad_sequence" in ad:
            XML_TEMPLATE = T_VAST_POD_AD
        else :
            XML_TEMPLATE = T_VAST_STANDALONE_AD

        # print(XML_TEMPLATE)
        with open(os.path.join(TEMPLATE_DIR, XML_TEMPLATE)) as fp:
            xml = fp.read()

        data = deepcopy(DEFAULT_TEMPLATE_DATA)
        data = dict([[key,value.format(host=request.host)] for key,value in data.items()])
        # print("data:%s" % data)
        ad["mediafile"] = mediafile_write(ad["mediafile"])
        data.update(ad)
        ad_list.insert(-1, xml.format(**data))
    
    xml = "\n".join(ad_list)
    
    with open(output, "w") as fp:
        fp.writelines(ad_list)
    
    return xml

def vmap_generate(request, output=os.path.join(_check_path(VMAP_PATH), VMAP_GENERATED_FILE)):
    # add header and footer after treat all ads by for loop
    ad_break_list = []
    
    with open(os.path.join(TEMPLATE_DIR, T_VMAP)) as fp:
        body = fp.read()

    with open(os.path.join(TEMPLATE_DIR, T_VMAP_ADBREAK_ITEM)) as fp:
        content = fp.read()

    if request.json != None:
        if not isinstance(request.json,list):
            data_list = [request.json]
        else:
            data_list = request.json
    else:
        data_list = [DEFAULT_ADBREAK_VMAP_DATA]
    
    for adbreak in data_list:
        data = deepcopy(DEFAULT_ADBREAK_VMAP_DATA)
        data["timeOffset"] = random.choice(["start","end","00:01:00.000"])
        data["breakId"] = uuid.uuid4()
        data["id"] = uuid.uuid4()
        data = dict([[key,value] for key,value in data.items()])
        print(data)
        print(adbreak)
        data.update(adbreak)
        print(data)
        ad_break_list.append(content.format(**data))
    
    xml = body.format(ad_breaks="\n".join(ad_break_list)).format(host=request.host)
    with open(output, "w") as fp:
        fp.write(xml)
    
    return xml

def check_vast(data,xsd_uri='schema/vast3_draft.xsd'):
    try:
        xml_error = get_validation_errors(data, xsd_uri)
        print("xml_error %s "% xml_error)
        if len(xml_error) > 0:
            msg = deepcopy(MSG_400_BAD_REQUEST)
            msg["error"] = "\n".join(xml_error)
            return Response(json.dumps(msg) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=500)
        # else:
        #     return Response(data, mimetype='text/xml',headers=DEFAULT_HEADERS)
    except Exception as err:
        msg = deepcopy(MSG_500_INTERNAL_ERROR)
        msg['error'] = str(err)
        return Response(json.dumps(msg) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=500)

def check_vmap(data, xsd_uri='schema/vmap_1.0.xsd'):
    try:
        xml_error = get_validation_errors(data, xsd_uri)
        if len(xml_error) > 0:
            msg = deepcopy(MSG_400_BAD_REQUEST)
            msg["error"] = "\n".join(xml_error)
            return Response(json.dumps(msg) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=400)
        # else:
        #     return Response(data, mimetype='text/xml',headers=DEFAULT_HEADERS)
    except Exception as err:
        msg = deepcopy(MSG_500_INTERNAL_ERROR)
        msg['error'] = str(err)
        return Response(json.dumps(msg) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=500)

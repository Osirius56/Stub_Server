from lxml import etree
import xmlschema
import os


def validate(xml_path: str, xsd_path: str) -> bool:

    xmlschema_doc = etree.parse(xsd_path)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    xml_doc = etree.parse(xml_path)
    result = xmlschema.validate(xml_doc)

    return result

def get_validation_errors(xml, xsd_uri='example.xsd'):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    if os.path.isfile(xml):
        with open(xml,'rb') as fp:
            xml_string = fp.read().decode('utf-8')
    elif isinstance(xml,str):
        xml_string = xml
        
    xsd_path = os.path.join(dir_path, xsd_uri)
    schema = xmlschema.XMLSchema(xsd_path)
    validation_error_iterator = schema.iter_errors(xml_string)
    for idx, validation_error in enumerate(validation_error_iterator, start=1):
        print(f'[{idx}] path: {validation_error.path} | reason: {validation_error.reason}')

if __name__ == "__main__":
    xsd = "C:\\Users\\bouhourss\\Documents\\SVN_AUTO_VM\\common_libs\\Python_libs\\VAST_VMAP_STUB\\schema\\vast3.0.xsd"

    # The directory with XML files
    xml = "C:\\Users\\bouhourss\\Documents\\SVN_AUTO_VM\\common_libs\\Python_libs\\VAST_VMAP_STUB\\vast\\001.xml"

    get_validation_errors(xml,xsd_uri=xsd)
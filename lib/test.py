from xml.dom.minidom import parse, parseString
from utils import read_xml, write_xml

myxml_file = "../runtime/5.1.0/conf/bindingservice.beans/META-INF/bindings-jboss-beans.xml"

dom = read_xml(myxml_file)


if __name__ == '__main__':
    print dom
dom_methods = ['ATTRIBUTE_NODE', 'CDATA_SECTION_NODE', 'COMMENT_NODE', 'DOCUMENT_FRAGMENT_NODE',
'DOCUMENT_NODE', 'DOCUMENT_TYPE_NODE', 'ELEMENT_NODE', 'ENTITY_NODE', 'ENTITY_REFERENCE_NODE',
'NOTATION_NODE', 'PROCESSING_INSTRUCTION_NODE', 'TEXT_NODE', '__doc__', '__init__', '__module__', 
'__nonzero__', '_call_user_data_handler', '_child_node_types', '_create_entity', '_create_notation',
'_elem_info', '_get_actualEncoding', '_get_async', '_get_childNodes', '_get_doctype',
'_get_documentElement', '_get_documentURI', '_get_elem_info', '_get_encoding', '_get_errorHandler',
'_get_firstChild', '_get_lastChild', '_get_localName', '_get_standalone', '_get_strictErrorChecking',
'_get_version', '_id_cache', '_id_search_stack', '_magic_id_count', '_set_async', 'abort',
'actualEncoding', 'appendChild', 'async', 'attributes', 'childNodes', 'cloneNode', 'createAttribute',
'createAttributeNS', 'createCDATASection', 'createComment', 'createDocumentFragment', 'createElement',
'createElementNS', 'createProcessingInstruction', 'createTextNode', 'doctype', 'documentElement',
'documentURI', 'encoding', 'errorHandler', 'firstChild', 'getElementById', 'getElementsByTagName',
'getElementsByTagNameNS', 'getInterface', 'getUserData', 'hasChildNodes', 'implementation',
'importNode', 'insertBefore', 'isSameNode', 'isSupported', 'lastChild', 'load', 'loadXML',
'localName', 'namespaceURI', 'nextSibling', 'nodeName', 'nodeType', 'nodeValue', 'normalize',
'ownerDocument', 'parentNode', 'prefix', 'previousSibling', 'removeChild', 'renameNode',
'replaceChild', 'saveXML', 'setUserData', 'standalone', 'strictErrorChecking', 'toprettyxml',
'toxml', 'unlink', 'version', 'writexml']
#    deployment = dom.getElementsByTagName('deployment')[0]

#    deployment.childNodes[15].nodeName
#    u'bean'

#    deployment.childNodes[15].getAttribute('name')
#    u'StandardBindings'

#    deployment.childNodes[15].getAttribute('class')
#    u'java.util.HashSet'

#    deployment.childNodes[15].childNodes[1].childNodes[1].getAttribute('class')
#    u'java.util.Collection'

#    deployment.childNodes[15].childNodes[1].childNodes[1].childNodes[1].getAttribute('elementClass')
#    >>>u'org.jboss.services.binding.ServiceBindingMetadata'

#    deployment.childNodes[15].childNodes[1].childNodes[1].childNodes[1].childNodes   # StandardBindings
    
#    deployment.childNodes[15].childNodes[1].childNodes[1].childNodes[1].childNodes[5].getAttribute('class')
#    >>>u'org.jboss.services.binding.ServiceBindingMetadata    
#    deployment.childNodes[15].childNodes[1].childNodes[1].childNodes[1].childNodes[5].childNodes[1].getAttribute('name')
#    >>>u'serviceName
#    deployment.childNodes[15].childNodes[1].childNodes[1].childNodes[1].childNodes[5].childNodes[3].getAttribute('name')
#    >>>u'bindingName'
#    deployment.childNodes[15].childNodes[1].childNodes[1].childNodes[1].childNodes[5].childNodes[5].getAttribute('name')
#    >>>u'port'
#    deployment.childNodes[15].childNodes[1].childNodes[1].childNodes[1].childNodes[5].childNodes[7].getAttribute('name')
#    >>>u'description'


    path = [["deployment",{"xmlns":"urn:jboss:bean-deployer:2.0"}],
        ["bean",{"name":"StandardBindings", "class":"java.util.HashSet"}, 15],
        "constructor",
        ["parameter", {"class":"java.util.Collection"}],
        ["bean", {"class":"org.jboss.services.binding.ServiceBindingMetadata"}],
        ["property", {"name":"serviceName"}]]

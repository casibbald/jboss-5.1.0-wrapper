from xml.dom.minidom import parse, parseString
from utils import read_xml, write_xml

myxml_file = "../runtime/5.1.0/conf/bindingservice.beans/META-INF/bindings-jboss-beans.xml"

dom = read_xml(myxml_file)


if __name__ == '__main__':
    
    deployment = dom.getElementsByTagName('deployment')[0]

    deployment.childNodes[15].nodeName
    u'bean'

    deployment.childNodes[15].getAttribute('name')
    u'StandardBindings'

    deployment.childNodes[15].getAttribute('class')
    u'java.util.HashSet'

    deployment.childNodes[15].childNodes[1].childNodes[1].getAttribute('class')
    u'java.util.Collection'

    deployment.childNodes[15].childNodes[1].childNodes[1].childNodes[1].getAttribute('elementClass')
    >>>u'org.jboss.services.binding.ServiceBindingMetadata'

    deployment.childNodes[15].childNodes[1].childNodes[1].childNodes[1].childNodes   # StandardBindings
    
    deployment.childNodes[15].childNodes[1].childNodes[1].childNodes[1].childNodes[5].getAttribute('class')
    >>>u'org.jboss.services.binding.ServiceBindingMetadata    
    deployment.childNodes[15].childNodes[1].childNodes[1].childNodes[1].childNodes[5].childNodes[1].getAttribute('name')
    >>>u'serviceName
    deployment.childNodes[15].childNodes[1].childNodes[1].childNodes[1].childNodes[5].childNodes[3].getAttribute('name')
    >>>u'bindingName'
    deployment.childNodes[15].childNodes[1].childNodes[1].childNodes[1].childNodes[5].childNodes[5].getAttribute('name')
    >>>u'port'
    deployment.childNodes[15].childNodes[1].childNodes[1].childNodes[1].childNodes[5].childNodes[7].getAttribute('name')
    >>>u'description'


path = [["deployment",{"xmlns":"urn:jboss:bean-deployer:2.0"}],
    ["bean",{"name":"StandardBindings" "class":"java.util.HashSet"}, 15],
    "constructor",
    ["parameter", {"class":"java.util.Collection"}],
    ["bean", {"class":"org.jboss.services.binding.ServiceBindingMetadata"}],
    ["property", {"name":"serviceName"}]]

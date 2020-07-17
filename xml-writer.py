#! /user/bin/python3

# writes a simple xml file 

from xml.etree.ElementTree import ElementTree, Element, SubElement, dump, tostring

root = Element("gexf")
root.set('xmlns', 'http://www.gexf.net/1.3')
root.set('version', '1.3')
root.set('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
root.set('xsi:schemaLocation','http://www.gexf.net/1.3 http://www.gexf.net/1.3/gexf.xsd')

graph = SubElement(root, "graph", type = "static")

'''
<attributes class="node" type="static">
    <attribute id="label" title="label" type="string"/>
</attributes>
'''
attr = SubElement(graph, "attributes")
attr.attrib["class"] = "node"
attr.attrib["type"] = "static"
attrib = SubElement(attr, "attribute", id="label", title="label", type="string")



nodes = SubElement(graph, "nodes")
aNode = SubElement(nodes, "node", id="1234", label="abcd")

edges = SubElement(graph, "edges")
anEdge = SubElement(edges, "edge", id="1234", source="1234", target="5678")


print(tostring(root))
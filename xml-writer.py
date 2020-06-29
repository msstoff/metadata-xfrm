#! /user/bin/python3

# writes a simple xml file 

from xml.etree.ElementTree import Element, SubElement, dump

root = Element("{http://www.gephi.org/gexf}gexf")
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

dump(root)

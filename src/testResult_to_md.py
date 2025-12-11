"""
Docstring for src.nunit3_to_md
"""

# Python 3 Standard Library Imports
from datetime import datetime
import re
import xml.etree.ElementTree as ET

def convert_nunit3_to_md(node: ET.Element, heading_level: int = 1) -> str:
    """
    Converts an NUnit3 XML report from the Pester Framework to Markdown.
    
    Each section of the hierarchical XML will have its own Markdown section. This section will be rendered with the appropriate heading.

    Args:
        node (xml.etree.ElementTree.Element):
            The node in the XML tree to gather information from on the front side of the recursion stack.
    Returns:
        str:
            A Markdown string that can be captured at the original call point and written to disk.
            This string returns on the back side of the recursion stack.
    """
    md = "" # starting with an empty md string each time, which returns back to the call point
    match node.tag:
        case 'test-run':
            md += f"""{"#" * heading_level} Test Results for {node.attrib['name']}

 > Overall Results: {node.attrib['result']} in {node.attrib['duration']}s

**Start Time:** {datetime.strptime(node.attrib['start-time'].split(".")[0], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")}
**End Time:** {datetime.strptime(node.attrib['end-time'].split(".")[0], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")}

| Total Tests | Total Passed | Total Failed | Total Inconclusive | Total Skipped | Total Warnings |
| :---------- | :----------- | :----------- | :----------------- | :------------ | :------------- |
| {node.attrib['total']} | {node.attrib['passed']} | {node.attrib['failed']} | {node.attrib['inconclusive']} | {node.attrib['skipped']} | {node.attrib['warnings']} |

_(Random Seed Value: {node.attrib['random-seed']})_
"""
        case 'filter':
            md += f"""{"#" * heading_level} Test Run Filters Applied

_(Not yet able to parse filters...)_
"""
            # process additional filter components here later

        case 'test-suite':
            # if it has properties under it, grab those values for use
            # targeting name="_TYPE" property by itself for now
            props = node.find('properties')  # the first returned node will be the one immediately underneath

            if props is not None:
                test_suite_type = [prop.attrib['value'] for prop in props if prop.attrib['name'] == "_TYPE"][0]
            else:
                # fallback just in case
                test_suite_type = node.attrib['type']
            
            # determine if test-suite has test-cases directly underneath it
            if 'test-case' in [child.tag for child in node]:
                test_case_header = f"""**Test Cases**

| ID | Result (Runstate) | Duration | Assert Statements | Description |
| :- | :---------------- | :------- | :---------------- | :---------- |
"""
            else:
                test_case_header = ""

            if test_suite_type == "ParameterizedMethod":
                test_suite_type = "Data-Driven Test"

            # determine what type of Test-Suite this is
            md += f"""
{(("#" * heading_level) + " ") if heading_level <= 4 else "**"}{test_suite_type}: {node.attrib['name']} (ID: {node.attrib['id']}, Run State: {node.attrib['runstate']}){"" if heading_level <= 4 else "**"} 

 > {test_suite_type} Results: {node.attrib['result']} in {node.attrib['duration']}s

| {test_suite_type} Tests | {test_suite_type} Passed | {test_suite_type} Failed | {test_suite_type} Inconclusive | {test_suite_type} Skipped | {test_suite_type} Warnings |
| :---------- | :----------- | :----------- | :----------------- | :------------ | :------------- |
| {node.attrib['total']} | {node.attrib['passed']} | {node.attrib['failed']} | {node.attrib['inconclusive']} | {node.attrib['skipped']} | {node.attrib['warnings']} |

{test_case_header.rstrip()}
"""
            md.rstrip()
            
        case 'environment':
            md += f"""{"#" * heading_level} Test Suite Environment

| Platform | OS Version | OS Architecture | CLR Version | Pester Framework Version |
| :------- | :--------- | :-------------- | :---------- | :----------------------- |
| {node.attrib['platform'].split('|')[0]} | {node.attrib['os-version']} | {node.attrib['os-architecture']} | {node.attrib['clr-version']} | {node.attrib['framework-version']} |
"""
        case 'test-case':
            # locate properties if exists
            props = node.find('properties')  # the first returned node will be the one immediately underneath

            if props is not None:
                # insert values from properties in the methodname where <> are found
                method_name_new = node.attrib['methodname']
                # searching for insertion places from properties
                token_pattern = re.compile(r'\<\w*\>')
                
                for token in re.findall(token_pattern, node.attrib['methodname']):
                    token_clean = token.strip('<>')
                    # search properties where the name=token_clean and capture value
                    token_value = [prop.attrib['value'] for prop in props if prop.attrib['name'].lower() == token_clean][0]
                    # insert value into method_name_new where token is currently
                    # continual split and sew back together, probably not the most efficient method
                    method_name_new = f"{token_value}".join(re.split(token, method_name_new))
            else:
                # fallback just in case
                method_name_new = node.attrib['methodname']
                        

            # render as a table row
            md += f"""| {node.attrib['id']} | {node.attrib['result']} ({node.attrib['runstate']}) | {node.attrib['duration']}s | {node.attrib['asserts']} | {method_name_new} |
"""
            md.lstrip()

    # locating children
    if len(node) > 0:
        for child in node:
            # traverse the node, convert to markdown, append to existing markdown string
            md += convert_nunit3_to_md(child, heading_level + 1)
    # base case, leaf node
    return md
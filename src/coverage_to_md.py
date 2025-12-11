# Python 3 Standard Library Imports
import sys
import xml.etree.ElementTree as ET

# utility functions
def get_counter_object(node: ET.Element) -> dict[str,dict[str,int]]:
    result = {}

    for ctr in node.findall('counter'):
        missed = int(ctr.attrib['missed'])
        covered = int(ctr.attrib['covered'])
        total = missed + covered
        percent = round(100 * (covered / total), 1) if total > 0 else 0

        result[ctr.attrib['type']] = {
            "missed": missed,
            "covered": covered,
            "total": total,
            "percent": percent
        }
    
    return result

def format_counter_row(counter_result: dict[str, dict[str,int]], label: str) -> str:
    instruction = counter_result['INSTRUCTION']
    line = counter_result['LINE']
    method = counter_result['METHOD']
    cls = counter_result['CLASS']

    return f"""| {label} | {line['covered']}/{line['total']} ({line['percent']}%) | {instruction['covered']}/{instruction['total']} ({instruction['percent']}%) | {method['covered']}/{method['total']} ({method['percent']}%) | {cls['covered']}/{cls['total']} ({cls['percent']}%) |
"""

def format_method_counter_row(counter_result: dict[str, dict[str, int]], className: str, methodName: str, lineNum: int) -> str:
    instruction = counter_result['INSTRUCTION']
    line = counter_result['LINE']
    method = counter_result['METHOD']

    return f"""| {className} | {methodName} | {lineNum} | {line['covered']}/{line['total']} ({line['percent']}%) | {instruction['covered']}/{instruction['total']} ({instruction['percent']}%) | {method['covered']}/{method['total']} ({method['percent']}%) |
"""

# core function
def convert_jacoco_to_md(root: ET.Element, coverage_thresholds: dict[str, int], heading_level: int = 3) -> str:
    
    # get tree root and basic report name
    reportName = root.attrib['name']

    # parse overall counters from code coverage
    overall_counters = get_counter_object(root)

    # parse class and method counters
    rowsByClass = []
    methodRows = []

    for pkg in root.findall('package'): # these are test suites
        for cls in pkg.findall('class'): # these are files
            className = cls.attrib['name'].replace("<", "&lt;").replace(">", "&gt;")
            rowsByClass.append(format_counter_row(
                get_counter_object(cls),
                className
            ))
            for mthd in cls.findall('method'): # these are functions in files
                methodName = mthd.attrib['name'].replace("<", "&lt;").replace(">", "&gt;")
                methodRows.append(format_method_counter_row(
                    get_counter_object(mthd),
                    className,
                    methodName,
                    int(mthd.attrib['line'])
                ))

    # start building markdown
    md = f"""{"#" * heading_level} Code Coverage Report (JaCoCo)

**Report:** {reportName}

{"#" * (heading_level + 1)} Summary

| Scope | Lines | Instructions | Methods | Classes |
| :---- | :---- | :----------- | :------ | :------ |
{format_counter_row(overall_counters, "Total")}

{"#" * (heading_level + 1)} Coverage By Class

| Class | Lines | Instructions | Methods | Classes |
| :---- | :---- | :----------- | :------ | :------ |
"""
    
    for row in rowsByClass:
        md += row
    
    md += f"""
    
{"#" * (heading_level + 1)} Coverage By Method

| Class | Method | Line | Lines | Instructions | Methods |
| :---- | :----- | :--- | :---- | :----------- | :------ |
"""
    for row in methodRows:
        md += row

    # Evaluate Threshold Failures
    linePct = overall_counters['LINE']['percent']
    instrPct = overall_counters['INSTRUCTION']['percent']
    methodPct = overall_counters['METHOD']['percent']
    classPct = overall_counters['CLASS']['percent']

    thresholdFailures = []

    if coverage_thresholds['line'] > 0 and linePct < coverage_thresholds['line']: # type: ignore
        thresholdFailures.append(f"Line coverage {linePct}% < min {coverage_thresholds['line']}") # type: ignore
    if coverage_thresholds['instr'] > 0 and instrPct < coverage_thresholds['instr']: # type: ignore
        thresholdFailures.append(f"Instruction coverage {instrPct}% < min {coverage_thresholds['instr']}") # type: ignore
    if coverage_thresholds['method'] > 0 and methodPct < coverage_thresholds['method']: # type: ignore
        thresholdFailures.append(f"Method coverage {methodPct}% < min {coverage_thresholds['method']}") # type: ignore
    if coverage_thresholds['class'] > 0 and classPct < coverage_thresholds['class']: # type: ignore
        thresholdFailures.append(f"Class coverage {classPct}% < min {coverage_thresholds['class']}") # type: ignore
    
    if len(thresholdFailures) > 0:
        md += f"""

{"#" * (heading_level + 1)} Coverage Thresholds Failed

> Build failed due to coverage thresholds.

"""
        
        for msg in thresholdFailures:
            md += f" - {msg}\n"
        
        print(f"Coverage threshold not met: {";".join(thresholdFailures)}")
    else:
        md += f"""

{"#" * (heading_level + 1)} Coverage Thresholds Passed!

> Build is passing, all coverage thresholds were met!
"""
        print("Build is passing, all coverage thresholds were met!")

    return md
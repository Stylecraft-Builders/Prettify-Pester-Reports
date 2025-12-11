# Python 3 Standard Library
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

# Custom Module Imports
from src.testResult_to_md import convert_nunit3_to_md   
from src.coverage_to_md import convert_jacoco_to_md

def restricted_float(value: float | str) -> float:
    try:
        fvalue = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Cannot convert {value} to floating point value.")
    if fvalue < 0 or fvalue > 100:
        raise argparse.ArgumentTypeError(f"{value} is out of range (0.0-100.0)")
    return fvalue

def parse_args(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='PrettifyPester',
        description='Prettify Pester Reports: Turn XML reports into Markdown for use on static sites and Github.'
    )

    parser.add_argument(
        "--xml_path",
        "-p",
        type=str,
        help="The Path object that points to the XML file you want to parse. Must be parseable by Path().",
        required=True
    )

    parser.add_argument(
        "--output_path",
        "-o",
        type=str,
        help="The Path object that points to the location where you want the Markdown file to be written. Must be parseable by Path().",
        required=True
    )

    parser.add_argument(
        "--report_type",
        "-r",
        type=str,
        help="The type of report that this script is parsing. Each type has restricted schema options.",
        default='testResult',
        choices=['testResult', 'coverage']
    )

    parser.add_argument(
        "--report_schema",
        "-s",
        type=str,
        help="The specific XML schema that will be used to parse this XML report. Each report type has restricted schema options.",
        default='nunit3',
        choices=['nunit3', 'jacoco']
    )

    parser.add_argument(
        "--heading_level",
        "-l",
        type=int,
        choices=[1,2,3],
        default=3, # for GitHub insertion
        help="The number of the top-level heading in the produced Markdown document. Set this to be appropriate for the document this report will be embedded in. If 1 is chosen, this is assumed to be a standalone report."
    )

    parser.add_argument(
        "--min_line_cov",
        type=restricted_float, # type: ignore
        help="The minimum coverage threshold for line coverage, between 0.0 and 100.0",
        default=75.0,
        required=False
    )

    parser.add_argument(
        "--min_instr_cov",
        type=restricted_float, # type: ignore
        help="The minimum coverage threshold for instruction coverage, between 0.0 and 100.0",
        default=75.0,
        required=False
    )

    parser.add_argument(
        "--min_method_cov",
        type=restricted_float, # type: ignore
        help="The minimum coverage threshold for method coverage, between 0.0 and 100.0",
        default=75.0,
        required=False
    )

    parser.add_argument(
        "--min_class_cov",
        type=restricted_float, # type: ignore
        help="The minimum coverage threshold for class coverage, between 0.0 and 100.0",
        default=100.0,
        required=False
    )

    return parser.parse_args(args)

def validate_args(args: argparse.Namespace) -> tuple[bool, list[str]]:
    """validate_args Determines whether a set of arguments is valid given specific parsing restrictions.

    Args:
        args (argparse.Namespace): The args produces by `argparse.ArgumentParser.parse_args()`. Specific to this script.

    Returns:
        tuple[bool, list[str]]: Returns a flag with the validity of the arguments and a list of errors. This list of errors may be empty if no errors were found.
    """
    # validate that the report type and schema will work together
    is_valid = True
    errors = []
    match args.report_type:
        # due to the argument parser, it will always be one of these two results
        case 'testResult':
            if args.report_schema not in ['nunit3']:
                is_valid = False
                errors.append(f"'{args.report_schema}' can't be used with {args.report_type}. Please see the function docstring for more information.")
        case 'coverage':
            if args.report_schema not in ['jacoco']:
                is_valid = False
                errors.append(f"'{args.report_schema}' can't be used with {args.report_type}. Please see the function docstring for more information.")
            
    # Now that those options are validated and we're not going to create a bad pairing, continue on.
    # Make sure that the input XML is valid
    xml_path = Path(args.xml_path).resolve()
    if not xml_path.exists():
        is_valid = False
        errors.append(f"Can't open '{xml_path}', please make sure it exists before trying again.")
    
    return is_valid, errors

def create_md_file(xml_tree: ET.ElementTree, output_path: Path, report_type: str, report_schema: str, coverage_thresholds: dict[str,int] | None = None, heading_level: int = 3) -> None:
    """create_md_file uses the input type and format of incoming XML to generate a Markdown report for display anywhere Markdown formatting is allowed.

    This function is designed to accept a limited set of `report_type` and `report_schema` pairs. Each `report_type` is some output of Pester, either a testResult or a coverage file. Each `report_type` has a set of `report_schema` values that it can accept. Because XML is an extensible file format, this function must know the schema in order to efficiently parse into Markdown in a way that makes sense semantically.

    Each `report_type` and `report_schema` combination is tied to a file in the src module, such as src.testResult_to_md. This is to make troubleshooting easier and should not have an impact on performance as these specific functions are imported on every run. This function does assume that the `report_type` and `report_schema` combination has been validated before being passed as parameters, to ensure reliability.

    Args:
        xml_tree (ET.ElementTree): The XML tree structure to perform parsing on.
        output_path (Path): The location and name of the newly generated Markdown file.
        report_type (str): The type of Pester report to process. Must be one of 'testResult' or 'coverage'.
        report_schema (str): The schema of the Pester report. Must be one of 'NUnit3' and 'JaCoCo' and be an acceptable pairing to the `report_type`.

    Raises:
        UserWarning: This warning is raised if the Markdown string is empty. This usually indicates an error with one of the conversion functions, and other errors should be thrown in this case from the failed function.
    """
    root = xml_tree.getroot()

    md = "" # ensure variable is bound

    match report_type:
        # only ever two report types found here
        case 'testResult':
            match report_schema:
                case 'nunit3':
                    md = convert_nunit3_to_md(
                        root,  # type: ignore
                        heading_level=heading_level
                    )
        case 'coverage':
            match report_schema:
                case 'jacoco':
                    if coverage_thresholds is not None:
                        md = convert_jacoco_to_md(
                            root, # type: ignore
                            heading_level=heading_level,
                            coverage_thresholds=coverage_thresholds
                        )
                    else:
                        raise ValueError("No Markdown was generated. Can't process Code Coverage without the coverage_thresholds dictionary.")

    # don't write any content to disk if there is no content
    if md != "":
        with open(output_path, 'w') as md_file:
            md_file.write(md)
    else:
        raise ValueError("No Markdown was generated, double check that the report type and schema you chose is supported.")
""" _summary_

Returns:
      _type_: _description_
"""

# Python 3 Standard Library Imports
import argparse
import os
from pathlib import Path
from pathlib._local import WindowsPath
import re
import xml.etree.ElementTree as ET

# Pip Package Imports
import pytest

# Custom imports for testing
from src.utilities import parse_args, validate_args, create_md_file, restricted_float

@pytest.fixture(scope="session")
def cwd() -> str:
   return os.getcwd()

@pytest.fixture(scope="session")
def xml_tree_tr_1(cwd) -> ET.Element:
   # pull in a test results file
   test_xml_path = Path(os.path.join(f"{cwd}\\tests\\_data\\", "test_results_test1.xml")).resolve()
   return ET.parse(test_xml_path) # type: ignore

@pytest.fixture(scope="session")
def xml_tree_cov_1(cwd) -> ET.Element:
   # pull in a coverage file
   test_xml_path = Path(os.path.join(f"{cwd}\\tests\\_data\\", "coverage_test1.xml")).resolve()
   return ET.parse(test_xml_path) # type: ignore

@pytest.fixture(scope="session")
def xml_tree_cov_2(cwd) -> ET.Element:
   # pull in a coverage file
   test_xml_path = Path(os.path.join(f"{cwd}\\tests\\_data\\", "coverage_test2.xml")).resolve()
   return ET.parse(test_xml_path) # type: ignore

@pytest.fixture(scope="session")
def bad_args_bad_file() -> list[str]:
   return [
      "--xml_path",
      str(Path("tests/_data/does_not_exist.xml").resolve()),
      "--output_path",
      str(Path("_reports/pytest_output.md")),
      "--report_type",
      "testResult",
      "--report_schema",
      "nunit3"
   ]

@pytest.fixture(scope="session")
def bad_args_bad_report() -> list[str]:
   return [
      "--xml_path",
      str(Path("tests/_data/test_results_test1.xml").resolve()),
      "--output_path",
      str(Path("_reports/pytest_output.md")),
      "--report_type",
      "pesterResultType",
      "--report_schema",
      "nunit3"
   ]

@pytest.fixture(scope="session")
def bad_args_bad_schema() -> list[str]:
   return [
      "--xml_path",
      str(Path("tests/_data/test_results_test1.xml").resolve()),
      "--output_path",
      str(Path("_reports/pytest_output.md")),
      "--report_type",
      "testResult",
      "--report_schema",
      "junit"
   ]

@pytest.fixture(scope="session")
def bad_args_bad_match1() -> list[str]:
   return [
      "--xml_path",
      str(Path("tests/_data/test_results_test1.xml").resolve()),
      "--output_path",
      str(Path("_reports/pytest_output.md")),
      "--report_type",
      "testResult",
      "--report_schema",
      "jacoco"
   ]

@pytest.fixture(scope="session")
def bad_args_bad_match2() -> list[str]:
   return [
      "--xml_path",
      str(Path("tests/_data/test_results_test1.xml").resolve()),
      "--output_path",
      str(Path("_reports/pytest_output.md")),
      "--report_type",
      "coverage",
      "--report_schema",
      "nunit3"
   ]

@pytest.fixture(scope="session")
def good_args_tr() -> list[str]:
   return [
      "--xml_path",
      str(Path("tests/_data/test_results_test1.xml").resolve()),
      "--output_path",
      str(Path("_reports/pytest_tr_test1.md")),
      "--report_type",
      "testResult",
      "--report_schema",
      "nunit3"
   ]

@pytest.fixture(scope="session")
def good_args_cov_fail() -> list[str]:
   cov_thresholds = {
      "line": "80",
      "instr": "70",
      "method": "70",
      "class": "100"
   }

   return [
      "--xml_path",
      str(Path("tests/_data/coverage_test1.xml").resolve()),
      "--output_path",
      str(Path("_reports/pytest_cov_test1.md")),
      "--report_type",
      "coverage",
      "--report_schema",
      "jacoco",
      "--min_line_cov",
      cov_thresholds["line"],
      "--min_instr_cov",
      cov_thresholds["instr"],
      "--min_method_cov",
      cov_thresholds["method"],
      "--min_class_cov",
      cov_thresholds["class"],
   ]

@pytest.fixture(scope="session")
def good_args_cov_pass() -> list[str]:
   cov_thresholds = {
      "line": "80",
      "instr": "70",
      "method": "70",
      "class": "100"
   }

   return [
      "--xml_path",
      str(Path("tests/_data/coverage_test2.xml").resolve()),
      "--output_path",
      str(Path("_reports/pytest_cov_test2.md")),
      "--report_type",
      "coverage",
      "--report_schema",
      "jacoco",
      "--min_line_cov",
      cov_thresholds["line"],
      "--min_instr_cov",
      cov_thresholds["instr"],
      "--min_method_cov",
      cov_thresholds["method"],
      "--min_class_cov",
      cov_thresholds["class"],
   ]

def test_restricted_float_good_value():
   fvalue_float = restricted_float(17.0)
   fvalue_string = restricted_float("28.2")

   assert isinstance(fvalue_float, float) == True
   assert isinstance(fvalue_string, float) == True

def test_restricted_float_bad_value():
   bad_value1 = 100.00281
   bad_value2 = -0.00281

   # too high
   with pytest.raises(argparse.ArgumentTypeError, match=re.escape(f"{bad_value1} is out of range (0.0-100.0)")):
      _ = restricted_float(bad_value1)   

   # too low
   with pytest.raises(argparse.ArgumentTypeError, match=re.escape(f"{bad_value2} is out of range (0.0-100.0)")):
      _ = restricted_float(bad_value2)

def test_restricted_float_non_float():
   bad_value = "hellothere"
   with pytest.raises(argparse.ArgumentTypeError, match=re.escape(f"Cannot convert {bad_value} to floating point value.")):
      _ = restricted_float(bad_value)

def test_parse_args_good(good_args_tr):
   args = parse_args(good_args_tr)

   # look at the args instance itself
   assert isinstance(args, argparse.Namespace)

   # evaluate type and value of each argument
   assert isinstance(args.xml_path, str) == True
   assert Path(args.xml_path).exists() == True
   assert isinstance(Path(args.xml_path).resolve(),WindowsPath) == True
   xml_pat = r'.*\\tests\\_data\\test_results_test1\.xml'
   assert re.match(xml_pat, str(Path(args.xml_path).resolve()))

   assert isinstance(args.output_path, str) == True
   assert isinstance(Path(args.output_path).resolve(),WindowsPath) == True
   output_pat = r'.*\\_reports\\pytest_tr_test1.md'
   assert re.match(output_pat, str(Path(args.output_path).resolve()))

   assert isinstance(args.report_type, str) == True
   assert args.report_type == 'testResult'

   assert isinstance(args.report_schema, str) == True
   assert args.report_schema == 'nunit3'

def test_parse_args_bad(bad_args_bad_schema):
   with pytest.raises(SystemExit) as pytest_err:
      args = parse_args(bad_args_bad_schema)

   assert pytest_err.type == SystemExit
   assert pytest_err.value.code != 0

def test_validate_args_valid(good_args_tr):
   args = parse_args(good_args_tr)
   result, errors = validate_args(args)

   # basics
   assert result == True
   assert len(errors) == 0

def test_validate_args_invalid_file(bad_args_bad_file):
   args = parse_args(bad_args_bad_file)
   result, errors = validate_args(args)

   # basics
   assert result == False
   assert len(errors) > 0

   # content of errors
   assert f"Can't open '{args.xml_path}', please make sure it exists before trying again." in errors

def test_parse_args_invalid_report(bad_args_bad_report):
   with pytest.raises(SystemExit) as pytest_err:
      args = parse_args(bad_args_bad_report)
   
   assert pytest_err.type == SystemExit
   assert pytest_err.value.code != 0

def test_parse_args_invalid_schema(bad_args_bad_schema):
   with pytest.raises(SystemExit) as pytest_err:
      args = parse_args(bad_args_bad_schema)
   
   assert pytest_err.type == SystemExit
   assert pytest_err.value.code != 0

def test_validate_args_invalid_match_tr(bad_args_bad_match1):
   args = parse_args(bad_args_bad_match1)
   result, errors = validate_args(args)

   # basics
   assert result == False
   assert len(errors) > 0

   # content of errors
   assert f"'{args.report_schema}' can't be used with {args.report_type}. Please see the function docstring for more information." in errors

def test_validate_args_invalid_match_cov(bad_args_bad_match2):
   args = parse_args(bad_args_bad_match2)
   result, errors = validate_args(args)

   # basics
   assert result == False
   assert len(errors) > 0

   # content of errors
   assert f"'{args.report_schema}' can't be used with {args.report_type}. Please see the function docstring for more information." in errors

def test_create_md_file_tr_nunit3(xml_tree_tr_1, good_args_tr, cwd):
   # pull for testing
   args = parse_args(good_args_tr)

   create_md_file(
      xml_tree=xml_tree_tr_1,
      output_path=args.output_path,
      report_type=args.report_type,
      report_schema=args.report_schema,
      heading_level=1
   )

   # verify file was created
   assert Path(args.output_path).exists() == True

   # verify file has contents
   with open(Path(os.path.join(cwd, args.output_path)).resolve(), 'r') as test_file:
      contents = test_file.read()

      assert contents
      assert len(contents) > 0 
      assert "# Test Results for " in contents

def test_create_md_file_cov_jacoco_fail(xml_tree_cov_1, good_args_cov_fail, cwd):
   args = parse_args(good_args_cov_fail)

   cov_thresholds = {
      "line": args.min_line_cov,
      "instr": args.min_instr_cov,
      "method": args.min_method_cov,
      "class": args.min_class_cov
   }

   create_md_file(
      xml_tree=xml_tree_cov_1,
      output_path=args.output_path,
      report_type=args.report_type,
      report_schema=args.report_schema,
      coverage_thresholds=cov_thresholds,
      heading_level=2
   )

   # verify file was created
   assert Path(args.output_path).exists() == True

   # verify file has contents
   with open(Path(os.path.join(cwd, args.output_path)).resolve(), 'r') as test_file:
      contents = test_file.read()

      assert contents
      assert len(contents) > 0 
      assert "# Code Coverage Report (JaCoCo)" in contents

def test_create_md_file_cov_jacoco_pass(xml_tree_cov_2, good_args_cov_pass, cwd):
   args = parse_args(good_args_cov_pass)

   cov_thresholds = {
      "line": args.min_line_cov,
      "instr": args.min_instr_cov,
      "method": args.min_method_cov,
      "class": args.min_class_cov
   }

   create_md_file(
      xml_tree=xml_tree_cov_2,
      output_path=args.output_path,
      report_type=args.report_type,
      report_schema=args.report_schema,
      coverage_thresholds=cov_thresholds,
      heading_level=2
   )

   # verify file was created
   assert Path(args.output_path).exists() == True

   # verify file has contents
   with open(Path(os.path.join(cwd, args.output_path)).resolve(), 'r') as test_file:
      contents = test_file.read()

      assert contents
      assert len(contents) > 0 
      assert "# Code Coverage Report (JaCoCo)" in contents

def test_create_md_file_cov_jacoco_no_covthres(xml_tree_cov_1, good_args_cov_fail, cwd):
   args = parse_args(good_args_cov_fail)
   with pytest.raises(ValueError, match="No Markdown was generated. Can't process Code Coverage without the coverage_thresholds dictionary."):
      create_md_file(
         xml_tree=xml_tree_cov_1,
         output_path=Path(os.path.join(cwd, args.output_path)).resolve(),
         report_type=args.report_type,
         report_schema=args.report_schema,
         heading_level=1,
         coverage_thresholds=None # explicitly None to force an error
      )

def test_create_md_file_no_contents(xml_tree_tr_1, cwd):
   output_path = Path(os.path.join(cwd, "_reports/bad_test_output.md")).resolve()
   # force a no content MD file and see what happens
   with pytest.raises(ValueError, match="No Markdown was generated, double check that the report type and schema you chose is supported"):
      create_md_file(
         xml_tree=xml_tree_tr_1,
         output_path=output_path,
         report_type='fake_report',
         report_schema='fake_schema'
      )

   # should not exist
   assert Path(output_path).exists() == False
# Prettify Pester Reports

![Python Validation](https://github.com/Stylecraft-Builders/Prettify-Pester-Reports/actions/workflows/python_validation.yml/badge.svg)

## Copyright
This package was created by Dallas Taylor at Stylecraft Builders, and released publicly under a GPLv3 License. This package contains no code or information proprietary to Stylecraft Builders, and has no implied warranty.

## Summary
Prettify Pester Reports is a GitHub Action designed to convert the XML outputs from the Pester Unit Testing framework into Markdown for easy display in GitHub PR comments or other locations that support Markdown formatting.

---

## Quick Start

To use this action in your own workflow, add the step below in your own Action:

```YAML
- name: 
  uses: de-taylor-scb/
  with:
    path: /path/to/file.xml
    output: /path/to/report.md
    reportType: 'testResult|coverage'
    reportSchema: 'nunit3|jacoco'
```

The `testResults.xml` file should be an ouput from Pester, a unit testing framework for PowerShell, and it should be in the NUnit3 code coverage schema. This Action does not currently support any other schemas.

## Full Documentation 

### YAML

This section fully describes the expected and optional inputs for this Action.

```YAML
- name: 
  uses: de-taylor-scb/
  with:
    path: 
    output: 
    reportType: 
    reportSchema:
    headingLevel:
    minLineCov: 
    minInstructionCov: 
    minMethodCov: 
    minClassCov:
```

### Inputs

Every input is of type string.

None of these inputs can take an array at this time.

#### `path`

The path string that points to the XML file you want to parse. Must be parseable by pathlib.Path()

```YAML
with:
  path: .\_results\testResults.xml
```

```YAML
with:
  path: .\tests\testResults.xml
```

#### `output`

The path string that points to the location where you want the Markdown file to be written. Must be parseable by pathlib.Path()

```YAML
with:
  output: .\_results\testResults.md
```

```YAML
with:
  output: .\tests\testResults.md
```


#### `reportType`

The type of report that this script is parsing. Each type has restricted schema options. Can be either 'testResult' or 'coverage'.

```YAML
with:
  reportType: 'testResult'
```

```YAML
with:
  reportType: 'coverage'
```

#### `reportSchema`

The specific XML schema that will be used to parse this XML report. Each report type has restricted schema options. Can be either 'nunit3' for testResult or 'jacoco' for coverage. More schema options will become available over time.

```YAML
with:
  reportSchema: 'nunit3'
```

```YAML
with:
  reportSchema: 'jacoco'
```

#### `headingLevel`

The topmost heading that should be included in the report. e.g. 1 for H1 (#), 2 for H2 (##), and so on. All other headings will be placed relative to the top level. Defaults to 3 (###).

```YAML
with:
  headingLevel: 1
```

```YAML
with:
  reportSchemav: 3
```

#### `minLineCov`

The minimum coverage threshold for line coverage, between 0.0 and 100.0

```YAML
with:
  minLineCov: 0.0
```

```YAML
with:
  minLineCov: 75.0
```

#### `minInstructionCov`

The minimum coverage threshold for instruction coverage, between 0.0 and 100.0

```YAML
with:
  minInstructionCov: 0.0
```

```YAML
with:
  minInstructionCov: 70.0
```

#### `minMethodCov`

The minimum coverage threshold for method coverage, between 0.0 and 100.0

```YAML
with:
  minMethodCov: 0.0
```

```YAML
with:
  minMethodCov: 80.0
```

#### `minClassCov`

The minimum coverage threshold for class coverage, between 0.0 and 100.0

```YAML
with:
  minClassCov: 0.0
```

```YAML
with:
  minClassCov: 100.0
```

---

## Local Script Run Examples

Here are a few locally-run examples demonstrating the inputs and outputs. I have provided both the `tests\` and `_reports\` directories for reproducibility.

The `tests\` directory contains the sample `testResults.xml` input files.

The `_reports\` directory contains the sample `testResults.md` output files.

### Example 1:

**Command**

```PowerShell

```

**Output**
```Text

```

**`testResults.xml`**

```XML
```

**Sample Markdown Output**
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
  uses: Stylecraft-Builders/Prettify-Pester-Reports@v0.1.0
  with:
    path: /path/to/file.xml
    output: /path/to/report.md
    reportType: 'testResult|coverage'
    reportSchema: 'nunit3|jacoco'
```

At this time, the following `reportType` and `reportSchema` combinations are supported:

- `reportType`
  - `nunit3`
- `reportSchema`
  - `jacoco`

## Full Documentation 

### YAML

This section fully describes the expected and optional inputs for this Action.

```YAML
- name: 
  uses: Stylecraft-Builders/Prettify-Pester-Reports@v0.1.0
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

The path string that points to the XML file you want to parse. Must be parseable by pathlib.Path(). This is the location provided to Pester as `$configuration.TestResult.OutputPath` or `$configuration.CodeCoverage.OutputPath` in the Pester configuration, depending on which report type you are converting.

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
  headingLevel: 3
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

See the PyTest tests for more information on running this module locally.
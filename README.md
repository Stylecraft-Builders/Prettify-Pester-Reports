# Prettify Pester Results

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
    path: 
    output: 
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
    title: 
    maxHeadingLevel: 
```

### Inputs

Every input is of type string.

None of these inputs can take an array at this time.

#### `path`

Specifies the path for the testResults.xml file to convert to Markdown. This must be a file parsable as XML. This input defaults to `.\_results\testResults.xml`, which is the expected location for code coverage reports for my organization.

```YAML
with:
  path: .\_results\testResults.xml
```

```YAML
with:
  path: .\tests\testResults.xml
```

#### `output`

Specifies the location of the Markdown output file. This input defaults to `.\_results\testResults.md`, which is the expected location for code coverage reports for my organization.

```YAML
with:
  output: .\_results\testResults.md
```

```YAML
with:
  output: .\tests\testResults.md
```


#### `title`

Specifies the title of the Markdown Report. For example, providing the repository name. Defaults to "NUnit3 Test Results".

```YAML
with:
  title: 'NUnit3 Test Results'
```

```YAML
with:
  title: 'My-Module Test Results Report (NUnit3)'
```

#### `maxHeadingLevel`

The topmost heading that should be included in the report. e.g. 1 for H1 (#), 2 for H2 (##), and so on. All other headings will be placed relative to the top level. Defaults to 3 (###).

This input was created so that Markdown reports could be produced at the appropriate subheading level, for example inside of an existing document.

This number corresponds to the number of '#' characters inserted into the Markdown for the highest-level subheading in this report.

```YAML
with:
  maxHeadingLevel: 3
```

```YAML
with:
  maxHeadingLevel: 1
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
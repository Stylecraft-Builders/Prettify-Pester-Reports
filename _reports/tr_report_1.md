### Test Results for New-CustomPackage-Pester

 > Overall Results: Passed in 1.045s

**Start Time:** 2025-12-05 13:34:30
**End Time:** 2025-12-05 13:34:32

| Total Tests | Total Passed | Total Failed | Total Inconclusive | Total Skipped | Total Warnings |
| :---------- | :----------- | :----------- | :----------------- | :------------ | :------------- |
| 7 | 7 | 0 | 0 | 0 | 0 |

_(Random Seed Value: 1763616678)_
#### Test Run Filters Applied

_(Not yet able to parse filters...)_

#### Assembly: Utilities.Tests.ps1 (ID: 1-1000, Run State: Runnable) 

 > Assembly Results: Passed in 1.045s

| Assembly Tests | Assembly Passed | Assembly Failed | Assembly Inconclusive | Assembly Skipped | Assembly Warnings |
| :---------- | :----------- | :----------- | :----------------- | :------------ | :------------- |
| 7 | 7 | 0 | 0 | 0 | 0 |


##### Test Suite Environment

- **platform:** Microsoft Windows 11 Pro|C:\WINDOWS|\Device\Harddisk0\Partition3
- **cwd:** C:\Users\jdoe\Script_Repos\Desktop_Engr\New-CustomPackage
- **machine-name:** Workstation01
- **user:** jdoe
- **os-version:** 10.0.26200
- **framework-version:** 5.7.1
- **user-domain:** domain
- **clr-version:** 9.0.10
- **culture:** en-US
- **uiculture:** en-US
- **os-architecture:** x64

**Describe: Utilities Test Suite (ID: 1-1001, Run State: Runnable)** 

 > Describe Results: Passed in 0.5037s

| Describe Tests | Describe Passed | Describe Failed | Describe Inconclusive | Describe Skipped | Describe Warnings |
| :---------- | :----------- | :----------- | :----------------- | :------------ | :------------- |
| 7 | 7 | 0 | 0 | 0 | 0 |



**Context: Run-CustomFunction1 (ID: 1-1002, Run State: Runnable)** 

 > Context Results: Passed in 0.3284s

| Context Tests | Context Passed | Context Failed | Context Inconclusive | Context Skipped | Context Warnings |
| :---------- | :----------- | :----------- | :----------------- | :------------ | :------------- |
| 4 | 4 | 0 | 0 | 0 | 0 |

**Test Cases**

| ID | Result (Runstate) | Duration | Assert Statements | Description |
| :- | :---------------- | :------- | :---------------- | :---------- |
| 1-1003 | Passed (Runnable) | 0.0524s | 1 | Throws an error if given no valid time server |

**Data-Driven Test: returns <server_exp> on try <num_tries> when given <server_list> (ID: 1-1004, Run State: Runnable)** 

 > Data-Driven Test Results: Passed in 0.2651s

| Data-Driven Test Tests | Data-Driven Test Passed | Data-Driven Test Failed | Data-Driven Test Inconclusive | Data-Driven Test Skipped | Data-Driven Test Warnings |
| :---------- | :----------- | :----------- | :----------------- | :------------ | :------------- |
| 3 | 3 | 0 | 0 | 0 | 0 |

**Test Cases**

| ID | Result (Runstate) | Duration | Assert Statements | Description |
| :- | :---------------- | :------- | :---------------- | :---------- |
| 1-1005 | Passed (Runnable) | 0.2013s | 1 | returns time.windows.com on try 3 when given time.example.com laggy.time.example.com time.windows.com |
| 1-1006 | Passed (Runnable) | 0.0318s | 1 | returns time01.domain.local on try 2 when given time.example.com time01.domain.local time.windows.com |
| 1-1007 | Passed (Runnable) | 0.0321s | 1 | returns time02.domain.local on try 1 when given time02.domain.local time01.domain.local time.windows.com |

**Context: Run-CustomFunction2 (ID: 1-1008, Run State: Runnable)** 

 > Context Results: Passed in 0.4084s

| Context Tests | Context Passed | Context Failed | Context Inconclusive | Context Skipped | Context Warnings |
| :---------- | :----------- | :----------- | :----------------- | :------------ | :------------- |
| 3 | 3 | 0 | 0 | 0 | 0 |



**Data-Driven Test: Returns <exp> given <num_samples> samples (ID: 1-1009, Run State: Runnable)** 

 > Data-Driven Test Results: Passed in 0.0623s

| Data-Driven Test Tests | Data-Driven Test Passed | Data-Driven Test Failed | Data-Driven Test Inconclusive | Data-Driven Test Skipped | Data-Driven Test Warnings |
| :---------- | :----------- | :----------- | :----------------- | :------------ | :------------- |
| 3 | 3 | 0 | 0 | 0 | 0 |

**Test Cases**

| ID | Result (Runstate) | Duration | Assert Statements | Description |
| :- | :---------------- | :------- | :---------------- | :---------- |
| 1-1010 | Passed (Runnable) | 0.0518s | 1 | Returns -0.00199635 given 25 samples |
| 1-1011 | Passed (Runnable) | 0.0051s | 1 | Returns -0.00255325 given 10 samples |
| 1-1012 | Passed (Runnable) | 0.0054s | 1 | Returns -0.00203954 given 15 samples |

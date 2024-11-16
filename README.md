# Internal Package Registry

By Setul Parekh, Nicholas Williams, David Reed, Chase McCoy

## Overview

An Internal Package Registry is a private system for managing dependencies within a company (in our case, ACME Corp). It provides enhanced security by allowing control over version numbers. This control ensures that all dependencies are checked for vulnerabilities before use. Additionally, it protects against potential issues introduced in newer versions available on the web, by allowing the company to either wait for a secure version or fix the vulnerability before updating the registry. Thus, it helps maintain system integrity and stability.

An Internal Package Registry is a great showcase of the skills needed for a Backend Developer. Managing and maintaining an internal package registry requires a deep understanding of software dependencies, version control, and security practices. This includes the ability to detect vulnerabilities, fix potential issues, and ensure system stability. Additionally, the internal registry uses a `Command Line Interface (CLI)` to generate metrics for a given public repository. This process involves making API calls to fetch data about the repository. These API calls retrieve comprehensive information such as the number of commits, contributors, branches, pull requests, and other relevant details. Other data gathered includes comments to code ratio. After obtaining the data, the registry system analyzes it to produce meaningful metrics that help in evaluating the repository's health, security, and activity. All of these metrics help determine whether a package can be added to the registry.

This is project is an **industry simulation** where ACME Corporation is hosting a competition to award a lucrative contract. The contract winner will need to build a trustworthy internal package registry. The competition involves creating a `Command Line Interface (CLI)` tool to assess the trustworthiness of GitHub or NPM packages. Your company participated but did not win, leading to its closure. However, you and your team have been hired by the winning company, Beta Software Solutions (BSS), to extend their implementation to meet ACME Corporation's new requirements. This requires refactoring and extending an existing system. The detailed requirements and context for this project are provided below.

Unfortunately, due to cost-saving measures, a live demo is unavailable as the **`AWS and GCP services have been shut down`**.

### Objectives

- Planning for a bigger project
- Refactoring and extending an existing system
- **Efficiency & Security:** Performance considerations and cybersecurity considerations
- **DevOps Skills:** Deploying and monitoring on a modern Cloud platform
- **API Development**: Create robust RESTful APIs
- **Database Management**: Design and manage databases to store package metadata, user information, and other relevant data.
- **CI/CD Pipeline**: Set up continuous integration and continuous deployment pipelines to automate testing and deployment processes.
- **Monitoring and Logging**: Implement monitoring and logging to track system performance, detect issues, and ensure system reliability.
- **Scalability**: Design the system to handle increasing loads and scale efficiently as the number of users and packages grows.
- **Error Handling**: Develop comprehensive error handling and reporting mechanisms to ensure smooth operation and quick resolution of issues.
- **Compliance**: Ensure the system complies with relevant standards and regulations, such as ADA compliance for web interfaces.
- **Collaboration**: Work closely with front-end developers, project managers, and other stakeholders to ensure seamless integration and project success.
- **Testing**: Implement automated testing to ensure code quality and system reliability, including unit tests, integration tests, and end-to-end tests.
- **Deployment**: Deploy the system on modern cloud platforms, ensuring it is accessible, reliable, and secure.


## PART 1: The Command Line Interface (CLI)

Link to Part 1 source code: https://github.com/ECE-461-Project-Nick-David-Setul-Chase/ECE-461-Project

ACME Corporation has announced a lucrative contract opportunity, sparking significant interest among various companies in the tech industry. This contract is highly sought after due to its potential to bring substantial financial rewards and prestige to the winning company. To determine the most suitable candidate, ACME Corporation is hosting a rigorous competition. This competition will evaluate the capabilities and innovation of the participating companies, including your employer, which is one of the key contenders.

The primary requirement for this competition is the development of a deliverable that can be executed through a `Command Line Interface (CLI)`. This deliverable must provide a robust and reliable method for categorizing the trustworthiness of GitHub or NPM packages. 

This competition represents a significant opportunity for your company to showcase its expertise and innovation. Winning the contract with ACME Corporation would not only bring financial benefits but also enhance your company's reputation in the industry. As such, it is crucial to develop a solution that meets and exceeds ACME Corporation's expectations, demonstrating your company's ability to deliver high-quality, reliable, and innovative software solutions.

### Criteria/Requirements

The goal is to create a tool that can assess various aspects of these packages, ensuring that they meet high standards of security, reliability, and maintainability. The CLI tool should be capable of analyzing multiple metrics to determine the trustworthiness of a package. These metrics might include factors such as the number of contributors, the frequency of updates, the presence of comprehensive documentation, the resolution of issues, and the overall activity within the repository. By evaluating these criteria, the tool will help ACME Corporation identify packages that are safe to use and integrate into their systems. In addition to the technical requirements, ACME Corporation is looking for a solution that is user-friendly and efficient. The CLI tool should be easy to install and use, with clear instructions and minimal setup required. It should also be designed to handle large volumes of data, providing accurate and timely results even when analyzing extensive repositories. Sarah, your contact person from ACME Corporation, has provided detailed requirements that the company would like implemented in the deliverable.

#### Project Specifications

- Develop a quick command line interface that can support input from command line arguments
- Easy to learn
- Easy to maintain
- Maintainers are responsive
- High security
- Adaptable structure to accommodate new aspects
- Use `GNU Lesser General Public License v2.1` for all open-source software
- Can produce list of repositories, ordered by trustworthiness

#### Internal Requirements

- Executable file in root directory called `src/`
- Should have the following CLI when executed on Linux machine
    - `./run install`
    - `./run build`
    - `./run URL_FILE`
    - `./run test`
- In event of an error, program should exit with return code 1
- In event of an error, program should print a *useful error message* to the console
- Software must produce a log file stored in the location named in the environment variable `$LOG_FILE` and using the verbosity level indicated in the environment variable `$LOG_LEVEL` (`0` means silent, `1` means informational messages, `2` means debug messages). Default log verbosity is `0`.
- Must be able to run on ECEPROG Linux server
- Each repository should be accompanied by its overall score, as well as sub-scores for `ramp-up time`, `correctness`, `bus factor`, `responsiveness`, and `license compatibility`.
- Should print all output to `stdout`, subject to change. The URL should also be included, as well as a “net score”.
- Returns overall score (range `[0, 1]`) and a score breakdown per category
- `NetScore` is calculated as weighted sum
- Both `Github` and `NPM` URLs will be supported. Any `NPM` repository that does not have a corresponding GitHub repository will not be supported, and an error message will be thrown.
- Program must contain **at least 30%** source lines of code written in Rust

#### Metric Calculations

- Metrics that need to be gathered: developer ramp-up time, code correctness, contributor bus factor, responsive maintainers, and package license.
- Software need only support metric calculation on modules that are hosted on GitHub
- Software should still behave appropriately in other hosting circumstances
- Must create GitHub tokens to programmatically access the GitHub API
- At least one metric must use the `GitHub REST API`
- At least one metric must use the `GitHub GraphQL API`
- Must not conduct “web scraping” of GitHub
- At least one of your metrics must use data from the source code repo, not using GitHub API. Conduct analysis in this order:
    - Clone repo locally
    - Write analysis using programming language of our choice
    - MIGHT WANT TO interact with the Git metadata programmatically
    - MIGHT WANT TO analyze the software itself, but DO NOT execute in an unsandboxed environment


### Metric Operationalizations & Net Score Formula

Given the requirements for Part 1 of this project, we came up with a formula to determine the trustworthiness of a package. This is done done through a rating (the NetScore) which can be divided into its subratings (`RampUp`, `Correctness`, `BusFactor`, `ResponsiveMaintainer`, `License`). 

#### The NetScore rating

The NetScore rating can be calculated through the sum of its subratings. Each subrating has a weight attached that it that indicates how impactful it is towards to NetScore. The weights add up to a total of 1, and each subrating is a value between `[0, 1]`. Shown in the table below are the specific weights of each subrating.

| **Factor** | **Weight** |
| --- | --- |
| RampUp | 3 ( 3/20 = 0.15) |
| Correctness | 4 (4/20 = 0.20) |
| BusFactor | 4 (4/20 = 0.20) |
| ResponsiveMaintainer | 3 ( 3/20 = 0.15) |
| License | 6 (6/20 = 0.30) |
| **Total** | 20 (20/20 = 1) |

$$NetScore = (3 * RampUp + 4 * Correctness + 4 * BusFactor +3 * ResponsiveMaintainer + 6 * License) / 20$$

**Reasoning:** The license is necessary and so it has the highest weighting. Next, the correctness and bus factor are second, as the code should be correct but also not be dependent on only a few contributors. Lastly, the RampUp and ResponsiveMaintainer are considered least significant, as the time to learn and how responsive changes are made is not as important as the correctness.

#### The SubRatings

For PART 1, there are five subrating: `RampUp`, `Correctness`, `BusFactor`, `ResponsiveMaintainer`, and `License`. Below are their formulas, descriptions, and reasonings.

$Correctness=\begin{cases}(closedIssues/allIssues)&\text{allIssues > 0}\\ 0&\text{otherwise} \end{cases}$

- $RampUp = ( README (exists) * .5 ) + ( Documentation (exists) * .5 )$
    - How easily new engineers can ‘ramp up’ or learn the code
    - **Reasoning:** Gives a good idea of the available resources for new developers to understand how the code base operates
- **Correctness** = #closed issues / (# all issues), if # all issues > 0, else 0
    - **Reasoning:** The given formula demonstrates how well the repository contributors respond to inevitable bugs in the code base
- **BusFactor** = 1 - (1 / # of contributors)
    - How many authors can (hypothetically) be hit by a bus and the project is still ok
    - **Reasoning:** Each contributor adds a specific need for the project therefore, the bus factor correspond to the number of contributors
- **ResponsiveMaintainer** = 1 / (weeks since last opened issue)
    - **Reasoning:** Depending on how many and how recent issues were posted, we know if it was more issues recently that there are people maintaining the repo relatively responsively
- **License** = If GNU LGPL 2.1, then 1, else 0
    - **Reasoning:** The repository license must be GNU LGPL 2.1 or it cannot be used by the company

#### API’s Used for Metric Calculations

- GitHub REST API
    - **Reasoning:** Requirement as listed in requirement section.
- GitHub GraphQL API
    - **Reasoning:** Requirement as listed in requirement section**.**
- Beautiful Soup API
    - **Reasoning:** Allows us to analyze NPM repositories, and find if they have a corresponding GitHub repository.

#### Handle URL Feature

We will use regular expressions to determine whether the repository is from GitHub or NPM. Based on that, we will either analyze the GitHub module, or use BeautifulSoup to analyze the NPM page for its corresponding GitHub repository link.

### Architecture

![*Diagram 1: Part 1 Architecture*](https://prod-files-secure.s3.us-west-2.amazonaws.com/ae12f0d5-d761-4fb9-805e-d457c8b478c2/b008941e-6980-4c8d-bdf2-b4604f0c20ff/image.png)

*Diagram 1: Part 1 Architecture*

The flowchart shows how these components work together to analyze and categorize the trustworthiness of packages, ensuring they meet high standards of security, reliability, and maintainability.

- **User**: Interacts with the system through a Command Line Interface (CLI).
- **CLI**: Handles tasks such as installing dependencies, building, and testing.
- **Metric Calculations**: This component processes data to evaluate package trustworthiness (see diagram below).
- **GitHub API**: Provides data from GitHub repositories.
- **Source Repository**: Repository of package being analyzed, interacted with using the GitHub API.

![*Diagram 2: Part 1 Scoring Process*](https://prod-files-secure.s3.us-west-2.amazonaws.com/ae12f0d5-d761-4fb9-805e-d457c8b478c2/291830d2-a97d-4fac-a071-456119011152/image.png)

*Diagram 2: Part 1 Scoring Process*

The image above illustrates the architecture of the system designed to evaluate the trustworthiness of GitHub or NPM packages. At the center of the system is `The Brain`, which acts as the central processing unit and is written in Rust. It is the main process that runs and is responsible for running the `Metricizer` and `Scorer` as well as handling the input/output. The process begins with the CLI. A CLI command is executed to run the program. A command line argument is provided that contains the file name of the list of package URLs. `The Brain` manages the input data through the `File Reader/Writer`, which is then sent to the `Metricizer`, which interacts with various APIs to gather necessary information. The output from the `Metricizer` is metric data in `JSON` format, which is again handled by the `File Reader/Writer`. Finally, the processed data is handled by an output component that interacts with the `Command Line Interface (CLI)`. This flowchart provides a clear and organized representation of the data processing pipeline, highlighting the roles of different components and their interactions, making it easier to understand the flow of data and the roles of various components in evaluating package trustworthiness.

### Deliverable

To download this software, first clone the repository onto a Linux based platform. Next, type and enter the command `./run install` This will install all dependencies needed for proper software execution.

**Note:** In the unlikely event that the run executable file does not exist or work, please type and enter `make` and then `./run install`

**Run**

To run the software, a couple environment variables must be set. Otherwise, the code will throw an error. Please create the environment variables listed below. To create these variables, simply type `export <ENV_VAR>=<VALUE>`.

- `GITHUB_TOKEN` : Your personal GitHub token to access GitHub APIs
- `LOG_LEVEL` : Either 0, 1, or 2. These determine the LOG file outputs.
- `LOG_FILE` : The location you would like the LOG file to be created.

Once environment variables are set, type and enter `./run <URL_FILE>`, where URL_FILE is a text file containing the list of URLs you would like to analyze. Once the process completes, an output file with the NetScore and sub scores for each URL will be created.



























## PART 2: A Trustworthy Package Repository

Link to Part 2 source code: https://github.com/ECE-461-Project-Nick-David-Setul-Chase/ECE461-Project-ACMEIR

**The bad news**: ACME Corporation rejected your company’s deliverable. They decided to proceed with another company’s offering.

**The worse news**: Your company was gambling on a lucrative contract with ACME Corporation. Your company is now out of business, and you are out of a job.

**The good news**: Your competitor, Beta Software Solutions (BSS), won the longer-term ACME Corporation contract. They are awash in cash and hiring software engineers to work on the next phase of the contract. Thanks to your domain expertise, you and your team have been hired for this phase. You will need to extend BSS’s winning implementation to ACME Corporation’s new requirements. As needed, your extension may (1) integrate entirely missing components using your previous company’s implementation; or (2) fix defects, refactor, or overhaul existing components as necessary, but *without* copying code from your previous company’s implementation.

ACME Corporation is continuing to expand its Node.js footprint. They are really benefiting from (your erstwhile competitor’s, now employer’s) tool for identifying trustworthy npm modules. However, they find themselves dissatisfied with aspects of the npm registry and their process for interacting with it:

- npm contains many untrustworthy or irrelevant modules, which pollute the search results.
- ACME Corporation would like to put its own modules – which are trusted, of course – into the same place that third-party modules are stored, but it does not want to share those modules publicly. It seems reputationally hazardous to do so without careful consideration.
- Some of ACME Corporation’s component re-use review processes involve a time-consuming manual inspection, and ACME Corporation doesn’t have a good system in place for tracking which modules have been vetted (investigated). Npm does not support a good way to distinguish vetted from unvetted modules, except via some kind of honor system.
- ACME Corporation’s engineers download many modules, and npm can take a while to serve the desired content.

For these reasons, ACME Corporation would like your team at BSS to develop a custom registry for their npm modules.

Sarah is still your contact person at ACME Corporation. Here are ACME Corporation’s desired requirements, in her words.

### Additional Criteria/Requirements

Your system must support the following general behaviors. Some behaviors are detailed later on, and others are introduced under an appropriate heading.

- Upload, update, rate, and download packages represented as zipped files.
    - Should work for individual packages.
    - Should have support for doing so on package groups, e.g., so that multiple related packages can be updated atomically. Support a three-stage transaction – (a) initiate an empty request; (b) append upload commands to the request, one at a time; and (c) execute the request.
- The “rate” option should provide the net score and sub-scores from Part 1, to inform prospective users of the quality of the module. It should also include **two** **new metrics:**
    - The fraction of dependencies that are pinned to at least a specific major+minor version, *e.g.*, version 2.3.X of a package. (If there are zero dependencies, they should receive a 1.0 rating. If there are two dependencies, one pinned to this degree, then they should receive a ½ = 0.5 rating).
    - The fraction of project code that was introduced through pull requests with a code review.
- Although ACME Corporation may upload its own internal modules to this registry, any such modules will be organized in the style of an npm package.
- Request the ingestion of a public npm package. To be ingestible, the package must score at least 0.5 on each of the metrics indicated in Part 1. If ingestible, the command should proceed to a package upload. You should add any metrics that are missing in BSS’s solution.
- Fetch history for an individual package, including on a particular set of its versions. Support:
    - Exact: “1.2.3”
    - Bounded range: “1.2.3-2.1.0”
    - Tilde and Carat ranges following the definition [here](https://github.com/npm/node-semver). “~1.2.0” or “^1.2.0”.
- Fetch a directory of all packages. Consider that this query may involve an enormous amount of data, e.g., if the registry has millions of packages in it. Choose a design that won’t become a denial-of-service vector.
- Search for a package using a regular expression over package names and READMEs. The results of a package search should resemble the “directory” view, but a subset thereof.
- Track the popularity of packages by downloads and stars. This feature should contain design elements to reduce attempts to artificially inflate a package’s popularity. Popularity information should be included in any search results or directory information for packages.
- The size cost of introducing a package – both directly and via its transitive dependencies, measured in terms of the size of zip files – should be communicated to potential users. Users may wish to query the size cost of multiple packages at once, because those packages might rely on a set of shared dependencies such that the transitive cost of their dependencies is not much higher than the cost of just one of them.
- To reduce storage costs, the “upload” and “update” features should support a “debloat” option that removes unnecessary “bloat” from the package.
- Reset to the default system state (an empty registry with the default user)
- Your system should be accessible via a REST-ful API (HTTP verbs with conventional meanings). You must support, via a REST-ful API:
    - Upload, update, rate, and download individual packages.
    - Support for the new metrics requested by the customer.
    - Ingestion of a public npm package as described
    - Package search
    - Directory of all packages
    - Reset to default system state
- Your system should be accessible via a pleasant and web browser interface that is compliant with the Americans with Disabilities Act (ADA). Use a front-end framework of your choice. Automate your tests with Selenium.
- A security case should be made based on STRIDE.
- Must employ RESTler to scan the system, and document the outcome. If RESTler misbehaves, open issue(s) and indicate how Microsoft resolves them.

ACME Corporation places a high value on CI/CD. Your system should be using GitHub Actions to perform:

- Automated tests (CI/Continuous Integration) on any pull request
    - You might conduct some tests (e.g. end-to-end performance tests with many clients) outside of your automated test pipeline.
- Automated service deployment to GCP on successful merge (CD/Continuous Deployment)

For consistent quality, ACME Corporation requests that every pull request receive a code review from at least two independent evaluators.

- All teams must use at least one GCP component – e.g. a VM with storage attached, hosted on Google Compute Engine.
- Introduce new behaviors using pull requests, with code review by at least one teammate for nonprod and two teammates for prod.

### ACME Corporation’s Budget is not Bottomless

Sarah reminds you that your team members are from an independent contracting firm. She says the company is **willing to pay your team for up to 90 hours per person for this project** and would rather see ***something that works – at least partially! –  by the deadline.***

- Your project plan and your weekly progress updates should reflect an appropriate amount of time for the project, e.g. at least 5 hours per team member per week. If you wait until the last minute, Sarah will be nervous, pull the plug on the project, and might break off future contracts with your company.
- If you begin to deviate from your planned timeline, you should submit a **revised** plan as part of a weekly update. That way Sarah can keep management abreast of progress and aware of any changes in the functionality that will be delivered.
- You should plan your project in such a way that you can deliver incremental value to Sarah even if you cannot complete all of her requirements.
- **PM Note: I will be amazed if any team were able to complete the full set of functionality by the deadline. In your design document, you should have enumerated and organized the requirements, estimated the cost of each feature, and identified the subset of the functionality that you think your team can reasonably deliver. The total desired cost for your team should be roughly 90 hours per person. Estimate and negotiate accordingly.**

### **Starting project analysis**

The project from Part 1 provided by BSS overall seems trustworthy.  They seemed to do a thorough job testing the different modules in the repository.  There are also tests that run the system as a whole.  The only issue is that there is quite a bit of code overall and modules are also parallelized, so it may be harder to debug or it may be more likely to have bugs that haven't been found. These findings do not affect our milestones and timeline since most of the key data we need is given by the previous project. However, if there were some bugs or issues that arise while trying to implement our new system with the project we are building from, it may drastically change how long each milestone will take because of the complexity of their code.

### Validation plan

Correctness will be determined by the percentage of tests passed and also the amount of code coverage achieved.  For Rust code, we will try to use “cargo test” for testing the modules.  This was also used in the code received from the other team, so it seems like a good idea to use the same testing structure.  We will try to test as we go to make sure that what we add to the repository does not have errors, although this may be moved to a separate phase depending on time constraints.  We will also have other teammates do code reviews and will have tests run on pull requests.  We will incorporate logging to log when certain events happen, which will help to see when problems occur, especially when assembling components together.  We are not planning on running performance tests.

### Architecture

| **Tool** | **Justification** |
| --- | --- |
| Python | Entire team is comfortable with Python and Python has robust methods for analyzing and working with data. |
| Rust | For the thirty percent code requirement |
| REST API / GitHub | Used for GitHub actions, getting data |
| Trello | Rather than using GitHub projects to keep track of our project, we will use Trello for progress tracking |
| Visual Studio Code | IDE to code and run all three languages |
| Google Cloud Platforms | Storage and hosting for running our system |
| GCP Cloud Run | Cloud Run is used to host our website front-end. This will be built in Flutter, then containerized and deployed as a Docker image to Cloud Run. |
| GCP Cloud Storage | Cloud Storage will be used to store the actual files in each package |
| GCP Datastore | Datastore will be used to store the metadata associated with each package. Examples include version number, issues, contributors, and any other information that goes into our scoring function. |
| cargo test | Rust test suite to run tests and ensure working condition of system |
| Flutter/Dart | Flutter/Dart will be used for our web interface. This will make developing a web interface easier than using straight HTML, CSS, etc. |
| AWS API Gateway | Provides an easy way to set up an API with the given OpenAPI spec |
| AWS Lambda | Easily connects to API Gateway and allows us to run serverless functions for each API call |
| Google Cloud Firestore | Allows us to store package information, such as metadata and the base64 string representing the files |

**Cloud Run:** Cloud Run is used to host our website front-end. This will be built in Flutter, then containerized and deployed as a Docker image to Cloud Run.

**Cloud Storage:** Cloud Storage will be used to store the actual files in each package

**Datastore:**

Datastore will be used to store the metadata associated with each package. Examples include version number, issues, contributors, and any other information that goes into our scoring function.

![*Diagram 3: Part 2 Architecture*](https://prod-files-secure.s3.us-west-2.amazonaws.com/ae12f0d5-d761-4fb9-805e-d457c8b478c2/69d2d6a7-34bd-4479-b1bf-bc04f8100b1e/image.png)

*Diagram 3: Part 2 Architecture*

![*Diagram 4: Part 2 Cloud Architecture*](https://prod-files-secure.s3.us-west-2.amazonaws.com/ae12f0d5-d761-4fb9-805e-d457c8b478c2/9b15dc3a-2e30-4a50-b1de-cee3e55e4749/image.png)

*Diagram 4: Part 2 Cloud Architecture*

## PART 3: Final Deliverable

### Screenshots

https://lh7-rt.googleusercontent.com/docsz/AD_4nXeHC7qH3WudrGFLJfN0sExTsZ8lLGe-Ya0D0QHyYJXodYaDsbWZlD-j_-Yn3TJz67ntAAwb2EeFOPn8wTmIBrl6tyBX-U4m42CaC6u7Bek26mBbcDGCmG-h-Y8zD630atJd2LNcGhm2PBooQLBZWXa6eMCmv6l08nRF7XGYkw?key=JAMgH77mlo9KnWtQt27gug

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/ae12f0d5-d761-4fb9-805e-d457c8b478c2/7040f3c2-f4cf-4e2f-903b-5a502c8dd480/image.png)

https://lh7-rt.googleusercontent.com/docsz/AD_4nXcXDnbk1v1Y-7VOivW1pZ0HRklSnq-_mrDrrARW53fYO2lmJewRthuIqW80XPC5ap4wBq3NAl9RWz6jZvUEoCiZHIimC8pjQn4TNviBeqCNRhBxEgl-oD_uIDqK96dmqVn8gsTi8NepRGCHpKOXkaZlfvvsPJ9Xmuejsa97vQ?key=JAMgH77mlo9KnWtQt27gug

https://lh7-rt.googleusercontent.com/docsz/AD_4nXeg6soOUX0wyDJpr-l6ZoelZkpwhk8CFoEBNzjRDD4w-jziWayPhUp5XE8FbMTH5mQK-LCnW9r8uWOfmTLgnNW-23xW8B-Z7Bpwf6_X6SrC7XJyJgvTxCKx91ngCpQ-m10sFgJr0bo4zIv3FnOOlRQSTx4_0-LijzYCbCzV?key=JAMgH77mlo9KnWtQt27gug

https://lh7-rt.googleusercontent.com/docsz/AD_4nXct-HDgvRENPEcCF_q29iDGpYKKLAuDqigBqfjLDQxpyTPoqWthQGF8vHa9tn8cg1_-d_MliXKE-XaF1zYRNklRV09cFITCprDqdH6wQY4olEq_4b2D0PmlA24tp6DxI2SUynFpt20dWvQlm0gNqSjeAQvg5iEo9l6nukHI?key=JAMgH77mlo9KnWtQt27gug

https://lh7-rt.googleusercontent.com/docsz/AD_4nXfMohtFL7JEK52afdquJIECsNPcyoyoWEI8nYkLEq_Uphf_Z7HGckMaPV9wGo5QMJR9IMDir1b02huXCTx8dx6TQGsMp9b7eGPEh92-Ihk-cEd7C9BOxjhaznZ25lHGHGQrd6u31nLiyTDNlcyxQht48zNE6gRUwqiz3Kko6g?key=JAMgH77mlo9KnWtQt27gug

### Overview

We have implemented a package manager that operates through an API, as well as a website. The package manager allows users to upload and update packages, download and delete packages by ID, search all packages by name, version, and regular expressions, delete all versions of a package, and provides a rating for each package as well as multiple subratings in different categories. This system allows users to upload their code either through package ingestion of an npmjs link, or through zipping up the contents of their GitHub repository and uploading that. The UI for the system can upload, delete, search, and sort packages.

### Changes made to Starting Project

*Changes to allow us to implement the new metrics*

**Change 1**: Added two new directories within the ‘src/controller’ directory, each with a mod.rs and [new-metric-name].py file to allow for integration of the two new metrics into the part 1 codebase.

**Justification**: The part 1 codebase was structured where each metric has its own subdirectory within the ‘src/controller’ directory. Each metric directory has a corresponding mod.rs file that calculates the metric value, and controls how the data is passed within the rest of the system. Therefore, to implement the two new metrics, we had to create their own subdirectory within the ‘src/controller’ directory, with the mod.rs file. In order to make the calculation process of the new metric values easier, our team added a python script that would be called within mod.rs in each new metric directory to calculate and return the metric value.

**Change 2**: Inside the ‘src/controller’ directory - Modifications to metric.rs, mod.rs, and tests.rs

**Justification**: The combination of these files are used in part 1 code to pass metric data through the rest of the system, to calculate overall scores, and to test the system. These files had to be modified to integrate the two new metrics into the rest of the system. Modifications were relatively simple.

*Changes to improve the reliability of the component so that our Part 2 implementation would satisfy the customer’s requirements.*

**Change 3**: Creation of Bash file

**Justification**: Allowed the team to call the part 1 code within a python script. The Python script would be executed by our Lambda function SSHing into our GCP Compute Instance.

**Change 4**: Creation of ‘acme’ subdirectory

Justification: Allowed the team to easily access the downloaded packages, without the users system impacted where the packages would be stored. All packages were downloaded to this directory within our own repository directory.

**Change 5**: Creation of call_decode.py and decode_and_rate.py

**Justification**: These two python scripts controlled the flow of how our part 1 code would be called, and how the metrics would be returned to our GCP and Firestore databases. Having these files allowed the API to make a single command line call on our VM, and it would only have to read the terminal output in order to collect the package metrics and content.

### ADA Compliance

[Image X: ADA Compliance Certificate](https://lh7-rt.googleusercontent.com/docsz/AD_4nXeR-xCxzOQIn-NHMrHxIFXJ0YmjEJKOBsNeUS_KJSccRkv5oa8D0-HYeglR7JS3aTVmtu98LwWTW5OyTrVyRhf2Ac2KS_KHr_rvdzc1UVW8nt91LVq726cZX0SDVRxv-6Mlh3jhd8xGhLpxQlXDZ5fpotwxeifslO3Bq7DU?key=JAMgH77mlo9KnWtQt27gug)

Image X: ADA Compliance Certificate

### Security requirements

Aligning with the six security properties defined by the STRIDE article (see references), provided below are the security requirements and analysis.

Confidentiality

- [All systems] Someone without API url, website link, or GCP API key can access our data.

Integrity

- [All systems]: Anyone with API key or access to the website or access to the CLI can edit the database.

Availability

- [All systems]: Currently all systems are deployed and accessible. Downtime is only when GCP, AWS, or GitHub have downtimes.

Authentication

- None

Authorization

- None

Nonrepudiation

- None

### Threat model

**Trust boundary #1**

Untrusted party: Outsider

Someone who is attempting to access the data they are not entitled to and is not an ACME employee.

**Trust boundary #2**

Untrusted party: *Insider*

Someone who is attempting to access the data they are not entitled to and is an ACME employee.

**Trust boundary #3**

Untrusted party: *Third-party*

Someone who stumbled upon the website and now has access to the database through it.

**Trust boundary #4**

Untrusted party: *Provider*

GCP, AWS, or GitHub accessing our data or some security breach within the provider giving access to our data.

### Analysis of risks

[*Diagram 5: Security Architecture*](https://lh7-rt.googleusercontent.com/docsz/AD_4nXcD8j_w98SWsf3UBB6Y-r2AMcVcHQPsgu-jbPznJdUWvLP9c1afFUWRpXlmRMhBjyAhN9aNEF3km1lUOineWwxZucIGcsXhfnyRmZrXRJymCx9cl5dTQHWIAIkuwU2xcih3vC_hQZEjroLVmlEVh8BYKb5MQFeZhAMSUJx0hg?key=JAMgH77mlo9KnWtQt27gug)

*Diagram 5: Security Architecture*

Fill out this table for each [STRIDE property](https://docs.microsoft.com/en-us/archive/msdn-magazine/2006/november/uncover-security-design-flaws-using-the-stride-approach) (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege):

**Stride property: Spoofing**

Affected security properties: *Authentication*

Analysis of components:

- We do not have authentication and therefore spoofing would have no effect since they would have access without spoofing anyway.

**Stride property: Tampering**

Affected security properties: *Integrity*

Analysis of components:

- Diagram 5, component 7 – Database: Accessing the database through api or web
- Web connection to database:
    - Mitigations applied: Some database features used on the web are done through a secure link between Firebase API and the website using Google’s package for Firebase.
    - Degree of risk resolution: Low
    - Suggestions for additional mitigations, if needed: Adding authentication so users of website do not directly have access
- API connection to database:
    - Mitigations applied: API is public but you need the URL, which is not stored somewhere that is accessible
    - Degree of risk resolution: Medium

**Stride property: Repudiation**

Affected security properties: *Non-repudiation*

Analysis of components:

- Diagram 5, component 2 – API: Editing the database
- User edits the database and denies:
    - Mitigations applied: There is history for each package and logging of the database to check what time and date someone changed something
    - Degree of risk resolution: Low
    - Suggestions for additional mitigations, if needed: Adding authentication so we know which user edited what

**Stride property: Information disclosure**

Affected security properties: *Confidentiality*

Analysis of components:

- Diagram 5, components 2 and 7 – Access to systems
- Attempt to edit database through any means:
    - Mitigations applied: Only those with API url, website link, or GCP API key are capable of accessing. GCP API key is only stored on local machines with code editing access.
    - Degree of risk resolution: High
    - Suggestions for additional mitigations, if needed: Adding authentication, making API private.
- Client-server network path:
    - Mitigations applied: HTTPS is used for security
    - Degree of risk resolution: Low
    - Suggestions for additional mitigations, if needed: Adding authentication.
- API url, website link:
    - Mitigations applied: All links must be kept secret either memorized or in an encrypted file.
    - Degree of risk resolution: Medium
    - Suggestions for additional mitigations, if needed: Adding authentication.

**Stride property: Denial of service**

Affected security properties: *Availability*

Analysis of components:

- Diagram 5, component 2 – Website, API, and GCP
- Attempt to shutdown or destabilize provider:
    - Mitigations applied: Providers already have high security and therefore have close to no way to be shutdown.
    - Degree of risk resolution: Low

**Stride property: Elevation of privilege**

Affected security properties: *Authentication*

Analysis of components:

- We do not have authentication and therefore spoofing would have no effect since they would have access without spoofing anyway.
- Diagram 5, component 7 – Database
- Injecting malicious JSProgram:
    - Mitigations applied: Program is stored as a string and is not directly run by our systems.
    - Degree of risk resolution: Low

### Risks we mitigated, and how

**Risk 1: Client and server connections**

Mitigation approach: All connections are done through either html or http packages because the packages use https encryption, connections are secure.

### Risks we did not mitigate, and why

**Risk 1: Unauthorized users**

Why not?

We did not have time to implement authentication and therefore anyone with access to the website or API can edit the data. No user sign on is required.

### Deployment: GCP

| **Purpose** | **Selected GCP component(s)** | **Other GCP components considered** | **Justification for selected component** |
| --- | --- | --- | --- |
| Store metadata for each package | Firestore | None | Seemed to be the best existing option for storing json structured data in GCP |
| Store package content | Cloud Storage | Firestore | Firestore maxes out at 1 MB per document, so any packages that exceed that would not work. We therefore opted for Cloud Storage to store the larger base64 strings. |
| Host and run part 1 code | Cloud Compute | None | Provided the proper linux environment to host and run the part 1 code |
| SSH into Cloud Compute instance to trigger part 1 code | Cloud Function | AWS Lambda | AWS Lambda has issues with the Paramiko library because of its natively built sub dependencies with the Cryptography library, so Cloud Function ended up being much easier |

We also used several AWS services to help us complete the service. We used AWS API Gateway to set up our API, and connected each endpoint to a Lambda Function to handle the request and interact with our backend.

### Deployment: CI/CD

Before the code goes into the master branch, we run a python linter over all the code. We mostly wanted to use it for warnings and errors, so we disabled convention and refactor messages. There were also some warnings that were disabled, such as unused arguments and variables, and also statements with no effect since we felt the statement being called out did have an effect. We also disabled the “unable to import” error since the requests package was not accessible during the action. We also ran the test suite that was created by the previous team for the Rust code. We also required one or more reviews.

We were consistent with protecting the master branch. We blocked force pushes, so the pull requests had to be reviewed and the tests passed. However, the continuous deployment was done on a different branch to speed up testing, which is explained in more detail below. In this way we were not consistent, as the deployed resources were changed outside of editing master.

The rust code (which is the rating code) was being tested by the automated test suite while the python code (which is the API code) was being checked by the linter.

There could be defects in the website as this is not checked, although this can be detected in the website's use and would not critically impact API through the terminal and thus would not be a critical failure. There could also be problems in the python code unrelated to the syntax. This could be problematic, but manual testing should resolve this.

[Screenshot of the GitHub action file (e.g. YAML) that defines the CI stages](https://lh7-rt.googleusercontent.com/docsz/AD_4nXeF5DdDwPNOP0AlZbfy58QfM8yqBvNB5965FE85CvCcjDSxB7szPJNfbdjyRlj3ab7hmEUFJ3XqZhzU61vIQIT4hatv4tvaUmERsNCuS0us6rnu4J6xF9Dlyk-LNDenwzg9wA5X0jEvcfL-Kk0lx1sDN9hg6WsL8JX31GH2yw?key=JAMgH77mlo9KnWtQt27gug)

Screenshot of the GitHub action file (e.g. YAML) that defines the CI stages

[Image X: Test](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdjTxWpT96UaMSVtrd9DsNVgbiAh2lp1JulQ44SLHNRPqf-Rwu8cPhO2yfONO4QFF-k5JzSwTmy9AkySW4TZEz9RGKURICT26IDksholCe5TAJ312yGTAqWKOk08_7_v80ws4tXPEJqO9bf3evnFAEKOCMP32SrmFTkkcLA?key=JAMgH77mlo9KnWtQt27gug)

Image X: Test

We are using AWS API Gateway and Lambda functions because of the specification versioning issue and are deploying to the AWS Lambda functions, but although we are using GCP compute engine, cloud storage, a cloud function, and firebase but are not automatically deploying to them. For the lambda functions, since we hadn't deployed our API yet we were doing CD on pushes to a specific Lambda-Functions branch so that the functions could be tested immediately on there. Since this also directly interfaced with the API Gateway, it was useful to keep the deployment on push to Lambda-Functions rather than to master, and is currently still that way, although that is probably something that should be moved to master now that we have a working API. Keeping it in Lambda-Functions makes it much easier to comply with pull request requirements for master, although in turn it makes keeping master safe much less useful. The code in the VM, the cloud function, and in the lambda functions was also changed separately from the GitHub as well.

### Security: RESTler evaluation

Fuzzing and other automated test generation tools are a major part of many software security strategies.

**Overall:**

Our team was unable to implement RESTler to scan our system. Our team spent over 20 hours researching the purpose of RESTler, using RESTler on a real-world API, and trying to get RESTler to work for our API. Additionally, our team had spent a significant amount of time on other parts of the project, and mutually agreed that it was not worth putting in more time due to additional stresses (studying for finals, and other projects).

**What we were able to do with Microsoft RESTler:**

Our team was able to set up RESTler and test the [PokeAPI](https://pokeapi.co/) on a Linux-based virtual machine hosted with Google Cloud Compute Engine, that was solely instantiated for RESTler testing. This process included downloading RESTler on the VM, downloading other needed softwares (Git, Python, WGET, etc.), downloading the PokeAPI specification (.yaml) file, and setting up directories for RESTler outputs. We were able to compile RESTler, run ‘test’, and run ‘fuzz-lean’ on the PokeAPI. Our team attempted configuring and running RESTler for our API, but were unable to get successful test outputs.

## Resources

- **REST APIs**
    - Fielding’s 2000 dissertation: You can start at [Chapter 5](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm) (“REST”) but the [whole thing](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm) is eminently readable and edifiying.
    - 20 years later, [brief commentary](https://twobithistory.org/2020/06/28/rest.html) on what Fielding meant vs. what REST means in practice (and conjectures about why).
    - [REST vs CRUD](https://nordicapis.com/crud-vs-rest-whats-the-difference/)
    - Specifying REST APIs through OpenAPI (formerly known as Swagger): [**https://swagger.io/specification/**](https://swagger.io/specification/)
    - Testing REST APIs: https://github.com/microsoft/restler-fuzzer
- **Google Cloud Platform**
    - Here’s the starting point: **https://cloud.google.com/docs/overview**
- **OWASP Top 10**
- Some common ways that engineers introduce cybersecurity vulnerabilities into the systems they develop: https://owasp.org/www-project-top-ten/
- **STRIDE Security Analysis**
    - [STRIDE](https://learn.microsoft.com/en-us/archive/msdn-magazine/2006/november/uncover-security-design-flaws-using-the-stride-approach)










## License & Rights
### Property of Purdue University ECE 461
### Developed and owned by Nicholas Williams, David Reed, Setul Parekh, Chase McCoy
Dependencies are supported by the [GNU GPL](https://www.gnu.org/licenses/license-list.en.html).
This software has no license support.

![Purdue CompE](https://media.licdn.com/dms/image/C560BAQFFhTOSK0IkUA/company-logo_200_200/0/1628271813820?e=2147483647&v=beta&t=t8XijiB1rlihGVKK4CmSVNxus8YNtV-pzuy91ssdSwE)

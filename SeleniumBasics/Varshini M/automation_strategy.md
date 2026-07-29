# Automation Strategy for Course Management API and Frontend

## Task 1: Automation Decision and Test Case Selection

### 1. Criteria for Deciding Whether a Test Should Be Automated

The following criteria help QA leads decide whether automation is worthwhile.

1. Repetitiveness

- If a test must be run many times, automation is usually efficient.
- Application to the scenario: The POST /api/courses/ test is good for automation because it may be executed repeatedly during regression cycles.

2. High Business Risk

- If failure would cause major impact, automation helps catch issues early.
- Application: Since creating courses is core business functionality, this test should be automated.

3. Regression Value

- Tests that validate stable features across changes are ideal candidates.
- Application: This endpoint should be automated because course creation is a critical regression path.

4. Data-Driven Potential

- If the same workflow must be repeated with many inputs, automation reduces manual effort.
- Application: The same endpoint can be tested with valid, invalid, duplicate, and missing field data using data-driven tests.

5. Stability and Maintainability

- Tests that are unlikely to change frequently are good automation candidates.
- Application: If the endpoint contract is stable, automation is a strong choice. If the API changes often, the script may need more maintenance.

### 2. Manual vs Automated Decisions for Course Management API Tests

| Test Case                                                            | Decision | Justification                                                                                                                        |
| -------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| (a) Regression test for all CRUD endpoints after every code change   | Automate | It is repetitive, high-risk, and ideal for regression coverage.                                                                      |
| (b) Exploratory testing of a new search feature                      | Manual   | Exploratory testing requires human intuition, discovery, and quick adaptation.                                                       |
| (c) Performance test: 100 concurrent users calling GET /api/courses/ | Automate | Performance tests are repetitive and need tooling, but they are best executed with specialized tools rather than only UI automation. |
| (d) UI test for the login form                                       | Automate | UI login flows are common, repetitive, and valuable for regression testing if they are stable.                                       |
| (e) Verify the API documentation (Swagger) is accurate               | Manual   | This is often a content and documentation review task that does not require frequent execution.                                      |
| (f) Smoke test: verify the API is reachable after deployment         | Automate | Smoke tests are short, repetitive, and critical for fast deployment validation.                                                      |

### 3. Test Automation ROI

Test automation ROI is the return on investment gained from automating a test compared with the effort and time of running it manually.

Given:

- Automation effort = 4 hours
- Manual execution time per run = 30 minutes = 0.5 hours

Break-even point before maintenance overhead:

- Number of runs needed = 4 / 0.5 = 8 runs

Maintenance overhead after the 10th run:

- After the 10th run, each additional run has a 20% overhead.
- So the effective manual time per run becomes 0.5 × 1.2 = 0.6 hours.

To recover the original 4-hour investment after the 10th run:

- Remaining time to recover = 4 - (10 × 0.5) = -1 hour

That means the automation pays for itself by the 8th run, and after the 10th run it is already well worth the investment. In practice, the automation is beneficial once it is executed enough times to offset the initial setup cost.

### 4. Flaky Tests

A flaky test is a test that sometimes passes and sometimes fails without any real product change. It undermines trust in the automation suite.

Example:

- A Selenium login test fails intermittently because the page loads slowly and the test tries to click the login button before the element is ready.

Strategies to prevent or fix flaky tests:

1. Use explicit waits instead of fixed sleeps.
2. Stabilize test data and avoid shared state between tests.
3. Isolate tests and remove dependency on timing, environment, or external services where possible.

---

## Task 2: Compare Automation Framework Types

### 5. Comparison of the Five Automation Framework Types

#### Linear Framework

A linear framework is the simplest structure where test cases are written as a straight sequence of steps with little or no reuse. It is suitable for small projects with limited scope.

- Advantage: Easy to create and understand.
- Disadvantage: Difficult to maintain when the test suite grows.
- Example use: A small set of one-off UI tests for a simple course registration page.

#### Modular Framework

A modular framework separates the application into reusable modules or components, and each module is tested independently. This improves structure and maintainability.

- Advantage: Strong reusability and easier maintenance.
- Disadvantage: Requires more upfront planning and design.
- Example use: Reusing common login and course management actions across many tests.

#### Data-Driven Framework

A data-driven framework runs the same test logic with multiple input data sets. Test scripts are separated from test data, which makes them easy to scale.

- Advantage: Excellent for testing many input combinations.
- Disadvantage: Requires careful data management and may be harder to maintain if the logic changes.
- Example use: Testing login with 50 different user/password combinations.

#### Keyword-Driven Framework

A keyword-driven framework uses keywords or action words to represent test steps, making it easier for non-technical team members to create test cases. It is often built on a table or abstraction layer.

- Advantage: Good for business users and non-technical testers.
- Disadvantage: More complex to implement and maintain.
- Example use: A QA team that wants non-technical testers to create scenarios using readable keywords.

#### Hybrid Framework

A hybrid framework combines the attributes of modular, data-driven, and sometimes keyword-driven approaches. It is the most practical option for medium to large automation projects.

- Advantage: Balances reusability, scalability, and flexibility.
- Disadvantage: More complex to design and govern than simpler frameworks.
- Example use: A large Course Management frontend suite with reusable page objects, data-driven login cases, and shared keywords.

### 6. Recommended Framework for the Selenium Suite Scenario

For the Course Management frontend, I recommend a Hybrid framework with a Modular foundation and Data-Driven support.

Why this is the best fit:

- The team must test login with 50 different user/password combinations, which fits a Data-Driven approach.
- The team also needs to reuse login steps across 20 test cases, which fits a Modular approach using page objects and reusable methods.
- The team includes both technical and non-technical members, so keyword-based abstraction can be added optionally to improve readability.

Recommended approach:

- Use Page Object Model for reusable UI interactions.
- Store login credentials and test data in external files.
- Add simple keyword wrappers if non-technical testers need to contribute.

### 7. Suggested Folder Structure for a Hybrid Framework

```text
tests/
  login_tests/
  course_tests/
  dashboard_tests/

page_objects/
  base_page.py
  login_page.py
  course_page.py

test_data/
  login_data.csv
  course_data.json

utilities/
  drivers.py
  helpers.py
  wait_utils.py
  assertions.py

config/
  config.ini
  environment.json

reports/
  screenshots/
  logs/

fixtures/
  conftest.py
```

This structure separates test logic, reusable page objects, external data, utilities, and configuration so the suite remains scalable and maintainable.

# V-Model Analysis and Agile QA

## Task 1: V-Model Mapping

### 1. V-Model Diagram

The V-Model shows development phases on the left side and corresponding testing phases on the right side.

```text
Requirements
  |
System Design
  |
Architecture Design
  |
Module Design
  |
Coding
  |
--------------------------------------
Unit Testing
  |
Integration Testing
  |
System Testing
  |
Acceptance Testing
```

### 2. SDLC ↔ TDLC Phase Mapping with Test Artifacts

| SDLC Phase          | TDLC Phase          | Test Artifact Produced During Development Phase       |
| ------------------- | ------------------- | ----------------------------------------------------- |
| Requirements        | Acceptance Testing  | Acceptance test plan and business requirements review |
| System Design       | System Testing      | System test plan and test scenarios                   |
| Architecture Design | Integration Testing | Integration test strategy and interface test cases    |
| Module Design       | Unit Testing        | Unit test cases and test design documents             |
| Coding              | -                   | Unit test scripts and automated test code             |

### 3. Entry and Exit Criteria for the Four Testing Levels

#### Unit Testing

- Entry Criteria:
  - Module design is complete.
  - Code for the module is available.
  - Unit test cases are prepared.
- Exit Criteria:
  - All planned unit test cases are executed.
  - No open critical or high defects remain.
  - Code compiles and passes unit tests.

#### Integration Testing

- Entry Criteria:
  - Unit testing is complete for the related modules.
  - Interfaces and data contracts are defined.
  - Integration test cases are ready.
- Exit Criteria:
  - All integration test cases are executed.
  - Interface defects are resolved or accepted.
  - No critical integration defects remain open.

#### System Testing

- Entry Criteria:
  - Integration testing is complete.
  - The full system is assembled.
  - Test environment is ready.
- Exit Criteria:
  - All system test cases are executed.
  - No open critical/high defects remain.
  - Business workflows pass end-to-end.

#### Acceptance Testing

- Entry Criteria:
  - System testing is complete.
  - Business requirements and acceptance criteria are approved.
  - Test environment matches production-like conditions.
- Exit Criteria:
  - All acceptance criteria are validated.
  - Stakeholders approve the release.
  - No critical acceptance defects remain.

### 4. Two Early QA Engagement Points in the Course Management API Project

1. Requirements Review

- QA should participate during requirements gathering to clarify ambiguities such as course fields, validation rules, and error messages before development begins.

2. Design Review

- QA should review API design and database schema decisions early to identify gaps in testability, data validation, and error handling before coding starts.

---

## Task 2: Agile QA and Shift-Left Testing

### 5. Problems Caused by Testing Late in Waterfall

In a traditional Waterfall project, testing occurs after development is complete. This creates three main problems for the Course Management API project:

1. Defects are found late, making them more expensive to fix.
2. Requirements misunderstandings are discovered too late, causing rework.
3. The team may miss important validation and reliability issues until the final testing stage.

### 6. QA Role in Agile Ceremonies

#### Sprint Planning

- QA helps define acceptance criteria, identify testable scenarios, and estimate testing effort.

#### Daily Standup

- QA reports blockers such as environment issues, missing test data, or unstable APIs.

#### Sprint Review

- QA validates the demo against acceptance criteria and confirms that the delivered feature is working as expected.

#### Retrospective

- QA contributes ideas to improve test coverage, automation, defect triage, and collaboration.

### 7. Shift-Left Practices Applied to the Course Management API

1. Reviewing requirements for testability

- QA reviews the API requirements to ensure they are clear, measurable, and testable before development starts.

2. Writing test cases before code (TDD/BDD)

- Test cases for course creation, duplicate course codes, and validation errors can be written before implementing the endpoint.

3. Static code analysis

- Tools can be used to detect code smells, security issues, and bad patterns early in development.

4. API contract testing before integration

- The expected request/response format for /api/courses/ can be tested before the full backend integration is completed.

### 8. Acceptance Criteria in Given-When-Then Format

#### Scenario 1: Happy Path

```gherkin
Given a college admin is authenticated
When the admin submits a new course with a unique course code
Then the course should be created successfully and stored in the system
```

#### Scenario 2: Duplicate Course Code

```gherkin
Given a college admin is authenticated
And a course with the same course code already exists
When the admin submits a new course with that duplicate code
Then the system should reject the request and show a duplicate course code error
```

#### Scenario 3: Missing Required Fields

```gherkin
Given a college admin is authenticated
When the admin submits a new course without a required field such as course name
Then the system should reject the request and display a validation error message
```

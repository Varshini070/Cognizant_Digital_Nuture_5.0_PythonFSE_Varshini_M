# QA Concepts

## Task 1: Map Testing Types to a Real System

### 1. Testing Types Applied to the Course Management API

Below are concrete test cases for the Course Management API.

1. Unit Testing

- Test Case: Verify that the function that validates a course name returns an error when the name is empty.
- Type: Functional
- Why: It checks whether the single function performs its intended behavior correctly in isolation.

2. Integration Testing

- Test Case: Verify that a POST request to /api/courses/ successfully stores the course in the database and returns a success response.
- Type: Functional
- Why: This tests the interaction between the API endpoint and the database layer.

3. System Testing

- Test Case: Verify the full workflow where a college admin sends a course creation request through the API, the course is persisted in the database, and the response confirms the course was created.
- Type: Functional
- Why: This covers the complete end-to-end flow.

4. User Acceptance Testing

- Test Case: Verify that a college admin can create a new course through the interface and confirm that the course appears in the system for academic planning.
- Type: Functional
- Why: This is tested from the perspective of a real business user.

### 2. Non-Functional Example for the API

Non-Functional Test Example:

- Performance Test: Verify that the POST /api/courses/ endpoint responds within 2 seconds under 100 concurrent requests.
- Type: Non-Functional
- Why: This checks how well the API performs under load, not just whether it works.

### 3. Black-Box vs White-Box Testing

- Black-Box Testing: Testing the system without knowledge of internal code structure. The tester validates behavior based on inputs and outputs.
- White-Box Testing: Testing with knowledge of the internal code logic, structure, and implementation.

Typical roles:

- QA tester usually performs Black-Box Testing.
- Developer usually performs White-Box Testing.

### 4. Formal Test Cases for POST /api/courses/

| Test Case ID | Description                               | Preconditions                                                     | Test Steps                                                                                                | Expected Result                                                                  | Actual Result | Pass/Fail |
| ------------ | ----------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ------------- | --------- |
| TC-001       | Create course with valid data             | User is authenticated as admin and database is reachable          | 1. Send POST request to /api/courses/ with valid course name, code, and description. 2. Observe response. | API returns 201 Created and the course is stored in the database.                |               |           |
| TC-002       | Create course with missing required field | User is authenticated as admin                                    | 1. Send POST request without the course name. 2. Observe response.                                        | API returns 400 Bad Request with a clear validation error.                       |               |           |
| TC-003       | Create course with duplicate course code  | User is authenticated as admin and the course code already exists | 1. Send POST request using an existing course code. 2. Observe response.                                  | API returns 409 Conflict or a validation error indicating duplicate course code. |               |           |

---

## Task 2: Defect Lifecycle & Severity Classification

### 5. Defect Lifecycle

The defect lifecycle can be described as follows:

New → Assigned → Open → Fixed → Retest → Verified → Closed

Additional paths:

- Rejected: The defect is not considered valid or reproducible and is closed as rejected.
- Deferred: The defect is valid but is postponed to a later release or sprint due to low priority or time constraints.

### 6. Severity and Priority Classification

#### a) POST /api/courses/ returns 500 Internal Server Error for all requests

- Severity: Critical
- Priority: P1
- Justification: The API is unusable for all users, causing complete failure of core functionality.

#### b) Course names longer than 150 characters are silently truncated without an error

- Severity: Medium
- Priority: P3
- Justification: It affects data quality and validation, but the system remains operational.

#### c) The /docs Swagger page has a typo in the API description

- Severity: Low
- Priority: P4
- Justification: This is a documentation issue and does not affect system functionality.

#### d) Login with correct credentials occasionally returns 401 on the first attempt

- Severity: Medium
- Priority: P2
- Justification: It causes intermittent authentication failures and reduces reliability, but it may not affect all users all the time.

### 7. Complete Defect Report for Bug (a)

| Field              | Value                                                                                                                                      |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Defect ID          | DEF-001                                                                                                                                    |
| Title              | POST /api/courses/ returns 500 Internal Server Error for all requests                                                                      |
| Environment        | QA Environment, Chrome, API v1.0                                                                                                           |
| Build Version      | Build 1.2.0                                                                                                                                |
| Severity           | Critical                                                                                                                                   |
| Priority           | P1                                                                                                                                         |
| Steps to Reproduce | 1. Open the API client. 2. Authenticate as admin. 3. Send a POST request to /api/courses/ with valid course data. 4. Observe the response. |
| Expected Result    | The API should return 201 Created and save the course successfully.                                                                        |
| Actual Result      | The API returns 500 Internal Server Error for all requests.                                                                                |
| Attachments        | Screenshot of 500 error                                                                                                                    |

### 8. Severity vs Priority

- Severity measures how serious the impact of a defect is on the system.
- Priority measures how urgently the defect should be fixed.

Example:

- A typo on the CEO dashboard may have Low Severity but High Priority because it affects executive visibility and business perception.
- In contrast, a backend bug that affects only a test environment may have High Severity but Low Priority if it is not used in production yet.

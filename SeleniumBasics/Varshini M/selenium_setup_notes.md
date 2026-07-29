# Selenium Setup Notes

## Environment Setup

- Install Selenium and webdriver-manager using:
  pip install selenium webdriver-manager

## Script Summary

- setup_test.py launches Chrome in headless mode, opens the LambdaTest Selenium Playground, prints the title, and closes the browser.
- navigation_test.py navigates to the Simple Form Demo page, opens a new tab, switches between tabs, and saves a screenshot.

## Important Notes

- Implicit waits are convenient but should be used sparingly because they apply globally and can make tests slower.
- Explicit waits are preferred for modern Selenium automation because they are more reliable and targeted.

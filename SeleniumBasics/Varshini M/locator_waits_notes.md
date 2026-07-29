# Locator and Wait Strategy Notes

## Locator Strategy Ranking

1. ID
2. CSS Selector
3. Name
4. Class Name
5. XPath
6. Absolute XPath

## Why this ranking?

- ID and CSS selectors are usually unique, fast, and readable.
- XPath is more flexible but can become brittle when the DOM structure changes.
- Absolute XPath is the least preferred because even small HTML changes break the locator.

## Explicit Waits vs Sleep

- time.sleep() pauses execution blindly and can make tests slower and less reliable.
- WebDriverWait and Expected Conditions make tests wait only as long as necessary.
- Explicit waits are preferred because they are faster on good machines and more reliable on slower ones.

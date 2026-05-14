---
name: pytest
description: "Use this skill any time Python testing is involved in any way — as input, output, or both. This includes: writing unit tests, integration tests, or end-to-end tests; reading, parsing, or analyzing existing test files; editing, modifying, or extending test suites; setting up fixtures, mocks, or parametrize; measuring test coverage; debugging failing tests. Trigger whenever the user mentions \"test,\" \"pytest,\" \"unit test,\" \"mock,\" \"fixture,\" \"coverage,\" or references a test_*.py filename, regardless of what they plan to do afterward. If any Python test file needs to be opened, created, or touched, use this skill."
license: Proprietary. LICENSE.txt has complete terms
---

# Pytest Skill

## Quick Reference

| Task | Guide |
|------|-------|
| Write a basic test | Read [basics.md](basics.md) |
| Use fixtures & setup/teardown | Read [fixtures.md](fixtures.md) |
| Mock external dependencies | Read [mocking.md](mocking.md) |
| Parametrize test cases | Read [parametrize.md](parametrize.md) |
| Measure coverage | `pytest --cov=src --cov-report=term-missing tests/` |
| Run a specific test | `pytest tests/test_foo.py::test_bar -v` |

---

## Reading Existing Tests

```bash
# List all discovered test files and functions
pytest --collect-only

# Show test output with print() statements
pytest -s tests/

# Run with verbose names
pytest -v tests/
```

---

## Writing Tests Workflow

**Read [basics.md](basics.md) for full details.**

1. Identify the function/class under test
2. Define input → expected output pairs
3. Write `test_` functions using `assert`
4. Group related tests in a `Test` class or module
5. Run and verify all pass

---

## Fixtures Workflow

**Read [fixtures.md](fixtures.md) for full details.**

Use when multiple tests share setup logic or need cleanup after running.

---

## Mocking Workflow

**Read [mocking.md](mocking.md) for full details.**

Use when the code under test calls external services, databases, or the filesystem.

---

## Test Design Principles

**Don't write shallow tests.** Asserting that a function returns *something* tells you nothing. Every test should be able to catch a real bug.

### Before Starting

- **Understand what can break**: Read the function under test carefully. What are the edge cases? What happens with empty input, zero, `None`, negative numbers, or very large values?
- **One behavior per test**: Each test function should verify exactly one thing. If you're tempted to add a second `assert` for a different behavior, write a second test.
- **Name tests like sentences**: `test_divide_by_zero_raises_value_error` is better than `test_divide_error`. A failing test name should tell you *exactly* what broke.
- **Arrange → Act → Assert**: Structure every test in three clear phases — set up data, call the function, check the result.

### Test Categories

Choose the right type for each situation:

| Type | When to use | Speed |
|------|-------------|-------|
| **Unit** | Single function/class in isolation | Fast (ms) |
| **Integration** | Multiple components working together | Medium |
| **End-to-end** | Full workflow from input to output | Slow |

**Default to unit tests.** They are fast, isolated, and easy to debug. Write integration tests only when the interaction between components is the thing being tested.

### For Each Function Under Test

**Every public function deserves tests for:**
- Happy path (normal valid input → expected output)
- Edge cases (empty string, zero, `None`, empty list, boundary values)
- Error cases (invalid input → correct exception with correct message)

**Data-driven patterns:**
- Use `@pytest.mark.parametrize` for the same behavior across many inputs
- Use fixtures for shared state that requires setup/teardown
- Use `pytest.approx` for any floating-point comparison

**Mock boundaries:**
- Mock at the boundary of your system (HTTP calls, DB queries, file I/O)
- Never mock the function you are testing
- Assert that mocks were called with the correct arguments

### Marks Strategy

**Use marks to organize large suites:**

| Mark | When to apply |
|------|---------------|
| `@pytest.mark.unit` | Pure function, no I/O |
| `@pytest.mark.integration` | Involves DB, API, or filesystem |
| `@pytest.mark.slow` | Takes > 1 second |
| `@pytest.mark.skip` | Temporarily disabled with a reason |
| `@pytest.mark.xfail` | Known bug, expected to fail |

Register all custom marks in `pytest.ini` to avoid warnings.

### Coverage Targets

| Coverage | Meaning |
|----------|---------|
| < 60% | Dangerous — large untested surface area |
| 60–79% | Acceptable for early-stage projects |
| 80–89% | Good baseline for most projects |
| 90–100% | Aim for critical business logic |

Coverage measures *lines executed*, not *behaviors tested*. 100% coverage with weak assertions is still a weak test suite.

### Avoid (Common Mistakes)

- **Don't assert without a clear reason** — `assert result` passes for `[0]`, `"false"`, `1`. Be explicit: `assert result == expected`
- **Don't test implementation details** — test what the function returns, not how it does it internally
- **Don't share mutable state between tests** — global variables or class attributes modified in one test will silently break another
- **Don't use `time.sleep()` in tests** — mock the clock or use `freezegun` instead
- **Don't catch exceptions silently** — `try/except pass` in a test hides failures
- **Don't write tests just to hit a coverage number** — write them to catch real bugs
- **Don't skip teardown** — unclosed DB connections, temp files, and patched globals will leak into subsequent tests
- **Don't import from `__main__`** — structure source code to be importable without side effects

---

## QA (Required)

**Assume tests have gaps. Your job is to find them.**

Your first test suite is almost never complete. Treat QA as a bug hunt, not a confirmation step. If you found zero missing cases on first inspection, you weren't looking hard enough.

### Content QA

```bash
# Run full suite and show all failures
pytest -v tests/

# Re-run only failed tests from the last run
pytest --lf -v

# Show which lines are NOT covered
pytest --cov=src --cov-report=term-missing tests/

# Branch-level coverage
pytest --cov=src --cov-branch --cov-report=term-missing tests/
```

**Check for common gaps:**

```bash
# Find test files with no parametrize (may need data-driven tests)
grep -rL "parametrize" tests/

# Find test files with no exception coverage
grep -rL "pytest.raises" tests/
```

If grep returns results on critical modules, consider adding more cases.

### Logic QA

**⚠️ USE SUBAGENTS** — even for small suites. You've been writing the tests and will see what you expect, not what's missing. Subagents have fresh eyes.

Review each test file with this prompt:

```
Inspect this test file. Assume there are gaps — find them.

Look for:
- Functions in src/ with no corresponding test
- Happy path tested but no edge cases (None, empty, zero, boundary)
- Exception raised but message/type not asserted
- Mock called but arguments never verified
- Fixture scope too broad (session-scoped fixture holding state across tests)
- Tests that would still pass if the function returned None (weak assertions)
- Tests with multiple unrelated asserts (should be split)
- Hardcoded values that should be parametrized
- Tests that depend on execution order

For each test function, list issues or gaps, even if minor.
```

### Verification Loop

1. Write tests → Run suite → Check coverage report
2. **List uncovered lines and missing edge cases** (if none found, look again more critically)
3. Add missing tests
4. **Re-run and verify coverage improved** — one addition often reveals another gap
5. Repeat until a full pass shows no new issues

**Do not declare the suite complete until you've done at least one gap-find-and-fill cycle.**

---

## Running Tests

```bash
pytest                                               # Run all tests
pytest tests/                                        # Run tests in tests/ directory
pytest tests/test_calculator.py                      # Run a specific file
pytest tests/test_calculator.py::test_add            # Run a specific function
pytest tests/test_calculator.py::TestCalc::test_add  # Run a method in a class
pytest -v                                            # Verbose output
pytest -s                                            # Show print() output
pytest -x                                            # Stop on first failure
pytest --lf                                          # Re-run only last failures
pytest -k "add"                                      # Run tests matching name
pytest -m unit                                       # Run tests by mark
pytest -m "not slow"                                 # Exclude by mark
pytest -q                                            # Quiet mode
pytest -n auto                                       # Run in parallel (pytest-xdist)
```

---

## Dependencies

- `pip install pytest` — test runner and framework
- `pip install pytest-cov` — coverage measurement
- `pip install pytest-mock` — cleaner mock interface via `mocker` fixture
- `pip install pytest-xdist` — parallel test execution (`pytest -n auto`)
- `pip install freezegun` — freeze/mock `datetime.now()` in tests
- `pip install factory-boy` — generate test data and model factories
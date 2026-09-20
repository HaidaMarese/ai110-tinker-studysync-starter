# StudySync — AI110 Tinker Project

This repository contains my work for the AI110 **Tinker 1B, 2B, and 3B** in-class activities. All three tinkers build on the same StudySync project, with each activity focusing on a different module.

> Original starter repository: [`codepath/ai110-tinker-studysync-starter`](https://github.com/codepath/ai110-tinker-studysync-starter)

## Tinker Activities

| Tinker | Focus | Files |
|---|---|---|
| 1B — Split the Logic | Writing a `pytest` test and completing a cross-file refactor | `scoring.py`, `scoring_helpers.py`, `test_scoring.py` |
| 2B — Wire It Up | Streamlit `session_state`, input validation, dataclasses, and recurring dates | `sessions.py`, `app.py` |
| 3B — Rank & Explain | CSV loading, weighted scoring, ranking explanations, and a data-flow diagram | `ranking.py`, `data/study_spots.csv`, `diagram.mmd` |

## Clone My Repository

```bash
git clone https://github.com/HaidaMarese/ai110-tinker-studysync-starter.git
cd ai110-tinker-studysync-starter
```

## Setup

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate it on Windows Command Prompt

```cmd
.venv\Scripts\activate.bat
```

### Activate it on Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Activate it on macOS, Linux, Git Bash, or WSL

```bash
source .venv/bin/activate
```

### Install the dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the Application

```bash
python -m streamlit run app.py
```

## Run the Session Scorer

```bash
python scoring.py
```

Expected output:

```text
Raw: 55 -> Boosted: 61 -> Rating: Meh
Raw: 68 -> Boosted: 74 -> Rating: OK
Raw: 82 -> Boosted: 88 -> Rating: Good
Raw: 91 -> Boosted: 97 -> Rating: Great
Raw: 77 -> Boosted: 83 -> Rating: Good
```

## Run the Tests

```bash
python -m pytest
```

After completing Tinker 1B, the expected result is:

```text
2 passed
```

## Files

- `app.py` — Streamlit entry point that connects the three tabs.
- `scoring.py` — Contains `session_rating()` and the Session Scorer tab.
- `scoring_helpers.py` — Contains the helper extracted during Tinker 1B.
- `sessions.py` — Contains the session log used during Tinker 2B.
- `ranking.py` — Contains the study-location ranking logic used during Tinker 3B.
- `data/study_spots.csv` — Contains sample data for ranking.
- `diagram.mmd` — Contains the Mermaid data-flow diagram for Tinker 3B.
- `test_scoring.py` — Contains the tests for `session_rating()`.
- `REFLECTION.md` — Contains my Tinker 1B reflection and breaker-input results.

## Tinker 1B — Split the Logic

### Test Added

I added a boundary test to verify that a score of `80` receives a `"Good"` rating:

```python
def test_session_rating_boundary_80_is_good():
    assert session_rating(80) == "Good"
```

Testing the function before refactoring created a behavioral baseline that could detect accidental changes.

### Cross-File Refactor

I moved `apply_streak_bonus()` from `scoring.py` to `scoring_helpers.py`:

```python
def apply_streak_bonus(combined_score: int, streak_days: int) -> int:
    """Add a bonus for consecutive study days, capped at 100."""
    boosted = combined_score + streak_days * 2
    return min(boosted, 100)
```

I imported it into `scoring.py` with:

```python
from scoring_helpers import apply_streak_bonus
```

The refactor improved the code organization without changing the program’s behavior.

## Breaker Inputs

| Input | Result | Decision |
|---|---|---|
| `session_rating(-10)` | `"Skip"` | Flagged as out of scope because the application normally provides nonnegative scores. |
| `session_rating(150)` | `"Great"` | Flagged as out of scope because the expected score range ends at 100. |
| `session_rating(87.5)` | `"Good"` | Accepted because decimal values work with the existing numeric comparisons. |

The score of `150` was the most surprising breaker input because it returned `"Great"` instead of rejecting a score above the expected maximum.

## How I Used AI

I used an AI coding assistant to investigate the relevant Python code, understand the expected behavior, make focused changes, and verify the results in the running application.

I treated the AI suggestions as hypotheses. I checked the suggested boundary test against the conditions in `session_rating()`, ran the test suite, and confirmed that the program produced identical results after the refactor.

## Author

**Haida Makouangou — UNC Charlotte Graduate**  
AI110 — Intro to AI-Native Programming  
CodePath — Fall 2026
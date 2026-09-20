# Tinker: Split the Logic Reflection

## What was misplaced?

`apply_streak_bonus()` worked correctly, but it was misplaced in `scoring.py`. I moved it to `scoring_helpers.py` and imported it into `scoring.py` without changing its behavior.

## Why did I test working code?

I tested `session_rating()` before refactoring so the assertions could detect any accidental behavior changes.

## AI suggestion I accepted

I accepted the suggestion to use `from scoring_helpers import apply_streak_bonus`. I verified it by running `python scoring.py` and confirming that all five results remained identical.

## AI suggestion I checked or adjusted

I checked the suggested boundary test against the conditions in `session_rating()` before using it. The code confirmed that a score of `80` should return `"Good"`.

## Breaker inputs

- `session_rating(-10)` returned `"Skip"`. I flagged negative-score validation as out of scope because the application normally supplies nonnegative scores.
- `session_rating(150)` returned `"Great"`. I flagged scores above 100 as out of scope because the application normally limits the score.
- `session_rating(87.5)` returned `"Good"`. I accepted this result because Python can compare decimal values with the existing numeric boundaries.

## Most surprising breaker input

The score of `150` surprised me most because the function returned `"Great"` instead of rejecting a value above the expected maximum.

## What I learned

I learned that a refactor changes the organization of code without changing its behavior, and pytest assertions help verify that the behavior remains correct.

## Author

**Haida Makouangou — UNC Charlotte Graduate**  
AI110 — Intro to AI-Native Programming  
CodePath — Fall 2026
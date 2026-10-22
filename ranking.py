"""
StudySync -- Find a Study Spot (Ticket 3, Tinker 3B).

Load study spots from CSV, score them against a student profile,
rank the full collection, and explain the top results.
"""

import csv

NOISE_ORDER = {"quiet": 0, "moderate": 1, "loud": 2}


def load_study_spots(csv_path: str) -> list:
    """
    Load study spots from a CSV into a list of dicts, converting
    "distance_miles" to float and "seats_available" to int.
    """
    spots = []

    with open(csv_path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["distance_miles"] = float(row["distance_miles"])
            row["seats_available"] = int(row["seats_available"])
            spots.append(row)

    return spots


def score_study_spot(profile: dict, spot: dict) -> tuple:
    """
    Score one study spot against a student profile.

    profile example: {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}

    Return (score, reasons) where reasons is a list of short strings
    explaining what contributed to the score.
    """
    score = 0.0
    reasons = []

    # Noise match: 3 points.
    noise_level = spot["noise_level"]
    max_noise = profile["max_noise"]

    if NOISE_ORDER[noise_level] <= NOISE_ORDER[max_noise]:
        score += 3
        reasons.append(
            f"noise {noise_level} meets limit {max_noise} (+3)"
        )
    else:
        reasons.append(
            f"noise {noise_level} exceeds limit {max_noise} (+0)"
        )

    # Distance match: 2 points.
    distance = spot["distance_miles"]
    max_distance = profile["max_distance"]

    if distance <= max_distance:
        score += 2
        reasons.append(
            f"{distance:.1f} miles is within {max_distance:.1f} (+2)"
        )
    else:
        reasons.append(
            f"{distance:.1f} miles exceeds {max_distance:.1f} (+0)"
        )

    # Seating match: 1 point.
    seats = spot["seats_available"]
    min_seats = profile["min_seats"]

    if seats >= min_seats:
        score += 1
        reasons.append(
            f"{seats} seats meets minimum {min_seats} (+1)"
        )
    else:
        reasons.append(
            f"{seats} seats is below minimum {min_seats} (+0)"
        )

    return score, reasons


def rank_study_spots(profile: dict, spots: list, k: int = 3) -> list:
    """
    Score every study spot, then return the top k as (spot, score, reasons)
    tuples, sorted by score descending.
    """
    scored_spots = []

    for spot in spots:
        score, reasons = score_study_spot(profile, spot)
        scored_spots.append((spot, score, reasons))

    return sorted(
        scored_spots,
        key=lambda result: result[1],
        reverse=True,
    )[:max(0, k)]


def format_results(ranked: list) -> None:
    """Print each ranked study spot with its score and reasons, one line each."""
    for position, (spot, score, reasons) in enumerate(ranked, start=1):
        print(
            f"{position}. {spot['name']} -- Score: {score:.1f}"
            f" -- Because: {', '.join(reasons)}"
        )


def render_study_spot_tab():
    import streamlit as st

    st.subheader("Find a Study Spot")
    max_noise = st.selectbox("Max noise level", ["quiet", "moderate", "loud"], index=1)
    max_distance = st.slider("Max distance (miles)", 0.0, 3.0, 1.0)
    min_seats = st.number_input("Minimum seats needed", min_value=1, value=4, step=1)

    if st.button("Find spots"):
        profile = {"max_noise": max_noise, "max_distance": max_distance, "min_seats": min_seats}
        spots = load_study_spots("data/study_spots.csv")
        ranked = rank_study_spots(profile, spots, k=3)

        for spot, score, reasons in ranked:
            st.write(f"**{spot['name']}** -- Score: {score:.1f} -- Because: {', '.join(reasons)}")


if __name__ == "__main__":
    spots = load_study_spots("data/study_spots.csv")
    profile = {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}
    ranked = rank_study_spots(profile, spots, k=3)
    format_results(ranked)
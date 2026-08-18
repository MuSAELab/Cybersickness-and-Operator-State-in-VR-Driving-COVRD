"""
anonymize_demographics.py

Applies the anonymization requests from the data-privacy review to:
  1. raw_demographic_info.csv           -> anonymized_demographic_info.csv
  2. processed_demo_info.csv            -> anonymized_processed_demo_info.csv
  3. processed_merged_ratings_and_demo.csv -> anonymized_processed_merged_ratings_and_demo.csv

Changes made (per review):
  - Age -> 4-bin age group: 15-25, 26-29, 30-33, 34+
  - Native language -> boolean "Native language is French" (yes/no)
  - Medical condition free text -> "Yes"/"No" (no condition details retained)
  - GAD-7 individual item scores (gad_1 ... gad_7) -> single summed "gad_total" column
  - Free-text comments/concerns -> "Yes"/"No" (no free text retained)

Run:
    python3 anonymize_demographics.py
"""

import csv
import io

UPLOAD_DIR = "/mnt/user-data/uploads"
OUTPUT_DIR = "/mnt/user-data/outputs"

AGE_BINS = [
    (15, 25, "15-25"),
    (26, 29, "26-29"),
    (30, 33, "30-33"),
]


def age_to_group(age: int) -> str:
    """Map a raw age to one of the four review-specified bins."""
    age = int(age)
    for low, high, label in AGE_BINS:
        if low <= age <= high:
            return label
    return "34+"


def yes_no_from_freetext(value: str) -> str:
    """Collapse a free-text column into a generic Yes/No.

    Any response that is effectively 'No' (case-insensitive, blank, etc.)
    stays 'No'. Anything else (i.e. the participant wrote something) becomes
    a generic 'Yes' so the specific content can't be used to self-identify.
    """
    if value is None:
        return "No"
    cleaned = value.strip()
    if cleaned == "" or cleaned.lower() == "no":
        return "No"
    return "Yes"


# ---------------------------------------------------------------------------
# 1. raw_demographic_info.csv -> anonymized_demographic_info.csv
# ---------------------------------------------------------------------------

def anonymize_raw_demographic_info():
    src = f"{UPLOAD_DIR}/raw_demographic_info.csv"
    dst = f"{OUTPUT_DIR}/anonymized_demographic_info.csv"

    # Source file has some non-UTF-8 (Windows-1252) punctuation (curly
    # apostrophes), so decode with cp1252 and write clean UTF-8 out.
    with open(src, "rb") as f:
        raw_bytes = f.read()
    text = raw_bytes.decode("cp1252")

    reader = csv.DictReader(io.StringIO(text))

    gad_cols = [
        "Feeling nervous, anxious, or on edge?",
        "Not being able to stop or control worrying?",
        "Worrying too much about different things?",
        "Trouble relaxing?",
        "Being so restless that it\u2019s hard to sit still?",
        "Becoming easily annoyed or irritable?",
        "Feeling afraid as if something awful might happen?",
    ]

    fieldnames = [
        "Condition",
        "Participants",
        "Age_group",
        "Gender",
        "Native_language_is_French",
        "Education level",
        "Have you used virtual reality (VR) before?",
        "How often do you use VR?",
        "Medical_condition",
        "GAD_total",
        "Comments_or_concerns",
    ]

    rows_out = []
    for row in reader:
        gad_total = sum(int(row[c]) for c in gad_cols)

        rows_out.append({
            "Condition": row["Condition"],
            "Participants": row["Participants"],
            "Age_group": age_to_group(row["Age"]),
            "Gender": row["Gender"],
            "Native_language_is_French": "Yes" if row["Native language"].strip().lower() == "french" else "No",
            "Education level": row["Education level"],
            "Have you used virtual reality (VR) before?": row["Have you used virtual reality (VR) before?"],
            "How often do you use VR?": row["How often do you use VR?"],
            "Medical_condition": yes_no_from_freetext(
                row["Do you have any medical conditions that could affect your experience in VR? (e.g., epilepsy, vestibular disorders, anxiety disorders, migraines)"]
            ),
            "GAD_total": gad_total,
            "Comments_or_concerns": yes_no_from_freetext(
                row["Do you have any comments or concerns before the experiment?"]
            ),
        })

    with open(dst, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"Wrote {dst} ({len(rows_out)} rows)")


# ---------------------------------------------------------------------------
# 2. processed_demo_info.csv -> anonymized_processed_demo_info.csv
# ---------------------------------------------------------------------------

def anonymize_processed_demo_info():
    src = f"{UPLOAD_DIR}/processed_demo_info.csv"
    dst = f"{OUTPUT_DIR}/anonymized_processed_demo_info.csv"

    with open(src, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    gad_cols = ["gad_1", "gad_2", "gad_3", "gad_4", "gad_5", "gad_6", "gad_7"]
    fieldnames = ["exp", "subjects", "age_group", "sex", "vr_use", "gad_total"]

    rows_out = []
    for row in rows:
        gad_total = sum(int(row[c]) for c in gad_cols)
        rows_out.append({
            "exp": row["exp"],
            "subjects": row["subjects"],
            "age_group": age_to_group(row["age"]),
            "sex": row["sex"],
            "vr_use": row["vr_use"],
            "gad_total": gad_total,
        })

    with open(dst, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"Wrote {dst} ({len(rows_out)} rows)")


# ---------------------------------------------------------------------------
# 3. processed_merged_ratings_and_demo.csv -> anonymized_processed_merged_ratings_and_demo.csv
# ---------------------------------------------------------------------------

def anonymize_processed_merged():
    src = f"{UPLOAD_DIR}/processed_merged_ratings_and_demo.csv"
    dst = f"{OUTPUT_DIR}/anonymized_processed_merged_ratings_and_demo.csv"

    with open(src, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    gad_cols = ["gad_1", "gad_2", "gad_3", "gad_4", "gad_5", "gad_6", "gad_7"]
    fieldnames = [
        "exp", "subjects", "age_group", "sex", "vr_use", "gad_total",
        "condition", "nasa_tlx", "dass", "ssq", "subject_exp",
    ]

    rows_out = []
    for row in rows:
        gad_total = sum(int(row[c]) for c in gad_cols)
        rows_out.append({
            "exp": row["exp"],
            "subjects": row["subjects"],
            "age_group": age_to_group(row["age"]),
            "sex": row["sex"],
            "vr_use": row["vr_use"],
            "gad_total": gad_total,
            "condition": row["condition"],
            "nasa_tlx": row["nasa_tlx"],
            "dass": row["dass"],
            "ssq": row["ssq"],
            "subject_exp": row["subject_exp"],
        })

    with open(dst, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"Wrote {dst} ({len(rows_out)} rows)")


if __name__ == "__main__":
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    anonymize_raw_demographic_info()
    anonymize_processed_demo_info()
    anonymize_processed_merged()
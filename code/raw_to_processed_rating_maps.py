"""
raw_to_processed_mapping.py

Data dictionary documenting how raw_demographic_info.csv fields map to
processed_demo_info.csv (and, by extension, processed_merged_ratings_and_demo.csv).

Reverse-engineered by cross-referencing every row of the two files
(joined on Condition/Participants == exp/subjects) -- these are the
actual value pairs that occur in the data, not assumptions.
"""

# --- Column renames (values pass through unchanged) -----------------------

COLUMN_RENAME_MAP = {
    "Condition":                                                      "exp",
    "Participants":                                                   "subjects",
    "Age":                                                            "age",
    "Feeling nervous, anxious, or on edge?":                          "gad_1",
    "Not being able to stop or control worrying?":                    "gad_2",
    "Worrying too much about different things?":                      "gad_3",
    "Trouble relaxing?":                                              "gad_4",
    "Being so restless that it\u2019s hard to sit still?":            "gad_5",
    "Becoming easily annoyed or irritable?":                          "gad_6",
    "Feeling afraid as if something awful might happen?":             "gad_7",
}



GENDER_TO_SEX = {
    "Female": 0,
    "Male": 1,
}


VR_USE_MAP = {
    ("No",  "Never"):                                  0,
    ("Yes", "Never"):                                  0,
    ("Yes", "Rarely (less than once a month)"):        1,
    ("Yes", "Occasionally (1-3 times per month)"):     2,
    ("Yes", "Regularly (more than once a week)"):      3,
}


# --- Columns present in raw but DROPPED from processed_demo_info.csv -------

DROPPED_COLUMNS = [
    "Native language",
    "Education level",
    "Do you have any medical conditions that could affect your experience "
        "in VR? (e.g., epilepsy, vestibular disorders, anxiety disorders, migraines)",
    "Do you have any comments or concerns before the experiment?",
]
# These never made it into processed_demo_info.csv / processed_merged_*.csv
# at all -- not re-coded, just not carried over.

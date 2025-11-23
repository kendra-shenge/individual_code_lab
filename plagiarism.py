#!/usr/bin/env python3
"""
plagiarism.py
Lab 2: Plagiarism Detector
Compares essays/essay1.txt and essays/essay2.txt, shows common words,
computes Jaccard similarity, allows saving a report, and provides a word-search.
"""

import os
import string

# ---------------------------
# Utility / constants
# ---------------------------
STOP_WORDS = {
    "a", "an", "the", "is", "in", "of", "to", "and", "it", "that", "for", "on", "with", "as", "at", "by"
}

ESSAY1_PATH = os.path.join("essays", "essay1.txt")
ESSAY2_PATH = os.path.join("essays", "essay2.txt")
REPORTS_DIR = "reports"
REPORT_FILE = os.path.join(REPORTS_DIR, "similarity_report.txt")


# ---------------------------
# 1) Text processing function
# ---------------------------
def process_text(raw_text):
    """
    Convert to lowercase, remove punctuation, split to words, filter stop words.
    Returns a list of meaningful words (may contain duplicates).
    """
    # Lowercase
    lower = raw_text.lower()
    # Remove punctuation
    translator = str.maketrans("", "", string.punctuation)
    no_punct = lower.translate(translator)
    # Split into words
    words = no_punct.split()
    # Filter stop words and any empty tokens
    clean_words = [w for w in words if w and w not in STOP_WORDS]
    return clean_words


# ---------------------------
# 2) Word search function
# ---------------------------
def word_search(word, raw_text):
    """
    Count occurrences of `word` in raw_text.
    We normalize by lowercasing and stripping punctuation for fair counting.
    Returns integer count.
    """
    if not word:
        return 0
    # normalize both
    translator = str.maketrans("", "", string.punctuation)
    normalized = raw_text.lower().translate(translator)
    tokens = normalized.split()
    return tokens.count(word.lower())


# ---------------------------
# 3) Main program
# ---------------------------
def main():
    # 3.1 Load the two essays
    if not os.path.exists(ESSAY1_PATH) or not os.path.exists(ESSAY2_PATH):
        print("ERROR: Make sure essays/essay1.txt and essays/essay2.txt exist.")
        print("Run setup.sh to create directories, then add the two files into essays/.")
        return

    with open(ESSAY1_PATH, "r", encoding="utf-8") as f:
        essay1_raw = f.read()
    with open(ESSAY2_PATH, "r", encoding="utf-8") as f:
        essay2_raw = f.read()

    # 3.2 Process text to get cleaned word lists
    essay1_words = process_text(essay1_raw)
    essay2_words = process_text(essay2_raw)

    # 3.3 Create sets for unique meaningful words
    set1 = set(essay1_words)
    set2 = set(essay2_words)

    # Safeguard: if both sets empty, avoid division by zero
    if not set1 and not set2:
        print("Both essays have no meaningful words after cleaning. Nothing to compare.")
        return

    # Intersection and union
    intersection = set1.intersection(set2)
    union = set1.union(set2)

    # Jaccard similarity (as percentage)
    if len(union) == 0:
        plagiarism_pct = 0.0
    else:
        plagiarism_pct = (len(intersection) / len(union)) * 100

    # 3.4 Output results
    print("====== Plagiarism Detector Report ======")
    print(f"Unique meaningful words in essay1: {len(set1)}")
    print(f"Unique meaningful words in essay2: {len(set2)}")
    print(f"Common meaningful words (count): {len(intersection)}")
    print(f"Plagiarism (Jaccard) percentage: {plagiarism_pct:.2f}%")
    if plagiarism_pct >= 50:
        print("!!! Similarity is likely (>= 50%).")
    else:
        print("✓ Similarity is low (< 50%).")
    print("----------------------------------------")
    # Print a short list of common words (sorted)
    if intersection:
        print("Some common words (sample):")
        sample = sorted(list(intersection))[:40]  # cap sample to 40 items
        print(", ".join(sample))
    else:
        print("No common meaningful words found.")

    # 3.5 Ask user to save report
    save = input("\nDo you want to save a full report to reports/similarity_report.txt? (y/n): ").strip().lower()
    if save == "y":
        os.makedirs(REPORTS_DIR, exist_ok=True)
        with open(REPORT_FILE, "w", encoding="utf-8") as rep:
            rep.write("Plagiarism Detector Report\n")
            rep.write("==========================\n")
            rep.write(f"Unique meaningful words in essay1: {len(set1)}\n")
            rep.write(f"Unique meaningful words in essay2: {len(set2)}\n")
            rep.write(f"Common meaningful words (count): {len(intersection)}\n")
            rep.write(f"Plagiarism (Jaccard) percentage: {plagiarism_pct:.2f}%\n")
            rep.write("\nCommon words:\n")
            for w in sorted(intersection):
                rep.write(w + "\n")
        print(f"Report saved to {REPORT_FILE}")

    # 3.6 Word search feature (count in original essays)
    while True:
        query = input("\nEnter a word to search (or press Enter to finish): ").strip()
        if query == "":
            break
        count1 = word_search(query, essay1_raw)
        count2 = word_search(query, essay2_raw)
        print(f"'{query}' occurrences -> essay1: {count1}, essay2: {count2}")

    print("\nDone. Thank you.")


if __name__ == "__main__":
    main()


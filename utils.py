from rapidfuzz import fuzz

# using a fuzzy maching function instead of strict matching
def is_match(command, keyword):
    return fuzz.partial_ratio(command, keyword) > 80


# cleaning text function 
def clean_text(text):
    return " ".join(text.lower().strip().split())


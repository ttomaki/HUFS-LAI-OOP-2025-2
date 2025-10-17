import re
import string

def clean_text(s: str) -> str:
    """
    Pipeline:
      1) lowercase
      2) strip
      3) collapse all whitespace to single spaces
      4) remove ASCII punctuation except apostrophes (') and hyphens (-)
    """
    # 1) lowercase
    s = s.lower()

    # 2) strip and 3) collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()

    # 4) remove punctuation except ' and -
    keep = {"'", "-"}
    drop = set(string.punctuation) - keep
    s = "".join(ch for ch in s if ch not in drop)

    # Clean up any extra whitespace after punctuation removal
    s = re.sub(r"\s+", " ", s).strip()

    return s


if __name__ == "__main__":
    def run_tests():
        assert clean_text("  Hello,   WORLD!  ") == "hello world"
        assert clean_text("\tROCK-'N'-ROLL!!") == "rock-'n'-roll"
        assert clean_text("...") == ""
        assert clean_text(" A  B\tC\nD ") == "a b c d"
        print("filters.py tests passed.")
    run_tests()
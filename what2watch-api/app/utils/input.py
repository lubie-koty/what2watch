from difflib import get_close_matches

import pandas as pd


def parse_input_title(title: str, indices: pd.Series) -> str | None:
    title = title.strip()
    if title in indices:
        return title

    matches = get_close_matches(title, indices.index, n=1)
    try:
        return matches[0]
    except IndexError:
        return ''

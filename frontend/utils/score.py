import pandas as pd


def convert_score_to_num(score: str):
    score = str(score).lower()
    mapping = {
        "poor": 1,
        "average": 2,
        "normal": 3,
        "good": 4,
    }
    return mapping.get(score, None)


def normalize_scores_df(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"])
    if "score" in df.columns:
        df["score"] = df["score"].str.lower()
        df["score"] = df["score"].apply(convert_score_to_num)

    return df

import numpy as np
import pandas as pd
import streamlit as st
import joblib


st.title("Kaggle Competition Recommender")


@st.cache
def load_recomendations() -> np.ndarray:
    recomendations = joblib.load("./data/Recommendations.pkl")
    return recomendations


@st.cache
def load_base() -> pd.DataFrame:
    base = joblib.load("./data/UsersCompetitionsMatrix.pkl")
    return base


@st.cache
def load_competitions() -> pd.DataFrame:
    competitions = pd.read_csv(
        "./data/9_1446962_compressed_Competitions.csv.zip", usecols=["Title", "Slug", "Id"]
    )
    competitions["URL"] = [
        f'<a target="_blank" href="https://www.kaggle.com/c/{c}">url</a>'
        for c in competitions["Slug"]
    ]
    competitions = competitions[["Title", "URL", "Id"]]
    return competitions


if __name__ == "__main__":
    recomendations = load_recomendations()
    base = load_base()
    competitions = load_competitions()

    user_name = st.text_input("Write Kaggle ID (Note: NOT Display Name)", "")
    if user_name in base.index:
        user_index = base.index.get_loc(user_name)
        joined_competitions = list(base.loc[user_name][(base.loc[user_name] > 0).values].index)
        candidate_competitions = list(
            base.loc[user_name].index[(-1 * recomendations[user_index]).argsort()]
        )
        score_df = pd.DataFrame(
            {
                "Id": candidate_competitions,
                "Score": sorted(recomendations[user_index], reverse=True),
            }
        )
        recommend_competidions = [
            int(cc) for cc in candidate_competitions if cc not in joined_competitions
        ]
        recommend_competidions = recommend_competidions[:10]
        st.write(f"{user_name} joined {len(joined_competitions)} competitions")
        st.write(f"Details: https://www.kaggle.com/{user_name}/competitions")
        st.subheader("Recomendations")

        res = competitions.copy()
        res = res[res["Id"].isin(recommend_competidions)].reset_index(drop=True)
        res = pd.merge(res, score_df, on="Id", how="inner")
        res = res.sort_values("Score", ascending=False).drop("Id", axis=1).reset_index(drop=True)
        st.write(res.to_html(escape=False), unsafe_allow_html=True)
    elif user_name:
        st.text(f"There is no user named {user_name}. Please write valid Kaggle ID.")

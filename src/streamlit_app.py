import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import numpy as np
from pathlib import Path

from config import CAT, CAT_GROUPS, NUM, NUM_GROUPS, ORDINAL, ONE_STORY_STYLES

st.set_page_config(layout="wide", page_title="Ames House Price Prediction")

base = Path(__file__).resolve().parent


@st.cache_data
def load_data():
    try:
        with open(base / "data"   / "x_test.pickle",       "rb") as f: x     = pickle.load(f)
        with open(base / "data"   / "y_test.pickle",       "rb") as f: y     = pickle.load(f)
        with open(base / "models" / "clf_streamlit.pickle", "rb") as f: clf   = pickle.load(f)
        with open(base / "models" / "mdl_streamlit.pickle", "rb") as f: model = pickle.load(f)
        return x, y, clf, model
    except FileNotFoundError as e:
        st.error(
            f"**Required file not found:** `{e.filename}`\n\n"
            "Make sure the `data/` and `models/` folders are next to `streamlit_app.py` "
            "and contain the four pickle files."
        )
        st.stop()
    except Exception as e:
        st.error(f"**Failed to load model files:** {e}")
        st.stop()


x, y, clf, model = load_data()
max_row = x.shape[0] - 1


def _cat_index(field_name: str, raw_value: str) -> int:
    """Return the selectbox index for a categorical field value."""
    options = CAT[field_name]
    for i, item in enumerate(options):
        if raw_value == item[: item.find(" ")]:
            return i
    return 0


def read_line(line: int):
    """Load row *line* from x into session_state."""
    x_row = x.iloc[line]

    for name, (lo, hi, *_) in NUM.items():
        raw = x_row[name]
        st.session_state[name] = int(np.clip(round(float(raw)), lo, hi))

    for name in CAT:
        idx = _cat_index(name, str(x_row[name]))
        st.session_state[name] = idx
        st.session_state[f"cat_{name}"] = CAT[name][idx]


def on_slider_change():
    read_line(st.session_state["line_slider"])


if "initialized" not in st.session_state:
    read_line(0)
    st.session_state["initialized"] = True

st.title("Ames city house price prediction")

st.slider(
    "Select record number from the test sample",
    min_value=0, max_value=max_row, value=0, step=1,
    key="line_slider",
    on_change=on_slider_change,
)

col1, col2, col3 = st.columns(3)


num_input = {}
with col1.container(border=True):
    st.subheader("Numerical attributes")
    for group_label, fields in NUM_GROUPS.items():
        with st.expander(group_label, expanded=False):
            for name, (lo, hi, step, fmt) in fields.items():
                num_input[name] = st.number_input(
                    f"Enter {name}:",
                    min_value=lo,
                    max_value=hi,
                    step=step,
                    format=fmt,
                    key=name,
                )


cat_button = {}
with col2.container(border=True):
    st.subheader("Categorical attributes")
    for group_label, fields in CAT_GROUPS.items():
        with st.expander(group_label, expanded=False):
            for name, options in fields.items():
                cat_button[name] = st.selectbox(
                    f"Select {name}:",
                    options,
                    index=st.session_state.get(name, 0),
                    key=f"cat_{name}",
                )


def run_validation() -> list[str]:
    warnings = []

    year_built    = num_input.get("Year Built", 0)
    year_remod    = num_input.get("Year Remod/Add", 0)
    flr2          = num_input.get("2nd Flr SF", 0)
    house_style   = cat_button.get("House Style", "")
    style_code    = house_style[: house_style.find(" ")] if house_style else ""

    if year_remod and year_built and year_remod < year_built:
        warnings.append(
            f"**Year Remod/Add** ({year_remod}) is earlier than **Year Built** ({year_built})."
        )

    if flr2 > 0 and style_code in ONE_STORY_STYLES:
        warnings.append(
            f"**2nd Flr SF** is {flr2} ft² but house style is **{house_style}** (one-storey)."
        )

    return warnings


with col3.container(border=True):
    st.subheader("Calculation results")

    current_line = st.session_state.get("line_slider", 0)
    real_price   = float(y.iloc[current_line]) * 1000
    st.caption(f"Real price (test set): **${real_price:,.0f}**")

    validation_warnings = run_validation()
    for w in validation_warnings:
        st.warning(w)

    if st.button("Estimate cost"):
        columns = list(NUM.keys()) + list(CAT.keys())
        data = []

        for name in NUM:
            data.append(num_input[name])

        for name in CAT:
            row = cat_button[name]
            code = row[: row.find(" ")]
            data.append(int(code) if name in ORDINAL else code)

        X_input = pd.DataFrame(columns=columns, data=[data])

        y_class = clf.predict(X_input)
        probs   = clf.predict_proba(X_input)[0]

        pred0 = model[0].predict(X_input)[0]
        pred1 = model[1].predict(X_input)[0]
        pred2 = model[2].predict(X_input)[0]
        pred3 = model[3].predict(X_input)[0]
        price = (probs[0]*pred0 + probs[1]*pred1 + probs[2]*pred2 + probs[3]*pred3) * 1000

        error_pct = (price - real_price) / real_price * 100

        st.metric(
            label="Estimated price",
            value=f"${price:,.0f}",
            delta=f"{error_pct:+.1f}% vs real",
            delta_color="inverse",
        )

        df_probs = pd.DataFrame({
            "Category":    ["Economy", "Comfort", "Business", "Luxury"],
            "Probability": probs,
        })
        fig = px.bar(
            df_probs, x="Category", y="Probability",
            title="Probability of price-category membership",
        )
        st.plotly_chart(fig, use_container_width=True)

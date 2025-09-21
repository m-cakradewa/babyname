import pandas as pd
import streamlit as st
import random
from streamlit import session_state as ss
import plotly.express as px

df = pd.read_excel("baby_names.xlsx")
names = df["Name"].unique().tolist()
def space(n):
    for _ in range(n):
        st.write("")
if "scores" not in ss:
    ss["scores"] = []

if "choices" not in st.session_state:
    ss["choices"] = random.sample(names, 3)
st.markdown("<h2 style='text-align: center;'>Baby Name Picker</h2>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>Pick a baby name, and learn more about each of them!</h5>", unsafe_allow_html=True)
space(2)
for name in ss["choices"]:
    c1,c2 = st.columns([4,.5])
    with c1:
        if st.button(name, key = f"btn_{name}", use_container_width=True):
            # new = pd.DataFrame([{"Name": name, "Score": 1}])
            # ss["scores"] = pd.concat([ss["scores"], new], ignore_index=True)

            ss["scores"].append({"Name": name, "Score": 1})
            ss["choices"] = random.sample(names, 3)
            st.rerun()
    with c2:
        with st.popover("?",use_container_width=True):
            st.subheader(name)
            space(1)
            row = df[df["Name"] == name].iloc[0]
            c3,c4 = st.columns(2)
            with c3:
                st.write("##### Origin & Background")
                st.write(row["Origin & Background"])
            with c4:
                st.write("##### Meaning")
                st.write(row["Meaning"])
            space(2)
            st.write("##### Traits:")
            st.write(row["Illustration / Personality + Quirky Trait"])

with st.expander("See Scoring"):
    space(1)
    if len(ss["scores"]) != 0:
        df = pd.DataFrame(ss["scores"])
        data = df.groupby("Name", as_index=False)["Score"].sum().sort_values("Score", ascending=False)
        fig = px.bar(
    data.head(),
    x="Name",
    y="Score",
    orientation="v",          # vertical
    template="plotly_dark", # dark theme
)
        # Remove text labels on bars
        fig.update_traces(
            texttemplate=None,
            textposition="none",
            width=0.4
        )

        # Clean layout
        fig.update_layout(
            xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )

        # Add names at the end of each bar using annotations
        for idx, row in data.head().iterrows():
            fig.add_annotation(
                x=row["Name"],
                y=row["Score"] + 0.1,   # slightly above bar
                text=row["Name"],
                showarrow=False,
                font=dict(size=14),
                xanchor="center"
            )
        st.plotly_chart(fig, use_container_width=True)
        if st.toggle("Show all names"):
            st.dataframe(data)

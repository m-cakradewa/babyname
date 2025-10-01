import pandas as pd
import streamlit as st
import random
from streamlit import session_state as ss
import plotly.express as px

df = pd.read_excel("baby_data.xlsx", sheet_name="names")
dfp = pd.read_csv("name_popularity.csv")
#st.dataframe(df.head(30))
names = df["names"].unique().tolist()
def space(n):
    for _ in range(n):
        st.write("")
if "scores" not in ss:
    ss["scores"] = []

if "choices" not in st.session_state:
    ss["choices"] = random.sample(names, 5)
st.markdown("<h3 style='text-align: center;'>Baby Name Picker</h2>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;'>Pick a baby name, and learn more about each of them!</h5>", unsafe_allow_html=True)
space(2)
if st.toggle("All Names"):
    dfprint = df.drop(columns=["letters","syllable","first_letter","traits"])
    for i in dfprint.names:
        with st.expander(i):
            row = dfprint[dfprint["names"] == i]
            # st.write(row)
            st.write(row.affiliation.values[0]+": "+row.origin_1.values[0] + " | " + row.origin_2.values[0] + " | " + row.origin_3.values[0])
            space(1)
            st.write("*Meaning:*")
            st.write(row.meaning.values[0])
            space(1)
            st.write("*About the name:*")
            st.write(row.backstory.values[0])
space(3)
for name in ss["choices"]:
    if st.button(name, key = f"btn_{name}", use_container_width=True):
        ss["scores"].append({"Name": name, "Score": 1})
        ss["choices"] = random.sample(names, 5)
        st.rerun()

    with st.expander("?"):
    # with st.expander("", expanded=False):
        st.subheader(name)
        space(1)
        row = df[df["names"] == name].iloc[0]
        c3,c4 = st.columns(2)
        with c3:
            st.write("###### Origin & Background")
            st.write(row["affiliation"]+": "+row["origin_1"] + " / " + row["origin_2"] + " / " + row["origin_3"])
        with c4:
            st.write("###### Meaning")
            st.write(row["meaning"])
        space(2)
        st.write("###### About the name:")
        st.write(row["backstory"])
        # space(1)
#         st.write("###### Popularity:")
#         df_filtered = dfp[dfp["name"] == name]
#         fig = px.line(df_filtered, x ="year",y="popularity",template="plotly_dark")
#         fig.update_layout(
# xaxis_title='Year',
# yaxis_title='Popularity (0-100)',
# yaxis=dict(range=[0, 100]))
#         st.plotly_chart(fig, use_container_width=True, key = "chart_"+name)
space(2)
_,c,_ = st.columns([1,2,1])
space(2)
with c:
    if st.button("Get New Names", use_container_width=False):
        ss["choices"] = random.sample(names, 5)
        st.rerun()

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
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        if st.toggle("Show all scores"):
            st.dataframe(data)

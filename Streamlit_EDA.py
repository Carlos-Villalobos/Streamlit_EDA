import pandas as pd
import streamlit as st
import plotly.express as px

st.title("Titanic Database")
st.header("Data Table of *Titanic*")

@st.cache
def get_data():
    URL = "https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv"
    return pd.read_csv(URL)

df=get_data()
st.dataframe(df.head())

st.code("""@st.cache
def get_data():
    URL = "https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv"
    return pd.read_csv(URL)""", language="python")

#Step 1 sort

st.subheader("Sorting in tables")
st.text("Top five most poor people aboard")
st.write(df.query("Fare>=0").sort_values("Fare", ascending=True).head())


#Step 2 - column filter
st.subheader("Select the data")
default_cols = ["Name", "Sex", "Age"]
cols = st.multiselect("Type of data:", df.columns.tolist(), default=default_cols)
st.dataframe(df[cols].head(10))

#Step 3 - Distributions - Sidebars
st.subheader("Select a range for the age within the sidebar") 
values = st.sidebar.slider("Age range", float(df.Age.min()), float(df.Age.clip(upper=100.).max()), (5., 100.)) 
hist = px.histogram(df.query(f"Age.between{values}", engine='python' ), x="Age", nbins=10, title="Age distribution")
hist.update_xaxes(title="Age") 
hist.update_yaxes(title=" Quantity") 
st.plotly_chart(hist)

#Step 4 - Static Grouping
st.subheader("Average of survivors")
st.table(df.groupby("Age").Pclass.mean().reset_index().round(2).sort_values("Pclass", ascending=False))


#Step 5 - Radio buttons

Sex = st.radio("Sex", df.Sex.unique())

@st.cache
def get_availability(Sex):
    return df.query("""
    Sex==@Sex
    and Fare>0""").Fare.describe(percentiles=[.1,.25,.5,.75,.9,.99]).to_frame().T
st.table(get_availability(Sex))
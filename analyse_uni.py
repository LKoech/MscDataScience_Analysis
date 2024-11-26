import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
@st.cache
def load_data():
    return pd.read_csv('cleaned_data (1).csv')

data = load_data()

# App Title
st.title("University Data Science Programs Analysis")

# Sidebar Options
st.sidebar.title("Explore the Dataset")
analysis_choice = st.sidebar.radio("Select Analysis", [
    "Program Content Comparisons",
    "Trends in Delivery Formats",
    "Core Courses Across Programs",
    "Specializations/Tracks Across Programs",
    "Broader Exploratory Analysis",
])

if analysis_choice == "Program Content Comparisons":
    st.header("Program Content Comparisons")
    selected_cols = st.multiselect("Select Columns for Comparison", data.columns, default=[
        "University Name", "Program Title", "Core Courses", "Specializations/Tracks"
    ])
    st.dataframe(data[selected_cols])

elif analysis_choice == "Trends in Delivery Formats":
    st.header("Trends in Delivery Formats")
    delivery_counts = data["Delivery Format"].value_counts()
    st.bar_chart(delivery_counts)
    st.write("The chart shows the frequency of different delivery formats across programs.")

elif analysis_choice == "Core Courses Across Programs":
    st.header("Core Courses  Across Programs")
    skill_column = "Core Courses"
    skill_data = data[skill_column].dropna()
    skill_keywords = skill_data.str.split(", ").explode().value_counts()
    st.bar_chart(skill_keywords)
    st.write("The chart displays the most frequently emphasized courses across programs.")

elif analysis_choice == "Specializations/Tracks Across Programs":
    st.header("Specializations/Tracks Across Programs")
    
    # Extract and process the data for specializations/tracks
    skill_column = "Specializations/Tracks"
    skill_data = data[skill_column].dropna()
    
    # Tokenize and count occurrences
    from collections import Counter
    skill_keywords = []
    for track in skill_data.unique():
        skill_keywords.extend([token.strip() for token in track.split(",")])  # Split and clean
    skill_counts = Counter(skill_keywords)
    most_common_items_top10 = dict(skill_counts.most_common(10))  # Get the top 10
    
    # Create the matplotlib bar chart
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.barh(list(most_common_items_top10.keys()), list(most_common_items_top10.values()))
    plt.title("Top 10 Specializations/Tracks")
    plt.xlabel("Count")
    plt.ylabel("Specialization/Track")
    plt.gca().invert_yaxis()  # Invert y-axis for better readability
    
    # Render the chart in Streamlit
    st.pyplot(plt)
    
    st.write("The chart displays the top 10 most frequently emphasized specializations/tracks across programs.")

elif analysis_choice == "Broader Exploratory Analysis":
    st.header("Broader Exploratory Analysis")
    st.dataframe(data)
    st.write("Explore the full dataset above. You can use filters or group programs by common attributes.")

# Footer
st.sidebar.info("Built with Streamlit")

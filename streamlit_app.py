import streamlit as st
import pandas as pd

st.title("Onspot Participants List")

# File uploader
fil = st.file_uploader("Upload the Participant Data", type=["csv", "xlsx"])

if fil is not None:
    try:
        # Read CSV or Excel file
        if fil.name.endswith(".csv"):
            df = pd.read_csv(fil)
        else:
            df = pd.read_excel(fil)

        # Clean column names (strip spaces)
        df.columns = df.columns.str.strip()

        # Required columns
        required_columns = ["Name of The Student (Ex: Aravinth S)", "Email address", "Phone Number (Whats App)"]
        preference_columns = [
            "Technical Event for Day 3 (08 Febuary 2025)",
            "Non Technical Event for Day 3 (08 Febuary 2025)",
            "Technical Event for Day 4 (09 Febuary 2025)",
            "Non Technical Event for Day 4 (09 Febuary 2025)",
        ]

        # Check if required columns exist
        missing_cols = [col for col in required_columns + preference_columns if col not in df.columns]
        if missing_cols:
            st.error(f"Missing columns: {missing_cols}")
        else:
            # Filter only required columns
            df_filtered = df[required_columns + preference_columns]

            # Extract unique event names dynamically (ignoring NaN values)
            unique_events = set()
            for col in preference_columns:
                unique_events.update(df_filtered[col].dropna().astype(str).unique())

            # Dropdown for event selection
            selected_event = st.selectbox("Select the Event", options=sorted(unique_events))
            

            if st.button("Fetch"):
                # Filter participants for the selected event
                df_filtered = df_filtered[df_filtered[preference_columns].apply(
                    lambda row: selected_event in row.values.astype(str), axis=1
                )]

                # Display the filtered results
                st.subheader(f"Count : {len(df_filtered[required_columns])}")
                st.dataframe(df_filtered[required_columns])  # Show only Name, Email, Mobile

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.write("Please upload a CSV or Excel file.")

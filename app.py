import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="AutoLookup Pro", layout="centered")

# --- CSS Styling ---
st.markdown(
    """
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {background-color: #4CAF50; color:white;}
    .stDownloadButton>button {background-color: #007BFF; color:white;}
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        text-align: center;
        color: #333;
        padding: 5px;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔍 AutoLookup Pro ")

file1 = st.file_uploader("📄 Upload First Excel (Base file)", type=["xlsx"])
file2 = st.file_uploader("📄 Upload Second Excel (Lookup file)", type=["xlsx"])

if file1 and file2:
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    col1 = st.selectbox("Match Column from First Excel", df1.columns, key="match1")
    col2 = st.selectbox("Match Column from Second Excel", df2.columns, key="match2")

    fetch_col = st.selectbox(
        "Value Column to Fetch from Second Excel (optional)",
        ["(None)"] + list(df2.columns), key="fetch"
    )

    # Step 1: Compare Unique Values
    if st.button("🔍 Compare Unique Values"):
        unique1 = sorted(df1[col1].dropna().unique())
        unique2 = sorted(df2[col2].dropna().unique())

        st.write("### Unique Values Mapping")
        mapping = {}
        for val in unique1:
            selected_match = st.selectbox(
                f"Map '{val}' to:",
                options=["(No Match)"] + unique2,
                key=f"map_{val}"
            )
            mapping[val] = None if selected_match == "(No Match)" else selected_match

        # Store mapping in session state
        st.session_state["value_mapping"] = mapping
        st.success("✅ Mapping table created. Now click '🚀 Apply Mapping & Run Lookup' to proceed.")

    # Step 2: Apply Mapping & Run Lookup
    if st.button("🚀 Apply Mapping & Run Lookup"):
        result_df = df1.copy()

        mapping = st.session_state.get("value_mapping", {})
        if mapping:
            # Apply mapping to column before lookup
            result_df[col1] = result_df[col1].apply(lambda x: mapping.get(x, x))

        if fetch_col != "(None)":
            lookup_dict = df2.set_index(col2)[fetch_col].to_dict()
            result_df["Result"] = result_df[col1].apply(
                lambda x: lookup_dict.get(x, "Not Available")
            )
        else:
            lookup_set = set(df2[col2])
            result_df["Result"] = result_df[col1].apply(
                lambda x: x if x in lookup_set else "Not Available"
            )

        st.dataframe(result_df)

        # Download Excel
        def to_excel(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            return output.getvalue()

        excel_data = to_excel(result_df)

        st.download_button(
            label="📥 Download Result Excel",
            data=excel_data,
            file_name="lookup_result.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.info("👆 Please upload both Excel files to begin.")

# ✅ Footer
st.markdown(
    """
    <div class='footer'>
        💻 Developed by <b>ER. Ruchi Tiwari</b>
    </div>
    """,
    unsafe_allow_html=True,
)

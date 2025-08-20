import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="AutoLookup Pro+", layout="wide")

# ----------------- CSS -----------------
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

st.title("🔍 AutoLookup Pro+ with Compare & Replace")

# ----------------- File Upload -----------------
file1 = st.file_uploader("📄 Upload First Excel (Base file)", type=["xlsx", "csv"])
file2 = st.file_uploader("📄 Upload Second Excel (Lookup file)", type=["xlsx", "csv"])

if file1 and file2:
    # Read function (csv/xlsx)
    def read_file(file):
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file, engine="openpyxl")
        df.columns = [str(c).upper() for c in df.columns]
        df = df.applymap(lambda x: str(x).upper() if isinstance(x, str) else x)
        return df

    df1 = read_file(file1)
    df2 = read_file(file2)

    tab1, tab2 = st.tabs(["🚀 Auto Lookup", "🛠 Compare & Replace"])

    # ----------------- TAB 1: AUTO LOOKUP -----------------
    with tab1:
        col1 = st.selectbox("Match Column from First Excel", df1.columns, key="match1")
        col2 = st.selectbox("Match Column from Second Excel", df2.columns, key="match2")

        fetch_col = st.selectbox(
            "Value Column to Fetch from Second Excel (optional)",
            ["(None)"] + list(df2.columns), key="fetch"
        )

        if st.button("🚀 Run Lookup"):
            result_df = df1.copy()

            if fetch_col != "(None)":
                # VLOOKUP mode
                lookup_dict = df2.set_index(col2)[fetch_col].to_dict()
                result_df["Result"] = result_df[col1].apply(
                    lambda x: lookup_dict.get(x, "Not Available")
                )
            else:
                # Just match check
                lookup_set = set(df2[col2])
                result_df["Result"] = result_df[col1].apply(
                    lambda x: x if x in lookup_set else "Not Available"
                )

            st.dataframe(result_df)

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

    # ----------------- TAB 2: COMPARE & REPLACE -----------------
    with tab2:
        st.subheader("🔎 Compare Columns & Fix Mismatches")

        col1_cr = st.selectbox("Select Column from File 1", df1.columns, key="cr1")
        col2_cr = st.selectbox("Select Column from File 2", df2.columns, key="cr2")

        if st.button("Show Mismatched Values"):
            col1_data = df1[col1_cr].dropna().unique()
            col2_data = df2[col2_cr].dropna().unique()

            mismatched1 = sorted(set(col1_data) - set(col2_data))
            mismatched2 = sorted(set(col2_data) - set(col1_data))

            st.write("### ❌ Values in File1 not in File2")
            st.dataframe(pd.DataFrame(mismatched1, columns=[col1_cr]))

            st.write("### ❌ Values in File2 not in File1")
            st.dataframe(pd.DataFrame(mismatched2, columns=[col2_cr]))

            st.session_state["mismatched1"] = mismatched1
            st.session_state["mismatched2"] = mismatched2
            st.session_state["df2_clone"] = df2.copy()
            st.session_state["task_list"] = []

        if "mismatched1" in st.session_state and "mismatched2" in st.session_state:
            st.write("### 📝 Create Task List (Mapping Values)")
            c1, c2 = st.columns(2)
            with c1:
                val1 = st.selectbox("Pick from File1 mismatched", [""] + st.session_state["mismatched1"], key="val1")
            with c2:
                val2 = st.selectbox("Pick from File2 mismatched", [""] + st.session_state["mismatched2"], key="val2")

            if st.button("➕ Add to Task List"):
                if val1 and val2:
                    st.session_state["task_list"].append((val1, val2))

            if st.session_state["task_list"]:
                st.write("### 📋 Task List")
                task_df = pd.DataFrame(st.session_state["task_list"], columns=["File1 Value", "File2 Value"])
                st.dataframe(task_df)

                if st.button("⚡ Execute Replacements"):
                    df2_clone = st.session_state["df2_clone"]
                    for v1, v2 in st.session_state["task_list"]:
                        df2_clone[col2_cr] = df2_clone[col2_cr].replace(v2, v1)
                    st.session_state["df2_clone"] = df2_clone
                    st.success("✅ Replacements done in File2 Clone!")

                if st.button("📥 Download Updated File2 Clone"):
                    def to_excel(df):
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            df.to_excel(writer, index=False)
                        return output.getvalue()

                    excel_data = to_excel(st.session_state["df2_clone"])
                    st.download_button(
                        label="📥 Download File2 Clone",
                        data=excel_data,
                        file_name="file2_clone.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

else:
    st.info("👆 Please upload both Excel/CSV files to begin.")

# ✅ Footer
st.markdown(
    """
    <div class='footer'>
        💻 Developed by <b>ER. Ruchi Tiwari</b>
    </div>
    """,
    unsafe_allow_html=True,
)

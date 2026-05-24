import io
import re
from datetime import datetime

import pandas as pd
import requests
import streamlit as st
from rapidfuzz import fuzz


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Open-End Fuzzy Matcher",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM FRONTEND CSS
# =========================================================
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg-main: #f3f6fb;
    --bg-card: #ffffff;
    --bg-soft: #f8fafc;
    --text-main: #172033;
    --text-muted: #64748b;
    --border: #dbe3ef;
    --primary: #174ea6;
    --primary-dark: #0f3b82;
    --navy: #0b1f3a;
    --success-bg: #ecfdf5;
    --success-text: #047857;
    --info-bg: #eff6ff;
    --info-text: #1d4ed8;
    --warning-bg: #fffbeb;
    --warning-text: #92400e;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--bg-main);
    color: var(--text-main);
}

.block-container {
    max-width: 1260px;
    padding-top: 1.5rem;
    padding-bottom: 3.5rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0b1f3a;
    border-right: 1px solid #16345f;
}

[data-testid="stSidebar"] * {
    color: #e5edf7;
}

[data-testid="stSidebar"] code {
    background: #ffffff !important;
    color: #0f172a !important;
}

/* Top official header */
.main-hero {
    background: #ffffff;
    border: 1px solid var(--border);
    border-left: 6px solid var(--primary);
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 24px;
    color: var(--text-main);
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.07);
}

.hero-kicker {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #eef4ff;
    color: var(--primary);
    border: 1px solid #c7d8f8;
    border-radius: 999px;
    padding: 7px 13px;
    font-size: 12px;
    font-weight: 800;
    margin-bottom: 14px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

.hero-title {
    font-size: 38px;
    line-height: 1.15;
    letter-spacing: -1px;
    font-weight: 800;
    margin-bottom: 10px;
    color: var(--navy);
}

.hero-title span {
    color: var(--primary);
}

.hero-subtitle {
    font-size: 15px;
    line-height: 1.7;
    color: var(--text-muted);
    max-width: 850px;
}

/* Cards */
.section-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 22px;
    margin-bottom: 18px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
}

.section-title {
    font-size: 19px;
    font-weight: 800;
    color: var(--navy);
    margin-bottom: 5px;
}

.section-subtitle {
    color: var(--text-muted);
    font-size: 14px;
    margin-bottom: 10px;
}

.step-badge {
    display: inline-block;
    background: #eef4ff;
    color: var(--primary);
    border: 1px solid #c7d8f8;
    padding: 6px 11px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
}

/* Info messages */
.info-strip {
    background: var(--info-bg);
    border: 1px solid #bfdbfe;
    color: var(--info-text);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 18px;
    font-size: 14px;
}

.warning-strip {
    background: var(--warning-bg);
    border: 1px solid #fde68a;
    color: var(--warning-text);
    border-radius: 12px;
    padding: 14px 16px;
    margin-top: 14px;
    font-size: 14px;
}

.success-strip {
    background: var(--success-bg);
    border: 1px solid #bbf7d0;
    color: var(--success-text);
    border-radius: 12px;
    padding: 14px 16px;
    margin-top: 14px;
    font-size: 14px;
}

/* Upload box */
[data-testid="stFileUploader"] {
    background: #ffffff;
    border: 1.5px dashed #b8c7dc;
    border-radius: 16px;
    padding: 18px;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--primary);
}

/* Metrics */
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid var(--border);
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
}

div[data-testid="stMetricLabel"] {
    color: var(--text-muted);
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: var(--navy);
    font-weight: 800;
}

/* Buttons */
.stButton > button {
    width: 100%;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.85rem 1rem;
    font-size: 15px;
    font-weight: 800;
    box-shadow: 0 8px 18px rgba(23, 78, 166, 0.18);
    transition: all 0.15s ease;
}

.stButton > button:hover {
    background: var(--primary-dark);
    color: white;
    border: none;
    transform: translateY(-1px);
}

.stDownloadButton > button {
    width: 100%;
    background: var(--navy);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.85rem 1rem;
    font-size: 15px;
    font-weight: 800;
    box-shadow: 0 8px 18px rgba(15, 23, 42, 0.18);
}

.stDownloadButton > button:hover {
    background: #132f55;
    color: white;
    border: none;
}

/* Inputs */
div[data-baseweb="select"] > div {
    border-radius: 12px;
    border-color: #cbd5e1;
    background: #ffffff;
}

.stSlider {
    padding-top: 4px;
}

/* Tables */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
}

/* Footer */
.footer-note {
    text-align: center;
    color: #475569;
    font-size: 13px;
    margin-top: 34px;
    padding: 14px 18px;
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 14px;
}

hr {
    border-color: var(--border);
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =========================================================
# HELPER FUNCTIONS
# =========================================================
def normalize_text(value):
    """
    Cleans text before comparison.
    """
    if pd.isna(value):
        return ""

    value = str(value).lower().strip()
    value = re.sub(r"[^\w\s/.-]", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def is_placeholder(text):
    """
    Skips placeholder values that should not be considered real responses.
    """
    normalized = normalize_text(text)

    placeholders = {
        "",
        "oe not pasted",
        "o e not pasted",
        "ss missing",
        "screenshot missing",
        "oe missing",
        "not pasted",
        "na",
        "n a",
        "n/a",
        "none",
        "no response",
        "no answer",
        "not answered",
        "blank",
        "-",
        "--",
        ".",
        "nil",
        "null",
        "ns",
        "n s",
        "not sure",
        "no screenshot",
    }

    return normalized in placeholders


def clean_display_value(value):
    """
    Keeps display clean in table/export.
    """
    if pd.isna(value):
        return ""
    return str(value).strip()


def flatten_open_ends(df):
    """
    Expected Excel structure:
    Column 1 = S.No.
    Column 2 = Date
    Column 3 = Link ID
    Column 4 onward = Open-ended answers
    """
    responses = []

    if df.shape[1] < 4:
        raise ValueError(
            "Expected at least 4 columns: S.No., Date, Link ID, and open-ended question columns."
        )

    headers = list(df.columns)

    date_col = headers[1]
    link_id_col = headers[2]
    question_cols = headers[3:]

    skipped_placeholders = 0
    skipped_empty = 0

    for row_index, row in df.iterrows():
        link_id = clean_display_value(row.get(link_id_col, ""))

        if not link_id or link_id.lower() == "nan":
            link_id = f"Row {row_index + 2}"

        date_value = clean_display_value(row.get(date_col, ""))

        for question in question_cols:
            response = clean_display_value(row.get(question, ""))

            if response == "":
                skipped_empty += 1
                continue

            if is_placeholder(response):
                skipped_placeholders += 1
                continue

            responses.append(
                {
                    "link_id": link_id,
                    "date": date_value,
                    "question": str(question),
                    "response": response,
                    "row_number": row_index + 2,
                }
            )

    return responses, skipped_placeholders, skipped_empty


def find_fuzzy_matches(responses, threshold):
    """
    Compares every response with every other response.
    """
    flagged = []
    exact_count = 0
    total = len(responses)

    normalized_responses = [normalize_text(item["response"]) for item in responses]

    for i in range(total):
        for j in range(i + 1, total):
            first = responses[i]
            second = responses[j]

            # Skip exact same person + same question field.
            if (
                first["link_id"] == second["link_id"]
                and first["question"] == second["question"]
            ):
                continue

            score = round(fuzz.token_set_ratio(first["response"], second["response"]))

            if score >= threshold:
                if score == 100 or normalized_responses[i] == normalized_responses[j]:
                    exact_count += 1

                flagged.append(
                    {
                        "score": score,
                        "link_id_a": first["link_id"],
                        "link_id_b": second["link_id"],
                        "same_link_id": "YES"
                        if first["link_id"] == second["link_id"]
                        else "",
                        "question_a": first["question"],
                        "response_a": first["response"],
                        "question_b": second["question"],
                        "response_b": second["response"],
                        "date_a": first["date"],
                        "date_b": second["date"],
                        "same_question": "YES"
                        if first["question"] == second["question"]
                        else "",
                        "row_a": first["row_number"],
                        "row_b": second["row_number"],
                    }
                )

    flagged = sorted(flagged, key=lambda x: x["score"], reverse=True)
    return flagged, exact_count


def make_display_dataframe(flagged):
    """
    Creates a clean dataframe for Streamlit display.
    """
    if not flagged:
        return pd.DataFrame()

    df = pd.DataFrame(flagged)

    display_df = df[
        [
            "score",
            "link_id_a",
            "link_id_b",
            "same_link_id",
            "question_a",
            "response_a",
            "question_b",
            "response_b",
            "same_question",
            "row_a",
            "row_b",
        ]
    ].copy()

    display_df.columns = [
        "Score (%)",
        "Link ID A",
        "Link ID B",
        "Same Link ID?",
        "Question A",
        "Response A",
        "Question B",
        "Response B",
        "Same Question?",
        "Row A",
        "Row B",
    ]

    return display_df


def create_excel_report(
    flagged,
    responses,
    selected_sheet,
    threshold,
    exact_count,
    skipped_placeholders,
    skipped_empty,
):
    """
    Creates downloadable Excel report.
    """
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        workbook = writer.book

        header_format = workbook.add_format(
            {
                "bold": True,
                "bg_color": "#1D4ED8",
                "font_color": "#FFFFFF",
                "border": 1,
                "align": "center",
                "valign": "vcenter",
            }
        )

        normal_format = workbook.add_format(
            {
                "text_wrap": True,
                "valign": "top",
            }
        )

        high_format = workbook.add_format(
            {
                "bg_color": "#FEE2E2",
                "font_color": "#991B1B",
                "bold": True,
                "align": "center",
            }
        )

        mid_format = workbook.add_format(
            {
                "bg_color": "#FEF3C7",
                "font_color": "#92400E",
                "bold": True,
                "align": "center",
            }
        )

        low_format = workbook.add_format(
            {
                "bg_color": "#DCFCE7",
                "font_color": "#166534",
                "bold": True,
                "align": "center",
            }
        )

        # Sheet 1: Flagged Pairs
        flagged_df = make_display_dataframe(flagged)
        flagged_df.to_excel(writer, sheet_name="Flagged Pairs", index=False)

        ws1 = writer.sheets["Flagged Pairs"]
        ws1.freeze_panes(1, 0)

        if not flagged_df.empty:
            ws1.autofilter(0, 0, len(flagged_df), len(flagged_df.columns) - 1)

        columns_widths = {
            "A": 12,
            "B": 18,
            "C": 18,
            "D": 16,
            "E": 22,
            "F": 58,
            "G": 22,
            "H": 58,
            "I": 17,
            "J": 10,
            "K": 10,
        }

        for col, width in columns_widths.items():
            ws1.set_column(f"{col}:{col}", width, normal_format)

        for col_num, col_name in enumerate(flagged_df.columns):
            ws1.write(0, col_num, col_name, header_format)

        if not flagged_df.empty:
            ws1.conditional_format(
                1,
                0,
                len(flagged_df),
                0,
                {
                    "type": "cell",
                    "criteria": ">=",
                    "value": 95,
                    "format": high_format,
                },
            )
            ws1.conditional_format(
                1,
                0,
                len(flagged_df),
                0,
                {
                    "type": "cell",
                    "criteria": "between",
                    "minimum": 85,
                    "maximum": 94,
                    "format": mid_format,
                },
            )
            ws1.conditional_format(
                1,
                0,
                len(flagged_df),
                0,
                {
                    "type": "cell",
                    "criteria": "<",
                    "value": 85,
                    "format": low_format,
                },
            )

        # Sheet 2: All Responses
        all_responses_df = pd.DataFrame(responses)

        if not all_responses_df.empty:
            all_responses_df = all_responses_df[
                ["link_id", "date", "question", "response", "row_number"]
            ]

            all_responses_df.columns = [
                "Link ID",
                "Date",
                "Question",
                "Response",
                "Original Row",
            ]

        all_responses_df.to_excel(writer, sheet_name="All Responses", index=False)

        ws2 = writer.sheets["All Responses"]
        ws2.freeze_panes(1, 0)
        ws2.set_column("A:A", 18)
        ws2.set_column("B:B", 18)
        ws2.set_column("C:C", 24)
        ws2.set_column("D:D", 72, normal_format)
        ws2.set_column("E:E", 14)

        for col_num, col_name in enumerate(all_responses_df.columns):
            ws2.write(0, col_num, col_name, header_format)

        # Sheet 3: Summary
        unique_link_ids = set()

        for item in flagged:
            unique_link_ids.add(item["link_id_a"])
            unique_link_ids.add(item["link_id_b"])

        summary_data = [
            ["Open-End Fuzzy Match Report", ""],
            ["Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["Project Sheet", selected_sheet],
            ["Threshold", f"{threshold}%"],
            ["", ""],
            ["Total Responses Analyzed", len(responses)],
            ["Pairs Flagged", len(flagged)],
            ["Exact / 100% Duplicates", exact_count],
            ["Unique Link IDs Flagged", len(unique_link_ids)],
            ["Placeholder Cells Skipped", skipped_placeholders],
            ["Empty Cells Skipped", skipped_empty],
            ["", ""],
            ["Score Guide", ""],
            ["95-100%", "Very strong duplicate / exact or almost exact"],
            ["85-94%", "Likely duplicate or strong paraphrase"],
            ["Below 85%", "Possible match depending on threshold"],
            ["", ""],
            ["Privacy Note", "Your Excel file is used only for fuzzy matching and is not stored by this app."],
        ]

        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name="Summary", index=False, header=False)

        ws3 = writer.sheets["Summary"]
        ws3.set_column("A:A", 34)
        ws3.set_column("B:B", 70)
        ws3.write("A1", "Open-End Fuzzy Match Report", header_format)

    output.seek(0)
    return output


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## Open-End Review")
    st.markdown(
        """
        Internal tool for checking duplicate or highly similar open-ended responses.
        """
    )

    st.divider()

    st.markdown("### Expected Excel Format")
    st.code(
        """Column 1 = S.No.
Column 2 = Date
Column 3 = Link ID
Column 4+ = Open-ended answers""",
        language="text",
    )

    st.divider()

    st.markdown("### Score Meaning")
    st.markdown(
        """
        **95–100%** → Very strong duplicate  
        **85–94%** → Likely duplicate  
        **80–84%** → Possible near duplicate  
        """
    )

    st.divider()

    st.markdown("### Skipped Values")
    st.markdown(
        """
        The app skips values like:
        `NA`, `N/A`, `NS`, `none`, `no response`, `oe not pasted`, `ss missing`
        """
    )


# =========================================================
# HERO
# =========================================================
st.markdown(
    """
<div class="main-hero">
    <div class="hero-kicker">Internal Quality Review Tool</div>
    <div class="hero-title">Open-End <span>Fuzzy Matcher</span></div>
    <div class="hero-subtitle">
        A local office utility for reviewing duplicate and near-duplicate open-ended survey responses.
        Upload an Excel workbook, select the project sheet, run fuzzy matching, and download a structured review report.
        <br><br>
        🔒 <b>Privacy note:</b> Your Excel file is used only for fuzzy matching and is not stored by this app.
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# MAIN UI
# =========================================================
st.markdown(
    """
<div class="section-card">
    <span class="step-badge">STEP 01</span>
    <div class="section-title">Upload Excel file</div>
    <div class="section-subtitle">
        Upload your workbook. The file is processed in memory for this review only.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

input_method = st.radio(
    "Choose Excel source",
    ["Upload file", "Use online link"],
    horizontal=True,
)

uploaded_file = None
excel_source = None

if input_method == "Upload file":
    uploaded_file = st.file_uploader(
        "Upload Excel",
        type=["xlsx", "xls"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        excel_source = uploaded_file

else:
    excel_url = st.text_input(
        "Paste Excel file link",
        placeholder="https://example.com/file.xlsx",
    )

    if excel_url:
        try:
            with st.spinner("Fetching Excel file from link..."):
                response = requests.get(excel_url, timeout=30)
                response.raise_for_status()

                excel_bytes = io.BytesIO(response.content)
                excel_source = excel_bytes

            st.success("Excel file loaded from link successfully.")

        except Exception as error:
            st.error(f"Could not load Excel from link: {error}")

if excel_source is None:
    st.markdown(
        """
<div class="info-strip">
    Waiting for your Excel file. Once uploaded, you will be able to select a sheet and run fuzzy matching.
</div>
""",
        unsafe_allow_html=True,
    )

else:
    try:
        excel_file = pd.ExcelFile(excel_source)
        sheet_names = excel_file.sheet_names

        st.markdown(
            f"""
<div class="success-strip">
    File loaded successfully. Found <b>{len(sheet_names)}</b> sheet(s).
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(
                """
<div class="section-card">
    <span class="step-badge">STEP 02</span>
    <div class="section-title">Choose project sheet</div>
    <div class="section-subtitle">
        Select the sheet/tab you want to analyze. No sheet is selected automatically.
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

            sheet_placeholder = "-- Select project sheet --"
            sheet_options = [sheet_placeholder] + sheet_names

            selected_sheet = st.selectbox(
                "Project sheet",
                sheet_options,
                index=0,
                label_visibility="collapsed",
            )

        with col2:
            st.markdown(
                """
<div class="section-card">
    <span class="step-badge">STEP 03</span>
    <div class="section-title">Set threshold</div>
    <div class="section-subtitle">
        Higher value means stricter matching.
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

            threshold = st.slider(
                "Similarity threshold",
                min_value=50,
                max_value=100,
                value=80,
                step=1,
            )

        st.markdown(
            """
<div class="info-strip">
    <b>Tip:</b> Start with 80%. Use 90% if you only want very close duplicates.
</div>
""",
            unsafe_allow_html=True,
        )

        run_clicked = st.button("Run Fuzzy Match Review")

        if run_clicked:
            if selected_sheet == sheet_placeholder:
                st.error("Please select a project sheet first.")
                st.stop()

            # keep_default_na=False prevents Pandas from turning "NA" into blank/NaN.
            df = pd.read_excel(
                excel_source,
                sheet_name=selected_sheet,
                keep_default_na=False,
            )

            responses, skipped_placeholders, skipped_empty = flatten_open_ends(df)

            if len(responses) < 2:
                st.error("Need at least 2 valid non-empty responses to compare.")
            else:
                with st.spinner("Comparing responses. Please wait..."):
                    flagged, exact_count = find_fuzzy_matches(responses, threshold)

                unique_link_ids = set()
                for item in flagged:
                    unique_link_ids.add(item["link_id_a"])
                    unique_link_ids.add(item["link_id_b"])

                st.divider()

                st.markdown("## Results Overview")

                metric1, metric2, metric3, metric4, metric5 = st.columns(5)

                metric1.metric("Responses", len(responses))
                metric2.metric("Pairs Flagged", len(flagged))
                metric3.metric("Link IDs", len(unique_link_ids))
                metric4.metric("Exact Dupes", exact_count)
                metric5.metric("Skipped", skipped_placeholders)

                if skipped_placeholders > 0:
                    st.markdown(
                        f"""
<div class="warning-strip">
    Skipped <b>{skipped_placeholders}</b> placeholder cell(s), including values like NA, NS, N/A, none, no response, etc.
</div>
""",
                        unsafe_allow_html=True,
                    )

                if skipped_empty > 0:
                    st.caption(f"Empty cells skipped: {skipped_empty}")

                if len(flagged) == 0:
                    st.markdown(
                        """
<div class="success-strip">
    No duplicate or near-duplicate responses found at the selected threshold.
</div>
""",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown("## Flagged Matches")

                    display_df = make_display_dataframe(flagged)

                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        height=560,
                        hide_index=True,
                    )

                    report = create_excel_report(
                        flagged=flagged,
                        responses=responses,
                        selected_sheet=selected_sheet,
                        threshold=threshold,
                        exact_count=exact_count,
                        skipped_placeholders=skipped_placeholders,
                        skipped_empty=skipped_empty,
                    )

                    safe_sheet_name = re.sub(r"[^\w\-]+", "_", selected_sheet)[:40]

                    filename = (
                        f"fuzzy_match_{safe_sheet_name}_"
                        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                    )

                    st.download_button(
                        label="Download Excel Report",
                        data=report,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

    except Exception as error:
        st.error(f"Error: {error}")


# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
<div class="footer-note">
    🔒 Privacy note: Your Excel file is used only for fuzzy matching and is not stored by this app.
</div>
""",
    unsafe_allow_html=True,
)
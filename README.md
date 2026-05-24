# Open-End Fuzzy Matcher

Open-End Fuzzy Matcher is an internal office tool used to detect duplicate and near-duplicate open-ended survey responses from Excel files.

The app allows users to upload an Excel workbook, select a project sheet, run fuzzy matching, review flagged responses, and download a structured Excel report.

## Features

- Upload `.xlsx` or `.xls` Excel files
- Select project sheet manually
- Compare open-ended responses using fuzzy matching
- Skip placeholder values like `NA`, `N/A`, `NS`, `none`, `no response`, `oe not pasted`, and `ss missing`
- View flagged duplicate or near-duplicate responses
- Download Excel report
- Privacy-focused internal tool

## Expected Excel Format

The Excel sheet should follow this structure:

| Column | Purpose |
|---|---|
| Column 1 | S.No. |
| Column 2 | Date |
| Column 3 | Link ID |
| Column 4 onward | Open-ended answers |

Example:

| S.No. | Date | Link ID | Q1 | Q2 |
|---|---|---|---|---|
| 1 | 2026-05-22 | R001 | Good service | Nice quality |
| 2 | 2026-05-22 | R002 | Service was good | Quality is nice |

## Technologies Used

- Python
- Streamlit
- Pandas
- OpenPyXL
- RapidFuzz
- XlsxWriter
- Requests

## Installation

Clone the repository or download the project files.

Install dependencies:

```bash
pip install -r requirements.txt

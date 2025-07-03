import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

# Google Sheets setup
def get_worksheet(tab_name):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    service_account_info = {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"],
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"],
        "universe_domain": st.secrets["universe_domain"]
    }
    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
    client = gspread.authorize(creds)
    SPREADSHEET_NAME = '1fN2MkfDK2F_mnYv-7S_YjEHaPlMBdGVL_X_EtNHSItg'
    sheet = client.open_by_key(SPREADSHEET_NAME)
    return sheet.worksheet(tab_name)

# Date and range mapping for each tab
date_range_map = [
    ("7/11(금)", "G11:G41"),
    ("7/12(토)", "H11:H41"),
    ("7/13(일)", "B49:B79"),
    ("7/15(화)", "D49:D79"),
    ("7/16(수)", "E49:E79"),
    ("7/17(목)", "F49:F79"),
    ("7/18(금)", "G49:G79"),
    ("7/19(토)", "H49:H79"),
    ("7/20(일)", "B87:B117"),
    ("7/21(월)", "C87:C117"),
    ("7/22(화)", "D87:D117"),
]

# Helper to find dates for a worksheet and mapping
def find_dates(worksheet, name, date_ranges):
    found = []
    for date_label, cell_range in date_ranges:
        cell_list = worksheet.range(cell_range)
        for cell in cell_list:
            if cell.value and re.search(re.escape(name), cell.value, re.IGNORECASE):
                found.append(date_label)
                break
    return found

st.title("2025 서울국제무용콩쿠르 서포터즈")
st.subheader("본선 기간 중 활동 일자 조회")

name = st.text_input("이름을 입력한 후 엔터를 눌러 주세요:")

if name:
    try:
        a_ws = get_worksheet("본선 기간(운영팀-A조)")
        b_ws = get_worksheet("본선 기간(운영팀-B조)")
        a_dates = find_dates(a_ws, name, date_range_map)
        b_dates = find_dates(b_ws, name, date_range_map)

        # Split A조 dates into normal and 7/18~20
        special_dates = {"7/18(금)", "7/19(토)", "7/20(일)"}
        a_normal = [d for d in a_dates if d not in special_dates]
        a_special = [d for d in a_dates if d in special_dates]

        # B조 includes all dates
        # Special section only from A조

        st.subheader("A조 출근일자")
        st.write(", ".join(a_normal) if a_normal else "없음")

        st.subheader("B조 출근일자")
        st.write(", ".join(b_dates) if b_dates else "없음")

        st.subheader("7/18 ~ 7/20 출근일자")
        st.write(", ".join(a_special) if a_special else "없음")
    except Exception as e:
        st.error(f"스프레드시트 접근 중 오류 발생: {e}")
else:
    st.info("결과가 나오기 까지 15초 정도 걸릴 수 있습니다.")

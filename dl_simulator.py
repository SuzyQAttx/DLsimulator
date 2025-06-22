# dl_simulator.py
import streamlit as st
import datetime

# --------------------
# Custom Styling for PMDPay Theme
# --------------------
st.markdown("""
    <style>
    body {
        background-color: #F7F7F7;
    }
    .stApp {
        font-family: 'Segoe UI', sans-serif;
        color: #1E1E1E;
    }
    .css-1d391kg {  /* Header */
        color: #02AAB0 !important;
    }
    .st-bb, .st-c3, .st-bx {
        background-color: #00CDAC !important;
        color: white !important;
    }
    .stButton>button {
        background-color: #02AAB0;
        color: white;
        font-weight: bold;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------
# Soundex implementation
# --------------------
def soundex(name):
    name = name.upper()
    mappings = {'BFPV': '1', 'CGJKQSXZ': '2', 'DT': '3', 'L': '4', 'MN': '5', 'R': '6'}
    result = name[0]
    last_code = ''
    for char in name[1:]:
        for key in mappings:
            if char in key:
                code = mappings[key]
                if code != last_code:
                    result += code
                    last_code = code
                break
        else:
            last_code = ''
    return result[:4].ljust(4, '0')

# --------------------
# State-specific DL generators
# --------------------
def florida_dl(last_name, birthdate, gender='M', sequence=0):
    sdx = soundex(last_name)[1:]  # Remove initial letter
    initial = last_name[0].upper()
    year = birthdate.year % 100
    daycode = (birthdate.month - 1) * 40 + birthdate.day
    if gender.upper() == 'F':
        daycode += 500
    return f"{initial}{sdx}{year:02d}{daycode:03d}{sequence:01d}"

def georgia_dl(ssn):
    return ssn.replace('-', '')

def illinois_dl(last_name, birthdate, gender='M'):
    sdx = soundex(last_name)  # 4 characters
    year = birthdate.year % 100
    month = birthdate.month + 50 if gender.upper() == 'F' else birthdate.month
    day = birthdate.day
    return f"{sdx}{year:02d}{month:02d}{day:02d}"

def wisconsin_dl(last_name, birthdate):
    sdx = soundex(last_name)[:4]
    year = birthdate.year % 100
    month = birthdate.month
    day = birthdate.day
    return f"{sdx}{year:02d}{month:02d}{day:02d}"

def washington_dl(last_name, birthdate):
    sdx = soundex(last_name)[:4]
    year = birthdate.year % 100
    return f"{last_name[0].upper()}{sdx[1:]}{year:02d}X"  # 'X' as a mock check digit

def placeholder_dl():
    return "DL format not implemented yet."

# --------------------
# DL Generator Dispatcher
# --------------------
def generate_dl(state, last_name, birthdate, gender, ssn):
    if state == "Florida":
        return florida_dl(last_name, birthdate, gender)
    elif state == "Georgia":
        return georgia_dl(ssn)
    elif state == "Illinois":
        return illinois_dl(last_name, birthdate, gender)
    elif state == "Wisconsin":
        return wisconsin_dl(last_name, birthdate)
    elif state == "Washington":
        return washington_dl(last_name, birthdate)
    else:
        return placeholder_dl()

# --------------------
# Streamlit App UI
# --------------------
st.title("\U0001F4C4 U.S. Driver’s License Simulator")

states = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
    'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
    'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
    'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
    'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
    'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
    'Wisconsin', 'Wyoming'
]

selected_state = st.selectbox("Select State", states)

first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
birthdate = st.date_input("Birthdate", datetime.date(1990, 1, 1))
gender = st.radio("Gender", ['M', 'F'])
ssn = st.text_input("SSN", placeholder="123-45-6789")

if st.button("Generate DL Number"):
    dl_number = generate_dl(selected_state, last_name, birthdate, gender, ssn)
    st.success(f"{selected_state} DL Number: {dl_number}")


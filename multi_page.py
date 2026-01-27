import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_cookies_manager import EncryptedCookieManager

st.set_page_config(
    layout="wide"
)

cookies = EncryptedCookieManager(
    prefix="francojay_",
    password="12345"
)

if not cookies.ready():
    st.stop()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = cookies.get("logged_in") == "true"


# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=86400)
def load_users():
     return conn.read(worksheet="users")

df = load_users()
users = df.to_dict(orient="records")

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

def login():
    st.title("Franco Jay Global")
    st.subheader("Log in to continue")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log in"):
        for user in users:
            if username == user["Username"] and password == user["Password"]:
                st.session_state.logged_in = True

                # ✅ Persist login
                cookies["logged_in"] = "true"
                cookies.save()

                st.rerun()
                break
        else:
            st.error("Invalid username or password")
     

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False

        cookies["logged_in"] = "false"
        cookies.save()

        st.rerun()



login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

dashboard = st.Page("reports/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True)
staffs = st.Page("reports/staffs.py", title="Staff reports", icon=":material/add_moderator:")


cards = st.Page("tools/cards.py", title="Cards", icon=":material/card_giftcard:")
loans = st.Page("tools/loan.py", title="Loans", icon=":material/sell:")
moniebooks = st.Page("tools/moniebook.py", title="Moniebooks", icon=":material/computer:")
admin = st.Page("tools/admin.py", title="Admin", icon=":material/admin_panel_settings:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Reports": [dashboard, staffs],
            "Tools": [cards, loans, moniebooks, admin],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()
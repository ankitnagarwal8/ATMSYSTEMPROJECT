import streamlit as st
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit_option_menu import option_menu

# Define custom styling for the dashboard
st.markdown(
    """
    <style>
    .stSidebar {
        background-color: #004d40;
        color: #ffffff;
        padding: 20px;
    }
    .stApp {
        background-color: #e0f2f1;
        font-family: Arial, sans-serif;
    }
    .header-title {
        color: #00251a;
        font-size: 34px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .content-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
        margin: 10px 0;
        color: #1b5e20;
    }
    .button {
        background-color: #bf360c;
        color: #ffffff;
        font-weight: bold;
    }
    .subheader {
        color: #004d40;
        font-weight: bold;
    }
    .info-text {
        color: #003300;
    }
    </style>
    """,
    unsafe_allow_html=True
)

class Atm:
    def __init__(self, email="ankitnagarwal0005@gmail.com"):
        self.pin = ""
        self.balance = 0
        self.email = email
        self.verification_code = None

    def pin_generator(self, new_pin, new_balance):
        self.pin = new_pin
        self.balance = new_balance
        if self.send_email_notification("PIN and balance set", self.email):
            st.success("Email notification sent.")
        else:
            st.error("Failed to send email.")
        return "PIN generated successfully."

    def send_email_verification(self, to_email, verification_code):
        try:
            sender_email = "ishika0870@gmail.com"
            password = "iflz geig vuyd pwfe"

            subject = "ATM PIN Change Verification Code"
            body = f"Your verification code is: {verification_code}"

            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, to_email, msg.as_string())
            return True
        except Exception as e:
            st.error(f"Error sending verification email: {e}")
            return False

    def pin_changer(self, old_pin, new_pin):
        if old_pin == self.pin:
            self.verification_code = random.randint(100000, 999999)
            st.session_state.verification_code = self.verification_code
            if self.send_email_verification(self.email, self.verification_code):
                st.success("Verification code sent to your email.")
                st.session_state.new_pin = new_pin
            else:
                st.error("Failed to send email.")
        else:
            st.error("Incorrect PIN. Please try again.")

    def verify_and_change_pin(self, verification_code_input):
        if st.session_state.verification_code and verification_code_input == str(st.session_state.verification_code):
            if st.session_state.new_pin:
                self.pin = st.session_state.new_pin
                st.success("PIN changed successfully.")
                st.session_state.verification_code = None
                st.session_state.new_pin = None
            else:
                st.error("New PIN cannot be empty.")
        else:
            st.error("Incorrect verification code.")

    def balance_enquiry(self):
        return f"Your balance is {self.balance}."

    def for_withdrawal_email(self, withdraw_amount, to_email, current_balance):
        sender_email = "ishika0870@gmail.com"
        password = "iflz geig vuyd pwfe"

        subject = "ATM Withdrawal Notification"
        body = f"Dear customer, the amount of {withdraw_amount} was successfully withdrawn from your account. Your current balance is {current_balance}."

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, to_email, msg.as_string())
        return True

    def withdraw(self, old_pin, withdraw_amount):
        if old_pin == self.pin:
            if self.balance >= withdraw_amount:
                self.balance -= withdraw_amount
                if self.for_withdrawal_email(withdraw_amount, self.email, self.balance):
                    return f"Withdrawal successful. Your new balance is {self.balance}."
                else:
                    st.error("Failed to send email.")
            else:
                return "Insufficient balance."
        else:
            return "Incorrect PIN."

    def send_email_notification(self, action, to_email):
        try:
            sender_email = "ishika0870@gmail.com"
            password = "iflz geig vuyd pwfe"

            subject = f"ATM Notification: {action}"
            body = f"Dear customer, your account has been updated: {action}.\n\nRegards,\nATM Team"

            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, to_email, msg.as_string())
            return True
        except Exception as e:
            st.error(f"Error sending email notification: {e}")
            return False

# Streamlit UI
def main():
    st.markdown('<h1 class="header-title">ATM System Dashboard</h1>', unsafe_allow_html=True)

    if 'atm' not in st.session_state:
        st.session_state.atm = Atm()

    menu_options = ["Generate PIN", "Change PIN", "Balance Inquiry", "Withdraw", "Exit"]
    icons = ["key", "unlock-alt", "dollar-sign", "money-bill-wave", "sign-out-alt"]
    
    # Sidebar with icons
    choice = option_menu(
        "Menu", menu_options, icons=icons, menu_icon="navicon", default_index=0,
        styles={
            "container": {"background-color": "#004d40"},
            "icon": {"color": "#ffffff", "font-size": "20px"},
            "nav-link": {"color": "#ffffff", "font-size": "16px"},
        },
    )

    # PIN Generation
    if choice == "Generate PIN":
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.subheader("🔑 Generate PIN")
        new_pin = st.text_input("Enter your new PIN:")
        new_balance = st.number_input("Enter initial balance:", min_value=0)
        if st.button("Generate PIN"):
            result = st.session_state.atm.pin_generator(new_pin, new_balance)
            st.success(result)
        st.markdown('</div>', unsafe_allow_html=True)

    # PIN Change
    elif choice == "Change PIN":
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.subheader("🔄 Change PIN")
        old_pin = st.text_input("Enter old PIN:")
        new_pin = st.text_input("Enter new PIN:")
        if st.button("Submit"):
            st.session_state.atm.pin_changer(old_pin, new_pin)

        verification_code_input = st.text_input("Enter verification code")
        if st.button("Verify"):
            st.session_state.atm.verify_and_change_pin(verification_code_input)
        st.markdown('</div>', unsafe_allow_html=True)

    # Balance Inquiry
    elif choice == "Balance Inquiry":
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.subheader("💰 Balance Inquiry")
        result = st.session_state.atm.balance_enquiry()
        st.info(result)
        st.markdown('</div>', unsafe_allow_html=True)

    # Withdraw
    elif choice == "Withdraw":
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.subheader("💸 Withdraw")
        old_pin = st.text_input("Enter PIN:")
        withdraw_amount = st.number_input("Enter amount:", min_value=1)
        if st.button("Withdraw"):
            result = st.session_state.atm.withdraw(old_pin, withdraw_amount)
            st.success(result)
        st.markdown('</div>', unsafe_allow_html=True)

    elif choice == "Exit":
        st.success("Exiting...")

if __name__ == "__main__":
    main()

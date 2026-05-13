from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
import random
import re

KV = '''
MDScreenManager:
    LoginScreen:
    EMIScreen:

<LoginScreen>:
    name: "login"
    md_bg_color: 0.95, 0.96, 0.98, 1

    MDCard:
        orientation: "vertical"
        size_hint: 0.85, 0.8
        pos_hint: {"center_x": .5, "center_y": .5}
        padding: "20dp"
        spacing: "10dp"
        radius: [20]

        MDLabel:
            text: "EMI Login"
            halign: "center"
            theme_text_color: "Primary"
            bold: True
            font_style: "HeadlineSmall"

        MDBoxLayout:
            adaptive_height: True
            spacing: "10dp"

            MDRaisedButton:
                text: "Phone"
                on_release: root.switch_mode("phone")

            MDRaisedButton:
                text: "Email"
                on_release: root.switch_mode("email")

        MDTextField:
            id: main_input
            hint_text: "Phone Number"
            icon_right: "phone"
            mode: "outlined"

        MDTextField:
            id: password_input
            hint_text: "Password"
            icon_right: "key"
            mode: "outlined"
            password: True
            opacity: 0
            disabled: True

        MDTextField:
            id: otp_input
            hint_text: "Enter OTP"
            mode: "outlined"
            opacity: 0
            disabled: True

        MDRaisedButton:
            id: action_btn
            text: "SEND OTP"
            size_hint_x: 1
            on_release: root.handle_action()

        MDFlatButton:
            text: "Skip Login →"
            pos_hint: {"center_x": .5}
            on_release: app.root.current = "emi"

<EMIScreen>:
    name: "emi"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "EMI Calculator"
            right_action_items: [["logout", lambda x: root.logout()]]

        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "15dp"

            MDTextField:
                id: principal
                hint_text: "Principal Amount (₹)"
                mode: "outlined"

            MDTextField:
                id: rate
                hint_text: "Interest Rate (%)"
                mode: "outlined"

            MDTextField:
                id: tenure
                hint_text: "Tenure (Years)"
                mode: "outlined"

            MDRaisedButton:
                text: "CALCULATE"
                on_release: root.calculate()

            MDCard:
                padding: "15dp"
                radius: [15]

                MDLabel:
                    id: result_label
                    text: "Results will appear here"
                    halign: "center"
'''

class LoginScreen(MDScreen):
    mode = "phone"
    otp_code = ""

    def switch_mode(self, mode):
        self.mode = mode

        if mode == "phone":
            self.ids.main_input.hint_text = "Phone Number"
            self.ids.main_input.icon_right = "phone"

            self.ids.password_input.opacity = 0
            self.ids.password_input.disabled = True

            self.ids.action_btn.text = "SEND OTP"

        else:
            self.ids.main_input.hint_text = "Email Address"
            self.ids.main_input.icon_right = "email"

            self.ids.password_input.opacity = 1
            self.ids.password_input.disabled = False

            self.ids.otp_input.opacity = 0
            self.ids.otp_input.disabled = True

            self.ids.action_btn.text = "LOGIN"

    def handle_action(self):
        val = self.ids.main_input.text.strip()

        if self.mode == "phone":

            if self.ids.action_btn.text == "SEND OTP":

                if val.isdigit() and len(val) == 10:

                    self.otp_code = str(random.randint(1000, 9999))

                    self.show_dialog(
                        "OTP Sent",
                        f"Your OTP is: {self.otp_code}"
                    )

                    self.ids.otp_input.opacity = 1
                    self.ids.otp_input.disabled = False

                    self.ids.action_btn.text = "VERIFY & LOGIN"

                else:
                    self.show_dialog(
                        "Error",
                        "Enter valid 10-digit number"
                    )

            else:

                if self.ids.otp_input.text == self.otp_code:
                    self.manager.current = "emi"
                else:
                    self.show_dialog("Error", "Invalid OTP")

        else:

            password = self.ids.password_input.text

            email_pattern = (
                r'^[a-zA-Z0-9._%+-]+'
                r'@[a-zA-Z0-9.-]+'
                r'\\.[a-zA-Z]{2,}$'
            )

            if not re.match(email_pattern, val):
                self.show_dialog("Format Error", "Invalid Email!")

            elif len(password) < 6:
                self.show_dialog(
                    "Security",
                    "Min 6 characters required"
                )

            elif password == "admin123":
                self.manager.current = "emi"

            else:
                self.show_dialog("Failed", "Wrong Password!")

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text
        )
        dialog.open()

class EMIScreen(MDScreen):

    def calculate(self):
        try:
            P = float(self.ids.principal.text)
            R = float(self.ids.rate.text) / (12 * 100)
            N = float(self.ids.tenure.text) * 12

            emi = (
                P * R * (1 + R) ** N
            ) / (
                ((1 + R) ** N) - 1
            )

            total = emi * N

            self.ids.result_label.text = (
                f"EMI: ₹{round(emi, 2)}\\n"
                f"Total Interest: ₹{round(total-P, 2)}\\n"
                f"Total Amount: ₹{round(total, 2)}"
            )

        except:
            self.show_error()

    def show_error(self):
        dialog = MDDialog(
            title="Error",
            text="Enter valid numbers"
        )
        dialog.open()

    def logout(self):
        self.manager.current = "login"

class MainApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

MainApp().run()
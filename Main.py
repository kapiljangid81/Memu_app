from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.button import MDRaisedButton

from plyer import filechooser
from plyer import camera

import os


files_data = {
    "Electrical": [],
    "Mechanical": [],
    "Pneumatic": []
}


KV = '''

ScreenManager:
    LoginScreen
    DashboardScreen
    SectionScreen


<LoginScreen>
    name: "login"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "MEMU"
            anchor_title: "center"

        Widget:
            size_hint_y: None
            height: "60dp"

        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "20dp"
            size_hint_y: None
            height: "220dp"

            MDTextField:
                id: username
                hint_text: "Username"

            MDTextField:
                id: password
                hint_text: "Password"
                password: True

            MDRaisedButton:
                text: "Login"
                pos_hint: {"center_x": .5}
                on_release: app.check_login()

        Widget



<DashboardScreen>
    name: "dashboard"

    MDNavigationLayout:

        ScreenManager:

            MDScreen:

                MDBoxLayout:
                    orientation: "vertical"

                    MDTopAppBar:
                        title: "MEMU"
                        anchor_title: "center"
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                        right_action_items: [["logout", lambda x: app.logout()]]

                    MDBoxLayout:
                        orientation: "vertical"
                        padding: "20dp"
                        spacing: "20dp"

                        MDTextField:
                            hint_text: "AI Search"

                        Spinner:
                            id: section_select
                            text: "Select Section"
                            values: ["Electrical","Mechanical","Pneumatic"]
                            size_hint_y: None
                            height: "50dp"

                        MDRaisedButton:
                            text: "Upload File"
                            pos_hint: {"center_x": .5}
                            on_release: app.open_file()

                        MDRaisedButton:
                            text: "Capture Photo"
                            pos_hint: {"center_x": .5}
                            on_release: app.open_camera()

                        MDLabel:
                            id: file_label
                            text: "No file selected"
                            halign: "center"

                        MDRaisedButton:
                            text: "Save File"
                            pos_hint: {"center_x": .5}
                            on_release: app.save_file()


        MDNavigationDrawer:
            id: nav_drawer

            MDBoxLayout:
                orientation: "vertical"

                MDList:

                    OneLineIconListItem:
                        text: "Failure History"
                        IconLeftWidget:
                            icon: "alert"

                    OneLineIconListItem:
                        text: "Schedule History"
                        IconLeftWidget:
                            icon: "calendar"

                    OneLineIconListItem:
                        text: "Equipment Details"
                        IconLeftWidget:
                            icon: "tools"

                    OneLineIconListItem:
                        text: "Rake Wise Remark"
                        IconLeftWidget:
                            icon: "train"

                    OneLineIconListItem:
                        text: "Online Remarks"
                        IconLeftWidget:
                            icon: "note"

                    OneLineIconListItem:
                        text: "Rake Link"
                        IconLeftWidget:
                            icon: "link"

                    OneLineIconListItem:
                        text: "Files"
                        on_release: app.open_section_page()
                        IconLeftWidget:
                            icon: "folder"

                    OneLineIconListItem:
                        text: "Logout"
                        on_release: app.logout()
                        IconLeftWidget:
                            icon: "power"



<SectionScreen>
    name: "section"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Files"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]

        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "20dp"

            Spinner:
                id: section_view
                text: "Select Section"
                values: ["Electrical","Mechanical","Pneumatic"]
                size_hint_y: None
                height: "50dp"
                on_text: app.load_files(self.text)

            MDBoxLayout:
                id: files_list
                orientation: "vertical"
                spacing: "10dp"

'''


class LoginScreen(Screen):
    pass


class DashboardScreen(Screen):
    pass


class SectionScreen(Screen):
    pass


class MEMUApp(MDApp):

    selected_file = ""


    def build(self):
        return Builder.load_string(KV)


    def check_login(self):

        screen = self.root.get_screen("login")

        if screen.ids.username.text == "a" and screen.ids.password.text == "a":

            toast("Login Successful")
            self.root.current = "dashboard"

        else:

            toast("Invalid Login")


    def logout(self):

        self.root.current = "login"


    def open_file(self):

        filechooser.open_file(on_selection=self.select_file)


    def select_file(self, selection):

        if selection:

            self.selected_file = selection[0]

            screen = self.root.get_screen("dashboard")

            screen.ids.file_label.text = os.path.basename(self.selected_file)


    def open_camera(self):

        camera.take_picture(
            filename="/storage/emulated/0/captured_photo.jpg",
            on_complete=self.camera_saved
        )


    def camera_saved(self, path):

        if path:

            self.selected_file = path

            screen = self.root.get_screen("dashboard")

            screen.ids.file_label.text = os.path.basename(path)


    def save_file(self):

        screen = self.root.get_screen("dashboard")

        section = screen.ids.section_select.text

        if section == "Select Section":

            toast("Select Section First")
            return

        if self.selected_file == "":

            toast("No file selected")
            return

        files_data[section].append(self.selected_file)

        toast("File Saved")


    def open_section_page(self):

        self.root.current = "section"


    def go_back(self):

        self.root.current = "dashboard"


    def load_files(self, section):

        screen = self.root.get_screen("section")

        screen.ids.files_list.clear_widgets()

        if section in files_data:

            for file in files_data[section]:

                btn = MDRaisedButton(
                    text=os.path.basename(file),
                    size_hint_y=None,
                    height="45dp"
                )

                screen.ids.files_list.add_widget(btn)


MEMUApp().run()

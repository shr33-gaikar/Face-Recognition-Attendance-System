import tkinter as tk
from PIL import Image, ImageTk
import cv2
import util
from register import RegisterGUI
import login

class App:
    def __init__(self):
        self.main_window = tk.Tk()

        # Maximize the window
        self.main_window.state('zoomed')

        # Load background image
        self.background_image = Image.open("bg.png")
        self.background_image = self.background_image.resize((1200, 520))

        # Display background image
        self.background_image = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.main_window, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Login button
        self.login_button_main_window = util.get_button(self.main_window, 'Login', 'green', self.login)
        self.login_button_main_window.place(x=953, y=400)

        # Register button
        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=953, y=500)

        # Webcam label
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=167, y=143)

        # Webcam capture
        self.add_webcam(self.webcam_label)
        self.process_webcam()

        # Bind "q" key to quit function
        self.main_window.bind("q", self.quit_app)

    def quit_app(self, event):
        self.main_window.destroy()

    def add_webcam(self, label):
        self.cap = cv2.VideoCapture(0)
        self._label = label

    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame

        if ret:
            frame = cv2.flip(frame, 1)
            img_ = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_ = cv2.resize(img_, (700, 500))
            self.most_recent_capture_pil = Image.fromarray(img_)
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            self._label.imgtk = imgtk
            self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def start(self):
        self.main_window.mainloop()

    def login(self):
        login.login()

    def register_new_user(self):
        register_gui = RegisterGUI()
        register_gui.register_user()

if __name__ == "__main__":
    app = App()
    app.start()



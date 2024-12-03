import os
import datetime
import pickle
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
import util
from test import test
import threading


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        # Buttons for login/logout/register functionalities
        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=200)

        self.logout_button_main_window = util.get_button(self.main_window, 'logout', 'red', self.logout)
        self.logout_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray', self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        # Webcam label for capturing and displaying webcam feed
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.images_dir = os.path.join(self.db_dir, 'images')
        if not os.path.exists(self.images_dir):
            os.mkdir(self.images_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                util.msg_box('Error', 'Unable to access webcam!')
                return

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        # Capture webcam frame
        ret, frame = self.cap.read()
        if not ret:
            util.msg_box('Error', 'Failed to capture webcam frame')
            return

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        # Re-run after 20ms for the next frame
        self._label.after(20, self.process_webcam)

    def deepfake_detection(self, frame):
        """
        Function to detect deepfake video.
        Returns:
            True if a deepfake is detected, False otherwise.
        """
        try:
            label = test(
                image=frame,
                model_dir='./Silent-Face-Anti-Spoofing/resources/anti_spoof_models',
                device_id=0
            )
            return label == 0
        except Exception as e:
            util.msg_box('Error', f'Deepfake detection failed: {str(e)}')
            return False  # Assume it's not a deepfake if detection fails

    def login(self):
        # Run login operations in a separate thread to avoid blocking the main thread
        def run_login():
            try:
                # Check for deepfake before proceeding with login
                if self.deepfake_detection(self.most_recent_capture_arr):
                    util.msg_box('Hey, you are a spoofer!', 'You are fake!')
                    return

                name = util.recognize(self.most_recent_capture_arr, self.db_dir)

                if name in ['unknown_person', 'no_persons_found']:
                    util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
                else:
                    # Check if image exists for the user
                    user_image_path = os.path.join(self.images_dir, f'{name}.jpg')
                    if os.path.exists(user_image_path):
                        util.msg_box('Warning', 'User is already registered with an image!')
                    else:
                        util.msg_box('Welcome back !', f'Welcome, {name}.')
                        with open(self.log_path, 'a') as f:
                            f.write(f'{name},{datetime.datetime.now()},in\n')

            except Exception as e:
                util.msg_box('Error', f'Login process failed: {str(e)}')

        # Run login process in a background thread
        threading.Thread(target=run_login, daemon=True).start()

    def logout(self):
        # Run logout operations in a separate thread to avoid blocking the main thread
        def run_logout():
            try:
                if self.deepfake_detection(self.most_recent_capture_arr):
                    util.msg_box('Hey, you are a spoofer!', 'You are fake!')
                    return

                name = util.recognize(self.most_recent_capture_arr, self.db_dir)

                if name in ['unknown_person', 'no_persons_found']:
                    util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
                else:
                    util.msg_box('Hasta la vista !', f'Goodbye, {name}.')
                    with open(self.log_path, 'a') as f:
                        f.write(f'{name},{datetime.datetime.now()},out\n')

            except Exception as e:
                util.msg_box('Error', f'Logout process failed: {str(e)}')

        # Run logout process in a background thread
        threading.Thread(target=run_logout, daemon=True).start()

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please, \ninput username:')
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        try:
            self.main_window.mainloop()
        except KeyboardInterrupt:
            util.msg_box('Error', 'The application was interrupted unexpectedly. Please try again.')

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        # Check if the user already exists (based on the image folder)
        user_image_path = os.path.join(self.images_dir, f'{name}.jpg')
        if os.path.exists(user_image_path):
            util.msg_box('Warning', 'User is already registered with an image!')
            return  # Prevent further registration

        # Save the image of the user
        try:
            cv2.imwrite(user_image_path, self.register_new_user_capture)

            embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]

            # Save the user's embeddings to a pickle file
            with open(os.path.join(self.db_dir, f'{name}.pickle'), 'wb') as file:
                pickle.dump(embeddings, file)

            util.msg_box('Success!', 'User was registered successfully!')
        except Exception as e:
            util.msg_box('Error', f'Registration failed: {str(e)}')

        self.register_new_user_window.destroy()


if __name__ == "__main__":
    app = App()
    app.start()

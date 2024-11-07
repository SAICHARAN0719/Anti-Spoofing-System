import os
import pickle
import tkinter as tk
from tkinter import messagebox  # Correct import for messagebox
import face_recognition


def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
        window,
        text=text,
        activebackground="black",
        activeforeground="white",
        fg=fg,
        bg=color,
        command=command,
        height=2,
        width=20,
        font=('Helvetica bold', 20)
    )
    return button


def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label


def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=2,
                       width=15, font=("Arial", 32))
    return inputtxt


def msg_box(title, description):
    messagebox.showinfo(title, description)  # messagebox used here


def recognize(img, db_path):
    """
    This function tries to recognize a person from the given image by comparing the image's face embeddings
    to the embeddings stored in pickle files in the database.
    Returns the name of the recognized person or 'no_persons_found' if no faces are detected,
    or 'unknown_person' if no match is found.
    """

    # Get the face encoding of the input image (assumes the image contains one face)
    embeddings_unknown = face_recognition.face_encodings(img)

    # If no faces are detected in the image, return 'no_persons_found'
    if len(embeddings_unknown) == 0:
        return 'no_persons_found'

    # We take the first detected face encoding (assuming there is only one face in the image)
    embeddings_unknown = embeddings_unknown[0]

    # Get the list of all files in the database directory
    db_dir = sorted(os.listdir(db_path))

    # Iterate over the files in the database directory and compare the embeddings
    for filename in db_dir:
        # Only consider pickle files
        if filename.endswith('.pickle'):
            path_ = os.path.join(db_path, filename)
            try:
                # Open and load the pickle file containing the stored embeddings
                with open(path_, 'rb') as file:
                    embeddings = pickle.load(file)

                # Compare the embeddings using face_recognition
                match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]

                if match:
                    # If a match is found, return the name (without the '.pickle' extension)
                    return filename[:-7]  # Strip '.pickle' from filename
            except (pickle.UnpicklingError, EOFError) as e:
                print(f"Error loading pickle file {filename}: {e}")
                continue  # Skip this file and move to the next one

    # If no match was found, return 'unknown_person'
    return 'unknown_person'

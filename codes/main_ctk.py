import customtkinter as ctk
from tkinter import messagebox, filedialog
import time
import threading
from logo_to_video import AddLogoProcess
import os

# Function to browse and select a video file
def browse_file():
    file_path = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=[("Video Files", "*.mp4 *.avi *.mkv *.mov"), ("All Files", "*.*")]
    )
    if file_path:
        label_file_path.configure(text=file_path)

# Function to simulate a process and update the progress bar
def start_process(file_path, float_number, option1, option2):
    # TODO: options to be inculded
    add_logo = AddLogoProcess(file_path,loc=option2)
    add_logo.process(frame_progress=frame_progress,label_progress=label_progress)
    messagebox.showinfo("Process Complete", "To open the resulting file click OK!")
    os.startfile(os.path.dirname(file_path))

# Function to handle the button click
def on_button_click():
    try:
        # Get the float number from the textbox
        float_number = float(text_box.get("1.0", "end").strip())
        
        # Get the selected options from the radio button sections
        selected_option1 = radio_var1.get()
        selected_option2 = radio_var2.get()
        
        # Get the video file path
        file_path = label_file_path.cget("text")
        
        # Check if all inputs are provided
        if not file_path or not selected_option1 or not selected_option2:
            messagebox.showwarning("Incomplete Selection", "Please complete all selections!")
        else:
            # Run the progress bar in a separate thread to keep the UI responsive
            threading.Thread(target=start_process, args=(file_path, float_number, selected_option1, selected_option2)).start()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid float number!")

# Configure customtkinter
ctk.set_appearance_mode("System")  # Options: "System", "Light", "Dark"
ctk.set_default_color_theme("blue")  # Options: "blue", "dark-blue", "green"

window = ctk.CTk()
window.title("ERD TV logo")
window.geometry("550x500")
window.resizable(False, False)

# Section 1: Browse Section (single line)
frame_browse = ctk.CTkFrame(window)
frame_browse.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

label_browse = ctk.CTkLabel(frame_browse, text="Choose a video file:", font=("Arial", 14),anchor="e")
label_browse.grid(row=0, column=0, pady=5, sticky="w")

browse_button = ctk.CTkButton(frame_browse, text="Browse", command=browse_file, width=100)
browse_button.grid(row=1, column=0, pady=5, sticky="w")

label_file_path = ctk.CTkLabel(frame_browse, text="No file selected", font=("Arial", 12), wraplength=400)
label_file_path.grid(row=2, column=0, pady=5, sticky="w")

# Section 2: Textbox, Float Section, and Radio Sections (side by side in one row)
frame_input = ctk.CTkFrame(window)
frame_input.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

# Float Number Textbox Section
label_textbox = ctk.CTkLabel(frame_input, text="Start (s):", font=("Arial", 14),anchor="e")
label_textbox.grid(row=0, column=0, pady=5, padx=20, sticky="w")

text_box = ctk.CTkTextbox(frame_input, height=30, width=50)
text_box.grid(row=1, column=0, pady=10)

# Radio Buttons Section 1 (on the right of the float input)
radio_var1 = ctk.StringVar(value=None)  # Variable to store the selected option
label_radio1 = ctk.CTkLabel(frame_input, text="Type:", font=("Arial", 14),anchor="e")
label_radio1.grid(row=0, column=1, pady=5, padx=20, sticky="w")

radio1_1 = ctk.CTkRadioButton(frame_input, text="ERD TV", variable=radio_var1, value="Option 1.1")
radio1_1.grid(row=1, column=1, pady=5, padx=30, sticky="w")

radio1_2 = ctk.CTkRadioButton(frame_input, text="Ismétlés", variable=radio_var1, value="Option 1.2")
radio1_2.grid(row=2, column=1, pady=5, padx=30, sticky="w")


# Radio Buttons Section 2 (on the right of Section 1)
radio_var2 = ctk.StringVar(value=None)  # Variable to store the selected option
label_radio2 = ctk.CTkLabel(frame_input, text="Location:", font=("Arial", 14),anchor="e")
label_radio2.grid(row=0, column=2, pady=5, padx=20, sticky="w")

radio2_1 = ctk.CTkRadioButton(frame_input, text="top left", variable=radio_var2, value="top left")
radio2_1.grid(row=1, column=2, pady=5, padx=30, sticky="w")

radio2_2 = ctk.CTkRadioButton(frame_input, text="top right", variable=radio_var2, value="top right")
radio2_2.grid(row=2, column=2, pady=5, padx=30, sticky="w")

radio2_3 = ctk.CTkRadioButton(frame_input, text="bottom left", variable=radio_var2, value="bottom left")
radio2_3.grid(row=3, column=2, pady=5, padx=30, sticky="w")

radio2_4 = ctk.CTkRadioButton(frame_input, text="bottom right", variable=radio_var2, value="bottom right")
radio2_4.grid(row=4, column=2, pady=5, padx=30, sticky="w")

# Section 3: Progress bar and details (below the radio button sections)
frame_progress = ctk.CTkFrame(window)
frame_progress.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

label_progress = ctk.CTkLabel(frame_progress, text="Processing...", font=("Arial", 14))
label_progress.grid(row=0, column=0, pady=5,padx=20)

# Submit Button
button_submit = ctk.CTkButton(window, text="Submit", command=on_button_click, height=40, width=200)
button_submit.grid(row=3, column=0, pady=20)

# Run the application
window.mainloop()

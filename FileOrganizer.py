# File Organizer by NoahKoh
# Description: A simple file organizer with 3 simple funcitons. Organize, Extract and Delete Empty Folders

import tkinter as tk
from tkinter import filedialog
import os
import shutil
import json

file_categories = {
    "Audio": (".mp3", ".wav", ".flac", ".aif", ".cda", ".mid", ".midi", ".mpa", ".ogg", ".wpl"),
    "Font": (".fnt", ".fon", ".otf", ".ttf"),
    "Image": (".ai", ".bmp", ".gif", ".ico", ".jpeg", ".jpg", ".png", ".ps", ".psd", ".scr", ".svg", ".tif", ".tiff", ".webp"),
    "Video": (".3g2", ".3gp", ".avi", ".flv", ".h264", ".m4v", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg", ".rm", ".swf", ".vob", ".webm", ".wmv"),
    "Text Document": (".doc", ".docx", ".odt", ".pdf", ".rtf", ".tex", ".txt", ".wpd"),
    "Presentation": (".key", ".odp", ".pps", ".ppt", ".pptx"),
    "Spreadsheet": (".ods", ".xls", ".xlsm", ".xlsx"),
    "Programming": (".apk", ".c", ".cgi", ".pl", ".class", ".cpp", ".cs", ".h", ".jar", ".java", ".php", ".py", ".sh", ".swift", ".vb", ".json", ".html", ".css", ".js"),
    "Data": (".csv", ".dat", ".db", ".dbf", ".log", ".mdb", ".sav", ".sql", ".tar", ".xml"),
    "Executable": (".bat", ".bin", ".com", ".exe", ".gadget", ".msi", ".sh", ".wsf"),
    "Archive": (".zip", ".rar", ".tar", ".7z", ".arj", ".deb", ".pkg", ".rpm", ".tar.gz", ".z"),
    "System": (".bak", ".cab", ".cfg", ".cpl", ".cur", ".dll", ".dmp", ".drv", ".icns", ".ico", ".ini", ".lnk", ".msi", ".sys", ".tmp"),
    # Add more categories here
}

def save_categories_to_file():
    global file_categories
    config_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialfile="config.json")
    if config_path:
        with open(config_path, "w") as config_file:
            json.dump(file_categories, config_file)
            print(os.getcwd())

def load_categories_from_file():
    global file_categories
    file_categories = {}
    config_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if config_path:
        try:
            with open(config_path, "r") as config_file:
                saved_categories = json.load(config_file)
                file_categories.update(saved_categories)
        except FileNotFoundError:
            pass  # Use default categories if config file doesn't exist

def default_categories():
    global file_categories
    file_categories = {
    "Audio": (".mp3", ".wav", ".flac", ".aif", ".cda", ".mid", ".midi", ".mpa", ".ogg", ".wpl"),
    "Font": (".fnt", ".fon", ".otf", ".ttf"),
    "Image": (".ai", ".bmp", ".gif", ".ico", ".jpeg", ".jpg", ".png", ".ps", ".psd", ".scr", ".svg", ".tif", ".tiff", ".webp"),
    "Video": (".3g2", ".3gp", ".avi", ".flv", ".h264", ".m4v", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg", ".rm", ".swf", ".vob", ".webm", ".wmv"),
    "Text Document": (".doc", ".docx", ".odt", ".pdf", ".rtf", ".tex", ".txt", ".wpd"),
    "Presentation": (".key", ".odp", ".pps", ".ppt", ".pptx"),
    "Spreadsheet": (".ods", ".xls", ".xlsm", ".xlsx"),
    "Programming": (".apk", ".c", ".cgi", ".pl", ".class", ".cpp", ".cs", ".h", ".jar", ".java", ".php", ".py", ".sh", ".swift", ".vb", ".json", ".html", ".css", ".js"),
    "Data": (".csv", ".dat", ".db", ".dbf", ".log", ".mdb", ".sav", ".sql", ".tar", ".xml"),
    "Executable": (".bat", ".bin", ".com", ".exe", ".gadget", ".msi", ".sh", ".wsf"),
    "Archive": (".zip", ".rar", ".tar", ".7z", ".arj", ".deb", ".pkg", ".rpm", ".tar.gz", ".z"),
    "System": (".bak", ".cab", ".cfg", ".cpl", ".cur", ".dll", ".dmp", ".drv", ".icns", ".ico", ".ini", ".lnk", ".msi", ".sys", ".tmp"),
    # Add more categories here
    }


def organize_files(directory):
    os.chdir(directory)

    for file in os.listdir():
        if os.path.isfile(file):
            for category, extensions in file_categories.items():
                if file.lower().endswith(extensions):
                    if not os.path.exists(category):
                        os.makedirs(category)
                    shutil.move(file, category)
                    break
            else:
                if not os.path.exists("Other"):
                    os.makedirs("Other")
                shutil.move(file, "Other")
        else:
            if not os.path.exists("Other"):
                os.makedirs("Other")
            if not file in file_categories and file != "Other":
                shutil.move(file, "Other")

def extract_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            src_path = os.path.join(root, file)
            shutil.move(src_path, directory)

def delete_empty_directories(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):  # Check if the directory is empty
                os.rmdir(dir_path)

def add_category(category_name, *extensions):
    if not category_name in file_categories:
        file_categories[category_name] = extensions
    else:
        existing_extension = file_categories[category_name]
        new_extension = existing_extension + extensions
        file_categories[category_name] = tuple(set(new_extension))

def on_go_button_click():
    directory = entry_path.get()
    organize_files(directory)
    status_label.config(text="Files organized!")

def on_extract_button_click():
    directory = entry_path.get()
    extract_files(directory)
    status_label.config(text="Files extracted!")

def on_delete_button_click():
    directory = entry_path.get()
    delete_empty_directories(directory)
    status_label.config(text="Folders deleted!")

def browse_directory():
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        entry_path.config(state="normal")
        entry_path.delete(0, tk.END)  # Clear existing text
        entry_path.insert(0, selected_directory)
        entry_path.config(state="readonly")

def open_config_window():
    config_window = tk.Toplevel(root)
    config_window.title("Configuration")
    config_window.geometry("800x600")

    canvas = tk.Canvas(config_window, height=200)
    canvas.pack(fill="both", expand=True)
    inner_frame = tk.Frame(config_window)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    inner_frame.place(relx=0.5, rely=0.5, anchor="c") # put at center of window
    
    # Display existing categories and extensions
    labelHeader = tk.Label(inner_frame, text="Category: Extensions")
    labelHeader.pack(pady=5)
    for category, extensions in file_categories.items():
        label = tk.Label(inner_frame, text=f"{category}: {', '.join(extensions)}")
        label.pack()

    # Input fields for new category and extensions
    global new_category_entry, new_extensions_entry, status_label_category, status_label_extensions
    category_label = tk.Label(inner_frame, text="Category")
    new_category_entry = tk.Entry(inner_frame)
    status_label_category = tk.Label(inner_frame, text="")
    extensions_label = tk.Label(inner_frame, text="Extensions (e.g. .txt, .pdf)")
    new_extensions_entry = tk.Entry(inner_frame)
    status_label_extensions = tk.Label(inner_frame, text="")
    add_button = tk.Button(inner_frame, text="Add", command=add_new_category)
    save_button = tk.Button(inner_frame, text="Export", command=save_categories_to_file)
    load_button = tk.Button(inner_frame, text="Import", command=load_categories_from_file)
    default_button = tk.Button(inner_frame, text="Default", command=default_categories)

    category_label.pack()
    new_category_entry.pack()
    status_label_category.pack()
    extensions_label.pack()
    new_extensions_entry.pack()
    status_label_extensions.pack()
    add_button.pack()
    save_button.pack(pady=10)
    load_button.pack()
    default_button.pack(pady=10)
    


    scrollbar = tk.Scrollbar(config_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def add_new_category():
    new_category = new_category_entry.get().strip()
    new_extensions = tuple(map(str.strip, new_extensions_entry.get().split(",")))
    print(new_extensions)
    if not new_category:
        # Display an error message or take appropriate action
        status_label_category.config(text="Error: Category name cannot be blank")
        return
    if not is_valid_extension(new_extensions):
        status_label_extensions.config(text="Error: Please enter a valid file extension with a dot prefix")
        return
    add_category(new_category, *new_extensions)
    status_label_category.config(text="")
    # Refresh the display of categories and extensions in the config window

def is_valid_extension(extensions):
    for extension in extensions:
        extension = extension.strip()
        if extension.count(".") != 1:
            return False
        if len(extension) <= 1:
            return False
        if extension[0] != ".":
            return False
    return True

def open_info_window():
    info_window = tk.Toplevel(root)
    info_window.title("Information")
    info_window.geometry("800x600")

    frame = tk.Frame(info_window)
    frame.place(relx=0.5, rely=0.5, anchor="c") # put at center of window

    label1 = tk.Label(frame, text="How to use:")
    label1.pack()
    label2 = tk.Label(frame, text="Choose your folder and click Organize")
    label2.pack()
    label3 = tk.Label(frame, text="Your may use the Configuration to add categories and extensions")
    label3.pack()
    label4 = tk.Label(frame, text="If you wish to add on to existing category, just type the same category name")
    label4.pack()
    label4 = tk.Label(frame, text="If you wish to configure it with more freedom, Export a JSON file, manually edit the file and Import")
    label4.pack()
    label5 = tk.Label(frame, text="You may relaunch or click Default to set it back to the default categories and extensions")
    label5.pack()
    label6 = tk.Label(frame, text="Created by NoahKoh")
    label6.pack()


root = tk.Tk()
root.geometry("400x300")
root.title("File Organizer")

frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor="c") # put at center of window

label_path = tk.Label(frame, text="Enter directory path:")
entry_path = tk.Entry(frame, state="readonly")
browse_button = tk.Button(frame, text="Browse", command=browse_directory)
go_button = tk.Button(frame, text="Organize", command=on_go_button_click)
status_label = tk.Label(frame, text="")
extract_button = tk.Button(frame, text="Extract", command=on_extract_button_click)
config_button = tk.Button(frame, text="Configure", command=open_config_window)
info_button = tk.Button(root, text="Info", command=open_info_window)
delete_button = tk.Button(root, text="Delete Empty Folders", command=on_delete_button_click)

label_path.pack(pady=10)
entry_path.pack(pady=10)
browse_button.pack(pady=10)
go_button.pack(pady=10)
status_label.pack(pady=10)
extract_button.pack(pady=10)
config_button.pack(pady=10)
info_button.place(relx=0.9, rely=0.9)
delete_button.place(relx=0.01   , rely=0.9)

root.mainloop()
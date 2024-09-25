import os
import shutil
import tkinter as tk

folders_to_clean = {

    'data_frames': {
        'except': ['.gitignore']
    },
    'debug': {
        'except': ['.gitignore']
    }

}


def clean_cache():
    for folder, files in folders_to_clean.items():
        except_files = files.get('except', [])
        for file in os.listdir(folder):
            if file not in except_files:
                file_path = os.path.join(folder, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)



if __name__ == '__main__':
    clean_cache()

    # label content warning about each field to cleanup

    label_warning_message = "This will delete the following folders: \n"
    for folder in folders_to_clean:
        label_warning_message += f"{folder}\n"

    root = tk.Tk()
    root.title("Warning")
    root.geometry("300x300")
    label = tk.Label(root, text=label_warning_message)

    label.pack()


    def yes_method():
        clean_cache()
        root.quit()


    button = tk.Button(root, text="Yes", command=yes_method)
    button.pack()
    root.mainloop()

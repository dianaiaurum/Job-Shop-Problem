import tkinter as tk

def open_input_window():
    global f
    try:
        entered_text = entry.get()
        f = open(entered_text, "r")
    except FileNotFoundError:
        label = tk.Label(window, text="The path given doesn't return any document. Please check the location of your file or the format of the path and try again")
        label.pack()
    except OSError:
        label = tk.Label(window, text="Invalid path.")
        label.pack()
    except:
        label = tk.Label(window, text="Invalid argument.")
        label.pack()
    else:
        close_current_window()

def close_current_window():
    window.destroy()

# Create the main window
window = tk.Tk()

# Create an Entry widget
entry = tk.Entry(window)
entry.pack()

# Create a button widget
button = tk.Button(window, text="Submit", command=open_input_window)
button.pack()

# Start the GUI event loop
window.mainloop()


    







import tkinter as tk
from tkinter import ttk, filedialog
from threading import Thread, Event

class App:
    def __init__(self, root):
        self.root = root
        root.title("Start-Stop App")
        
        # 1st Line: Label for "Process"
        self.process_label = ttk.Label(root, text="Process:")
        self.process_label.grid(row=0, column=0, sticky='w', pady=5, padx=5)
        
        # 2nd Line: Start, Stop, and Clear Buttons
        self.start_button = ttk.Button(root, text="Start", command=self.start_loop)
        self.start_button.grid(row=1, column=0, pady=5, padx=5)
        
        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_loop, state=tk.DISABLED)
        self.stop_button.grid(row=1, column=1, pady=5, padx=5)

        self.clear_button = ttk.Button(root, text="Clear", command=self.clear_output)
        self.clear_button.grid(row=1, column=2, pady=5, padx=5)
        
        # 3rd Line: Label for "Output"
        self.output_label = ttk.Label(root, text="Output:")
        self.output_label.grid(row=2, column=0, sticky='w', pady=5, padx=5)
        
        # 4th Line: Text Area with Scrollbar
        self.text_output = tk.Text(root, wrap=tk.WORD, width=40, height=10)
        self.scrollbar = ttk.Scrollbar(root, command=self.text_output.yview)
        self.text_output.config(yscrollcommand=self.scrollbar.set)

        self.text_output.grid(row=3, column=0, columnspan=3, sticky='nsew', padx=5)
        self.scrollbar.grid(row=3, column=3, sticky='ns')

        # 5th Line: File Chooser and Save Button
        self.file_label = ttk.Label(root, text="Save to:")
        self.file_label.grid(row=4, column=0, sticky='w', pady=5, padx=5)

        self.file_entry = ttk.Entry(root)
        self.file_entry.grid(row=4, column=1, sticky='ew', padx=5)

        self.browse_button = ttk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=4, column=2, padx=5)

        self.save_button = ttk.Button(root, text="Save", command=self.save_file)
        self.save_button.grid(row=4, column=3, padx=5)

        # 6th Line: Label for "Status"
        self.status_label = ttk.Label(root, text="Status: Not Running")
        self.status_label.grid(row=5, column=0, sticky='w', columnspan=3, pady=5, padx=5)

        # Event for stopping the loop
        self.stop_event = Event()

    def start_loop(self):
        """Start the loop and toggle the button states."""
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Running")

        # Start the loop in a new thread
        self.thread = Thread(target=self.loop)
        self.thread.start()

    def stop_loop(self):
        """Stop the loop and toggle the button states."""
        self.stop_event.set()
        # Wait for the thread to finish
        self.thread.join()

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Not Running")

    def clear_output(self):
        """Clear the contents of the text area."""
        self.text_output.delete(1.0, tk.END)

    def browse_file(self):
        """Open a file dialog and update the file entry with the selected path."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def save_file(self):
        """Save the content of the text area to the file specified in the file entry."""
        file_path = self.file_entry.get()
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_output.get(1.0, tk.END))

    def loop(self):
        """The loop to run in the background."""
        while not self.stop_event.is_set():
            # This is the work of your loop.
            self.text_output.insert(tk.END, "Running...\n")
            self.text_output.see(tk.END)
            self.stop_event.wait(1)

        # Reset the stop event for the next run
        self.stop_event.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.grid_columnconfigure(1, weight=1)  # This makes the file entry expand with the window
    root.grid_rowconfigure(3, weight=1)  # This makes the text area fill all remaining vertical space
    root.mainloop()

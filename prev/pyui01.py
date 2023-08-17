import tkinter as tk
from tkinter import ttk
from threading import Thread, Event

class App:
    def __init__(self, root):
        self.root = root
        root.title("Start-Stop App")
        
        # 1st Line: Label for "Process"
        self.process_label = ttk.Label(root, text="Process:")
        self.process_label.grid(row=0, column=0, sticky='w', pady=5, padx=5)
        
        # 2nd Line: Start and Stop Buttons
        self.start_button = ttk.Button(root, text="Start", command=self.start_loop)
        self.start_button.grid(row=1, column=0, pady=5, padx=5)
        
        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_loop, state=tk.DISABLED)
        self.stop_button.grid(row=1, column=1, pady=5, padx=5)
        
        # 3rd Line: Label for "Output"
        self.output_label = ttk.Label(root, text="Output:")
        self.output_label.grid(row=2, column=0, sticky='w', pady=5, padx=5)
        
        # 4th Line: Text Area with Scrollbar
        self.text_output = tk.Text(root, wrap=tk.WORD, width=40, height=10)
        self.scrollbar = ttk.Scrollbar(root, command=self.text_output.yview)
        self.text_output.config(yscrollcommand=self.scrollbar.set)

        self.text_output.grid(row=3, column=0, columnspan=2, sticky='ew', padx=5)
        self.scrollbar.grid(row=3, column=2, sticky='ns')

        # 5th Line: Label for "Status"
        self.status_label = ttk.Label(root, text="Status: Not Running")
        self.status_label.grid(row=4, column=0, sticky='w', columnspan=2, pady=5, padx=5)
        
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

    def loop(self):
        """The loop to run in the background."""
        while not self.stop_event.is_set():
            # This is the work of your loop.
            # For demonstration purposes, I'm just inserting "Running...\n" into the text area.
            # Replace this with your actual code.
            self.text_output.insert(tk.END, "Running...\n")
            # Ensure the Text widget scrolls to show the latest text
            self.text_output.see(tk.END)

            # Sleep for a while to simulate work
            self.stop_event.wait(1)  # Waits for 1 second or until the stop event is set

        # Reset the stop event for the next run
        self.stop_event.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    # Making the window resizable in horizontal direction
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()

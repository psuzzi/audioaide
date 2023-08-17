import tkinter as tk
from threading import Thread, Event

class App:
    def __init__(self, root):
        self.root = root
        root.title("Start-Stop App")

        # Create the buttons
        self.start_button = tk.Button(root, text="Start", command=self.start_loop)
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_loop, state=tk.DISABLED)
        
        # Pack the buttons
        self.start_button.pack(pady=20)
        self.stop_button.pack(pady=20)
        
        # Event for stopping the loop
        self.stop_event = Event()

    def start_loop(self):
        """Start the loop and toggle the button states."""
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
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

    def loop(self):
        """The loop to run in the background."""
        while not self.stop_event.is_set():
            # This is the work of your loop.
            # For demonstration purposes, I'm just printing "Running...".
            # Replace this with your actual code.
            print("Running...")
            
            # Sleep for a while to simulate work
            self.stop_event.wait(1)  # Waits for 1 second or until the stop event is set

        # Reset the stop event for the next run
        self.stop_event.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

import customtkinter as ctk
import threading
import yaml
from watcher import start_watching
from tkinter import filedialog # To open a folder selection dialog

# --- Main Application Class ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("File Sorter")
        self.geometry("600x550") # Increased window size
        
        # --- State Variables ---
        self.watcher_thread = None
        self.stop_event = threading.Event()
        self.config_file_path = 'config.yaml'

        # --- UI Theme ---
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # --- Widgets ---
        
        # --- Service Control Frame ---
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(pady=10, padx=10, fill="x")

        self.status_label = ctk.CTkLabel(control_frame, text="Status: Stopped 🔴", font=("Arial", 20))
        self.status_label.pack(pady=10)

        self.start_button = ctk.CTkButton(control_frame, text="Start Service", command=self.start_service)
        self.start_button.pack(side="left", expand=True, padx=5, pady=5)

        self.stop_button = ctk.CTkButton(control_frame, text="Stop Service", command=self.stop_service, state="disabled")
        self.stop_button.pack(side="left", expand=True, padx=5, pady=5)

        # --- Configuration Frame ---
        config_frame = ctk.CTkFrame(self)
        config_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        ctk.CTkLabel(config_frame, text="Configuration", font=("Arial", 16)).pack(pady=5)
        
        # Staging Directory
        self.staging_entry = self.create_directory_entry(config_frame, "Staging Directory:")
        
        # Target Directories (will be populated dynamically)
        self.target_entries = {}
        
        self.save_button = ctk.CTkButton(config_frame, text="Save Configuration", command=self.save_config)
        self.save_button.pack(pady=20)
        
        self.load_config()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_directory_entry(self, parent, label_text):
        """Helper function to create a label, entry, and browse button row."""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=5, pady=5)
        
        label = ctk.CTkLabel(frame, text=label_text, width=120)
        label.pack(side="left")
        
        entry = ctk.CTkEntry(frame, width=300)
        entry.pack(side="left", expand=True, padx=5)
        
        def browse_folder():
            folder_path = filedialog.askdirectory()
            if folder_path:
                entry.delete(0, "end")
                entry.insert(0, folder_path)
                
        browse_button = ctk.CTkButton(frame, text="Edit", width=30, command=browse_folder)
        browse_button.pack(side="left")
        
        return entry

    def load_config(self):
        """Loads configuration from yaml and populates UI fields."""
        with open(self.config_file_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.staging_entry.insert(0, config.get('staging_directory', ''))
        
        # Clear old target entries if any
        for widget in self.target_entries.values():
            widget.master.destroy()
        self.target_entries.clear()
        
        # Create new target entries
        for key, value in config.get('target_directories', {}).items():
            entry_widget = self.create_directory_entry(self.save_button.master, f"{key.title()} Directory:")
            entry_widget.insert(0, value)
            self.target_entries[key] = entry_widget
            # Move the save button to the bottom again
            self.save_button.pack_forget()
            self.save_button.pack(pady=20)


    def save_config(self):
        """Saves the current UI fields back to the yaml file."""
        with open(self.config_file_path, 'r') as f:
            config = yaml.safe_load(f)
            
        config['staging_directory'] = self.staging_entry.get()
        
        for key, entry_widget in self.target_entries.items():
            config['target_directories'][key] = entry_widget.get()
            
        with open(self.config_file_path, 'w') as f:
            yaml.dump(config, f, sort_keys=False)
        
        
        print("✅ Configuration saved!")


    def start_service(self):
        """Starts the file watcher in a background thread."""
       
        if self.watcher_thread is None or not self.watcher_thread.is_alive():
            print("Starting service...")
            self.stop_event.clear()
            
            with open(self.config_file_path, 'r') as f:
                config_data = yaml.safe_load(f)

            self.watcher_thread = threading.Thread(
                target=start_watching,
                args=(config_data, self.stop_event),
                daemon=True
            )
            self.watcher_thread.start()
            
            self.status_label.configure(text="Status: Running 🟢", text_color="green")
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            
    def stop_service(self):
        """Stops the file watcher thread."""
       
        if self.watcher_thread and self.watcher_thread.is_alive():
            print("Stopping service...")
            self.stop_event.set()
            
            self.status_label.configure(text="Status: Stopped 🔴", text_color="red")
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")

    def on_closing(self):
        """Called when the user closes the window."""
        self.stop_service()
        self.destroy()

# --- Run the Application ---
if __name__ == "__main__":
    app = App()
    app.mainloop()
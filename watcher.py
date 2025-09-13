import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor
from sorter import process_file 

class StagingAreaHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.config = config
        # Create a thread pool with a number of workers
        self.executor = ThreadPoolExecutor(max_workers=8) 

    def on_created(self, event):
        """Called when a file or directory is created."""
        if not event.is_directory:
            # Submit the file processing task to the thread pool
            self.executor.submit(process_file, event.src_path, self.config['target_directories'])

def start_watching(config, stop_event): # Added stop_event parameter
    path = config['staging_directory']
    event_handler = StagingAreaHandler(config)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print(f"🚀 Watcher thread started. Watching directory: {path}")
    
    # This loop now checks the stop_event
    while not stop_event.is_set():
        time.sleep(1)
        
    observer.stop()
    observer.join()
    print("🛑 Watcher thread stopped.")
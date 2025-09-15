AutoSort - The Intelligent File Sorter
AutoSort is a powerful, GUI-driven utility that monitors a "hot folder" and automatically classifies and sorts files based on their actual content, not their file extension. It's designed to be a highly responsive staging area, capable of processing thousands of extension-less files in seconds and moving them to their designated homes with the correct file extension.

✨ Key Features
Hot Folder Monitoring: Actively watches a pre-set staging directory for new files.

Content-Based Identification: Uses "magic numbers" (file signatures) to identify file types like PNG, JPEG, PDF, and MP3, even if they have no file extension.

Automatic Sorting & Renaming: Moves identified files to user-defined target directories and assigns the correct file extension.

Intuitive GUI: A clean and modern user interface to start/stop the service and configure directory paths on the fly.

High Performance: Built with a multi-threaded architecture to handle thousands of files efficiently without freezing the UI.

Robust and Reliable: Includes a retry mechanism to handle files that are temporarily locked by the system during the copy process.

Easy Configuration: All settings are managed through a simple, human-readable config.yaml file.

⚙️ How It Works
The application uses a producer-consumer architecture for maximum efficiency:

The Watcher (Producer): The watchdog library monitors the staging directory. When it detects a new file, it adds the file's path to a queue.

The Worker Pool (Consumers): A ThreadPoolExecutor runs multiple worker threads. These threads pick up file paths from the queue and perform the following actions:

Use python-magic to read the file's magic number and identify its true MIME type.

Look up the target directory in the config.yaml configuration.

Move and rename the file to its new home, adding the correct extension.

The GUI: A CustomTkinter window acts as the main control panel, running on the main thread. It manages the background worker thread and allows for real-time configuration changes.

🛠️ Technology Stack
Language: Python 3

GUI: CustomTkinter

Directory Monitoring: Watchdog

File Type Identification: python-magic

Configuration: PyYAML

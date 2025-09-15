## AutoSort - The Intelligent File Sorter

AutoSort is a powerful, GUI-driven utility that monitors a "hot folder" and automatically classifies and sorts files based on their actual content, not their file extension. It's designed to be a highly responsive staging area, capable of processing thousands of extension-less files in seconds and moving them to their designated homes with the correct file extension.

# ✨ Key Features

Hot Folder Monitoring: Actively watches a pre-set staging directory for new files.

Content-Based Identification: Uses "magic numbers" (file signatures) to identify file types like PNG, JPEG, PDF, and MP3, even if they have no file extension.

Automatic Sorting & Renaming: Moves identified files to user-defined target directories and assigns the correct file extension.

Intuitive GUI: A clean and modern user interface to start/stop the service and configure directory paths on the fly.

High Performance: Built with a multi-threaded architecture to handle thousands of files efficiently without freezing the UI.

Robust and Reliable: Includes a retry mechanism to handle files that are temporarily locked by the system during the copy process.

Easy Configuration: All settings are managed through a simple, human-readable config.yaml file.

# ⚙️ How It Works

The application uses a producer-consumer architecture for maximum efficiency:

The Watcher (Producer): The watchdog library monitors the staging directory. When it detects a new file, it adds the file's path to a queue.

The Worker Pool (Consumers): A ThreadPoolExecutor runs multiple worker threads. These threads pick up file paths from the queue and perform the following actions:

Use python-magic to read the file's magic number and identify its true MIME type.

Look up the target directory in the config.yaml configuration.

Move and rename the file to its new home, adding the correct extension.

The GUI: A CustomTkinter window acts as the main control panel, running on the main thread. It manages the background worker thread and allows for real-time configuration changes.

# 🛠️ Technology Stack

Language: Python 3

GUI: CustomTkinter

Directory Monitoring: Watchdog

File Type Identification: python-magic

Configuration: PyYAML

# 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites
Python 3.7 or newer.

For python-magic on Windows, you may need to install magic binaries. On Linux/macOS, you can install it via your package manager (e.g., sudo apt-get install libmagic1).

Installation
Clone the repository:

Bash

git clone https://github.com/KevinGeorgeKuruvilla/challenge.git
cd challenge
Create and activate a virtual environment:

On Windows:

Bash

python -m venv venv
.\venv\Scripts\activate
On macOS/Linux:

Bash

python3 -m venv venv
source venv/bin/activate

Install dependencies
Bash

pip install -r requirements.txt

Install the required packages:

Bash

pip install -r requirements.txt

- Configuration\*

Before running the application, you must set up your directories in the config.yaml file.

Create the necessary folders on your computer for the staging area and the target locations.

Edit the config.yaml file with the correct paths.

Here is an example configuration:
YAML

- The "hot folder" that the application will monitor.\*

staging_directory: "C:/Users/YourUser/Desktop/Staging"

- The destination folders for each file type.\*

target_directories:
png: "C:/Users/YourUser/Pictures/PNGs"
jpeg: "C:/Users/YourUser/Pictures/JPEGs"
pdf: "C:/Users/YourUser/Documents/PDFs"
mp3: "C:/Users/YourUser/Music/MP3s"
plain: "C:/Users/YourUser/Documents/TextFiles"

Note for Windows users: Use forward slashes (/) or double backslashes (\\) in your paths.

#▶️ Usage
To run the application, simply execute the gui_app.py script from the root of the project directory:

Bash

python gui_app.py
The graphical user interface will appear. From there, you can:

Click "Start Service" to begin monitoring the staging directory.

Modify the directory paths and click "Save Configuration".

Click "Stop Service" to pause the monitoring.

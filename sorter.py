import os
import magic
import shutil
import uuid
import time
from pathlib import Path

def process_file(file_path, target_dirs):
    """Identifies, moves, and renames a single file, retrying if it's locked."""
    
    
    for i in range(10):
        try:
            # 1. Identify file type-python magic
            mime_type = magic.from_file(file_path, mime=True)
            file_type = mime_type.split('/')[-1]

            # 2. Check if we have a target directory for this type
            if file_type in target_dirs:
                target_dir = Path(target_dirs[file_type])
                target_dir.mkdir(parents=True, exist_ok=True)
                
                # 3. Create a new, unique filename
                new_filename = f"{uuid.uuid4()}.{file_type}"
                destination_path = target_dir / new_filename
                
                # 4. Move and rename the file
                shutil.move(file_path, destination_path)
                print(f"✅ Moved {file_path} -> {destination_path}")
            else:
                print(f"⚠️ Unknown file type '{file_type}' for {file_path}. Skipping.")
            
            
            break

        except PermissionError:
            print(f"⏳ File is locked by another process: {file_path}. Retrying in 0.2s...")
            time.sleep(0.2)
        
        except FileNotFoundError:
            print(f"❓ File {file_path} was moved or deleted before processing. Skipping.")
            break # Exit if file is gone

        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            break  
    else:
        # This part runs if the for loop completes without a 'break'
        print(f"❌ Failed to process {file_path} after multiple retries. File may be in use.")
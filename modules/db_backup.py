import os
import shutil
import datetime
import filecmp

def db_backup():
    # Define the paths
    data_folder = os.path.join(os.path.dirname(__file__), f"../data/")
    offers_db_path = os.path.join(data_folder, "offers.db")
    backup_folder_path = os.path.join(data_folder, "db_backups")

    # Check if offer.db exists
    if not os.path.exists(offers_db_path):
        print("Error: offer.db does not exist.")
        return

    # Create a timestamp for the backup file
    timestamp = datetime.datetime.now().strftime("%Y.%m.%d-%H.%M")

    # Create the backup file path
    backup_file_name = f"{timestamp}.db"
    backup_file_path = os.path.join(backup_folder_path, backup_file_name)

    # Copy offer.db to the backup folder with the timestamped name
    shutil.copy(offers_db_path, backup_file_path)
    print(f"Backup created: {backup_file_path}")

    # Compare original and backup files
    if filecmp.cmp(offers_db_path, backup_file_path):
        print("Files are identical.")
    else:
        print("Files are not identical.")
# SyncManager.py
import os
import json
import time
import shutil
from datetime import datetime
from EncryptionData import EncryptionData

class SyncManager:
    def __init__(self, vault_file="vault_data.json"):
        self.__sync_method = "file"  # Default sync method
        self.__sync_data = ""  # Data being synced
        self.__last_sync_time = None  # Last sync time
        self.vault_file = vault_file
        self.encryption = EncryptionData()
        self.backup_folder_name = "SecureVaultBackup"

    @property
    def sync_method(self):
        return self.__sync_method

    @property
    def last_sync_time(self):
        return self.__last_sync_time

    def sync_to_usb(self, usb_path, user_id):
        """Sync the vault data to a USB drive."""
        try:
            backup_dir = os.path.join(usb_path, self.backup_folder_name)
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            if not os.path.exists(self.vault_file):
                return False

            with open(self.vault_file, "r") as file:
                vault_data = json.load(file)

            backup_file = os.path.join(backup_dir, f"vault_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

            with open(backup_file, "w") as file:
                json.dump(vault_data, file, indent=4)

            self.__sync_method = "file"
            self.__sync_data = backup_file
            self.__last_sync_time = datetime.now()

            sync_info = {
                "last_sync": self.__last_sync_time.isoformat(),
                "source": self.vault_file,
                "backup": backup_file,
		        "user_id": user_id
            }

            with open(os.path.join(backup_dir, "sync_info.json"), "w") as file:
                json.dump(sync_info, file, indent=4)

            return True

        except Exception as e:
            print(f"Error during sync to USB: {e}")
            return False

    def sync_from_usb(self, usb_path, user_id):
        """Overwrite vault with data from USB."""
        try:
            backup_dir = os.path.join(usb_path, self.backup_folder_name)
            if not os.path.exists(backup_dir):
                print("no directory found")
                return False

            sync_info_path = os.path.join(backup_dir, "sync_info.json")
            if os.path.exists(sync_info_path):
                with open(sync_info_path, "r") as file:
                    sync_info = json.load(file)
                    backup_file = sync_info.get("backup")
            else:
                backup_files = [f for f in os.listdir(backup_dir) if f.startswith("vault_backup_") and f.endswith(".json")]
                if not backup_files:
                    print("no backup file")
                    return False

                backup_files.sort(reverse=True)
                backup_file = os.path.join(backup_dir, backup_files[0])

            if not os.path.exists(backup_file):
                print("backup file does not exist")
                return False

            # Overwrite vault_data.json
            shutil.copy2(backup_file, self.vault_file)

            self.__sync_method = "file"
            self.__sync_data = backup_file
            self.__last_sync_time = datetime.now()

            return True
        except Exception as e:
            print(f"Error during sync from USB: {e}")
            return False

    def get_last_sync_info(self):
        """Get information about the last sync operation."""
        if self.__last_sync_time:
            return {
                "method": self.__sync_method,
                "data": self.__sync_data,
                "time": self.__last_sync_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        return None

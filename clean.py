import os
from glob import glob

def clean_folder():
    clean_image = glob("image/*.png")
    for image_path in clean_image:
        try:
            os.remove(image_path)
            print(f"Deleted: {image_path}")
        except FileNotFoundError:
            print(f"File not found: {image_path}")
        except PermissionError:
            print(f"Permission denied: {image_path}")
        except Exception as e:
            print(f"Error deleting {image_path}: {e}")
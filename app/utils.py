import os

def get_image_files(folder_path):
    return [f for f in os.listdir(folder_path) if f.lower().endswith((".png", ".jpg", ".jpeg", ".pdf"))]
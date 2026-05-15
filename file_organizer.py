import os
import shutil

# --- SETTINGS ---
# Change this to the folder you want to organize
FOLDER_TO_ORGANIZE = "C:/Users/rogha/Downloads"  # Change this path

# File type categories
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".wmv"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp"],
    "Others": []
}

def get_category(extension):
    for category, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return category
    return "Others"

def organize_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return

    files_moved = 0

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Skip folders
        if os.path.isdir(file_path):
            continue

        # Get file extension and category
        _, extension = os.path.splitext(filename)
        category = get_category(extension)

        # Create category folder if it doesn't exist
        category_folder = os.path.join(folder_path, category)
        os.makedirs(category_folder, exist_ok=True)

        # Move file
        destination = os.path.join(category_folder, filename)
        shutil.move(file_path, destination)
        print(f"✅ Moved: {filename} → {category}/")
        files_moved += 1

    print(f"\n🎉 Done! {files_moved} files organized successfully.")

# --- RUN ---
organize_folder(FOLDER_TO_ORGANIZE)
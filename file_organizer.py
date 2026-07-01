import os
import shutil
import argparse
import logging

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


def get_category(extension, file_types=FILE_TYPES):
    """Return the category name for a given file extension."""
    for category, extensions in file_types.items():
        if extension.lower() in extensions:
            return category
    return "Others"


def get_unique_destination(destination):
    """If destination already exists, append (1), (2), etc. to avoid overwriting."""
    if not os.path.exists(destination):
        return destination

    base, ext = os.path.splitext(destination)
    counter = 1
    new_destination = f"{base} ({counter}){ext}"
    while os.path.exists(new_destination):
        counter += 1
        new_destination = f"{base} ({counter}){ext}"
    return new_destination


def setup_logger(folder_path):
    """Configure logging to write moves to log.txt inside the target folder."""
    log_path = os.path.join(folder_path, "log.txt")
    logger = logging.getLogger("file_organizer")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    logger.addHandler(file_handler)

    return logger


def organize_folder(folder_path, dry_run=False, logger=None):
    """
    Scan folder_path and move files into category subfolders.
    If dry_run=True, only print/log what would happen without moving anything.
    Returns the number of files (that were or would be) moved.
    """
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return 0

    files_moved = 0

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Skip folders and the log file itself
        if os.path.isdir(file_path) or filename == "log.txt":
            continue

        _, extension = os.path.splitext(filename)
        category = get_category(extension)
        category_folder = os.path.join(folder_path, category)
        destination = os.path.join(category_folder, filename)

        try:
            destination = get_unique_destination(destination)

            if dry_run:
                print(f"[DRY RUN] Would move: {filename} -> {category}/{os.path.basename(destination)}")
                if logger:
                    logger.info(f"[DRY RUN] Would move: {filename} -> {category}/{os.path.basename(destination)}")
            else:
                os.makedirs(category_folder, exist_ok=True)
                shutil.move(file_path, destination)
                print(f"Moved: {filename} -> {category}/{os.path.basename(destination)}")
                if logger:
                    logger.info(f"Moved: {filename} -> {category}/{os.path.basename(destination)}")

            files_moved += 1

        except PermissionError:
            print(f"Skipped (permission denied): {filename}")
            if logger:
                logger.info(f"Skipped (permission denied): {filename}")
        except OSError as e:
            print(f"Skipped (error: {e}): {filename}")
            if logger:
                logger.info(f"Skipped (error: {e}): {filename}")

    action = "would be organized" if dry_run else "organized successfully"
    print(f"\nDone! {files_moved} files {action}.")
    return files_moved


def parse_args():
    parser = argparse.ArgumentParser(
        description="Organize files in a folder into subfolders by file type."
    )
    parser.add_argument(
        "--path", required=True,
        help="Path to the folder you want to organize"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview what would be moved without actually moving any files"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    log = setup_logger(args.path) if os.path.exists(args.path) else None
    organize_folder(args.path, dry_run=args.dry_run, logger=log)

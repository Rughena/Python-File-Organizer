# Python File Organizer 📁

A CLI tool that automatically organizes files in a folder into subfolders by file type — with dry-run preview, duplicate-safe renaming, and an activity log.

## Features
- **Sorts files by type** into subfolders (Images, Videos, Documents, Audio, Archives, Code, Others)
- **Dry-run mode** — preview exactly what would move before touching any files
- **Duplicate-safe** — never overwrites existing files; renames conflicts as `file (1).ext`
- **Activity logging** — every move is recorded with a timestamp in `log.txt`
- **Error handling** — gracefully skips files it can't access (permissions, in-use files) instead of crashing
- **CLI arguments** — point it at any folder, no editing the script required

## Tech Stack
- **Python** — scripting
- **os / shutil** — file system operations
- **argparse** — command-line interface
- **logging** — activity tracking
- **pytest** — unit testing (9 tests covering categorization, duplicate handling, dry-run, and error cases)

## Usage

1. Clone the repository
   ```bash
   git clone https://github.com/Rughena/Python-File-Organizer.git
   cd Python-File-Organizer
   ```

2. Preview what will happen (recommended first run)
   ```bash
   python file_organizer.py --path "C:/Users/you/Downloads" --dry-run
   ```

3. Run it for real
   ```bash
   python file_organizer.py --path "C:/Users/you/Downloads"
   ```

4. Check `log.txt` inside the organized folder for a full record of what moved where.

## Running Tests

```bash
pip install pytest
python -m pytest test_file_organizer.py -v
```

All 9 tests should pass, covering:
- File categorization by extension (including case-insensitivity)
- Duplicate filename handling
- Dry-run mode (no files actually moved)
- Missing folder handling

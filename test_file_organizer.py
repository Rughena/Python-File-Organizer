import os
import pytest
from file_organizer import get_category, get_unique_destination, organize_folder, FILE_TYPES


def test_get_category_known_extension():
    assert get_category(".jpg") == "Images"
    assert get_category(".mp3") == "Audio"
    assert get_category(".py") == "Code"


def test_get_category_case_insensitive():
    assert get_category(".JPG") == "Images"
    assert get_category(".PDF") == "Documents"


def test_get_category_unknown_extension():
    assert get_category(".xyz") == "Others"


def test_get_unique_destination_no_conflict(tmp_path):
    destination = tmp_path / "file.txt"
    result = get_unique_destination(str(destination))
    assert result == str(destination)


def test_get_unique_destination_with_conflict(tmp_path):
    existing = tmp_path / "file.txt"
    existing.write_text("existing content")

    result = get_unique_destination(str(existing))
    assert result != str(existing)
    assert "(1)" in result


def test_organize_folder_moves_files_by_type(tmp_path):
    (tmp_path / "photo.jpg").write_text("fake image")
    (tmp_path / "notes.txt").write_text("fake doc")

    files_moved = organize_folder(str(tmp_path))

    assert files_moved == 2
    assert (tmp_path / "Images" / "photo.jpg").exists()
    assert (tmp_path / "Documents" / "notes.txt").exists()


def test_organize_folder_dry_run_does_not_move_files(tmp_path):
    (tmp_path / "photo.jpg").write_text("fake image")

    files_moved = organize_folder(str(tmp_path), dry_run=True)

    assert files_moved == 1
    # File should still be in the original location, untouched
    assert (tmp_path / "photo.jpg").exists()
    assert not (tmp_path / "Images").exists()


def test_organize_folder_handles_duplicate_filenames(tmp_path):
    (tmp_path / "Images").mkdir()
    (tmp_path / "Images" / "photo.jpg").write_text("old image")
    (tmp_path / "photo.jpg").write_text("new image")

    organize_folder(str(tmp_path))

    # Original should be preserved, new file renamed instead of overwritten
    assert (tmp_path / "Images" / "photo.jpg").read_text() == "old image"
    assert (tmp_path / "Images" / "photo (1).jpg").exists()


def test_organize_folder_missing_folder_returns_zero(tmp_path):
    missing = tmp_path / "does_not_exist"
    files_moved = organize_folder(str(missing))
    assert files_moved == 0

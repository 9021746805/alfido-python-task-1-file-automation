
import shutil
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent

# Default source and destination folders
SOURCE_FOLDER = BASE_DIR / "sample_files"
DESTINATION_FOLDER = BASE_DIR / "organized_files"

# File extension categories
FILE_CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Python_Files": [".py"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".7z"]
}


def get_category(file_extension):

    for category, extensions in FILE_CATEGORIES.items():
        if file_extension.lower() in extensions:
            return category

    return "Others"


def get_unique_path(destination):

    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = (
            f"{destination.stem}_{counter}"
            f"{destination.suffix}"
        )

        new_path = destination.with_name(new_name)

        if not new_path.exists():
            return new_path

        counter += 1


def organize_files(source, destination):

    try:
        source = Path(source).resolve()
        destination = Path(destination).resolve()

        # Validate source folder
        if not source.exists():
            print("Error: Source folder does not exist.")
            return

        if not source.is_dir():
            print("Error: Source path is not a directory.")
            return

        # Prevent organizing a folder into itself
        if source == destination:
            print("Error: Source and destination cannot be the same.")
            return

        if source in destination.parents:
            print("Error: Destination cannot be inside source folder.")
            return

        destination.mkdir(parents=True, exist_ok=True)

        total_files = 0
        moved_files = 0
        failed_files = 0

        print("\nStarting File Organization...\n")

        # Scan files in source directory
        for file_path in source.iterdir():

            if not file_path.is_file():
                continue

            total_files += 1

            try:
                extension = file_path.suffix.lower()
                category = get_category(extension)

                # Create category folder
                category_folder = destination / category
                category_folder.mkdir(
                    parents=True,
                    exist_ok=True
                )

                # Avoid overwriting existing files
                target_path = get_unique_path(
                    category_folder / file_path.name
                )

                # Move file
                shutil.move(
                    str(file_path),
                    str(target_path)
                )

                moved_files += 1

                print(
                    f"Moved: {file_path.name} "
                    f"-> {category}/{target_path.name}"
                )

            except PermissionError:
                failed_files += 1
                print(f"Permission denied: {file_path.name}")

            except (OSError, shutil.Error) as error:
                failed_files += 1
                print(f"Failed: {file_path.name} - {error}")

        # Display final report

        print(f"Total files scanned : {total_files}")
        print(f"Files moved         : {moved_files}")
        print(f"Files failed        : {failed_files}")
    

    except PermissionError:
        print("Error: Permission denied while accessing folders.")

    except OSError as error:
        print(f"System error: {error}")

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    organize_files(
        SOURCE_FOLDER,
        DESTINATION_FOLDER
    )


import argparse
import sys
import zipfile
from pathlib import Path, PurePosixPath, PureWindowsPath


def is_safe_member(member_name, destination):
    """Reject archive entries that can escape the destination directory."""
    if not member_name or "\x00" in member_name:
        return False

    posix_path = PurePosixPath(member_name)
    windows_path = PureWindowsPath(member_name)

    if posix_path.is_absolute() or windows_path.is_absolute():
        return False

    if windows_path.drive or ".." in posix_path.parts:
        return False

    destination = destination.resolve()
    target = (destination / Path(*posix_path.parts)).resolve()

    try:
        target.relative_to(destination)
    except ValueError:
        return False

    return True


def extract_zip(zip_path):
    """Validate and safely extract a ZIP archive into a sibling folder."""
    archive_path = Path(zip_path).expanduser()

    if not archive_path.exists():
        print(f"Error: File not found: {archive_path}", file=sys.stderr)
        return 1

    if not archive_path.is_file():
        print(f"Error: Not a regular file: {archive_path}", file=sys.stderr)
        return 1

    if archive_path.suffix.lower() != ".zip":
        print("Error: The input file must have a .zip extension.", file=sys.stderr)
        return 1

    destination = archive_path.parent / archive_path.stem

    try:
        with zipfile.ZipFile(archive_path, "r") as archive:
            bad_member = archive.testzip()

            if bad_member is not None:
                print(
                    f"Error: Corrupted ZIP member: {bad_member}",
                    file=sys.stderr,
                )
                return 1

            members = archive.infolist()

            if not members:
                print("The ZIP archive is empty.")
                return 0

            for member in members:
                if not is_safe_member(member.filename, destination):
                    print(
                        f"Error: Unsafe path in archive: {member.filename}",
                        file=sys.stderr,
                    )
                    return 1

            destination.mkdir(parents=True, exist_ok=True)
            archive.extractall(destination)

    except zipfile.BadZipFile:
        print("Error: The file is not a valid ZIP archive.", file=sys.stderr)
        return 1
    except (OSError, RuntimeError, NotImplementedError) as error:
        print(f"Error extracting archive: {error}", file=sys.stderr)
        return 1

    print(f"Extracted successfully to: {destination}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Safely extract a ZIP archive into a folder."
    )
    parser.add_argument(
        "-l",
        "--zippedfile",
        required=True,
        help="Path to the ZIP file to extract",
    )

    args = parser.parse_args()
    return extract_zip(args.zippedfile)


if __name__ == "__main__":
    raise SystemExit(main())

import argparse
import os


def create_index_file(target_file_path, index_file_path):
    """
    Create an index file for the target file.
    Each line in the index file contains the byte offset of the corresponding line in the target file.

    :param target_file_path: Path to the target file.
    :param index_file_path: Path to the index file to create.
    """
    with (
        open(target_file_path, "r") as target_file,
        open(index_file_path, "w") as index_file,
    ):
        offset = 0
        lines_count = 0
        for line in target_file:
            index_file.write(f"{offset:012d}\n")
            offset += len(line)
            lines_count += 1
    print(f"Total lines indexed: {lines_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create an index file for a given target file"
    )
    parser.add_argument("target_file", help="Path to the target file")
    args = parser.parse_args()

    target_file_path = args.target_file
    index_file_path = f"{target_file_path}_index.txt"

    if not os.path.exists(target_file_path):
        print(f"Error: Target file '{target_file_path}' does not exist.")
        exit(1)

    create_index_file(target_file_path, index_file_path)

    print(
        f"Index file '{index_file_path}' has been created for '{target_file_path}'."
    )

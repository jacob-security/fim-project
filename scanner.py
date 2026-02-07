import os
from hasher import calculate_sha256

def scan(target_path: str) -> list[tuple]:
    file_list = []

    # convert target path to its absolute path for consistency
    abs_target = os.path.abspath(target_path)

    # append single hash and file
    if os.path.isfile(abs_target):
        result = hash_file(abs_target)
        # only append if successfully hashed
        if result:
            file_list.append((result, abs_target))
    
    # append entire directory recursively walked
    elif os.path.isdir(abs_target):
        for root, dirs, files in os.walk(abs_target):
            for filename in files:
                full_path = os.path.join(root, filename)

                # add error handling for restricted files
                try:
                    sha_sum = calculate_sha256(full_path)
                    # check file actually hashed
                    if sha_sum:
                        file_list.append((sha_sum, full_path))
                except (PermissionError, OSError) as e:
                    print(f"Skipping {full_path}: {e}")

    return file_list

def hash_file(target_path: str) -> tuple:
    try:
        if os.path.isfile(target_path):
            return (calculate_sha256(target_path), target_path)
    except Exception as e:
        print(f"Error hashing file: {e}")
    return None

def main():
    filepath = "/home/jacob/CS/fim/test_directory"
    hashes = scan(filepath)
    for field in hashes:
        print(field)

if __name__ == "__main__":
    main()

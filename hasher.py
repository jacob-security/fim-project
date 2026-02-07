import hashlib

def calculate_sha256(filepath: str) -> str:
    sha256_hash = hashlib.sha256()

    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
    
        return sha256_hash.hexdigest()
    except (PermissionError, OSError) as e:
        print(f"Error opening {filepath}: {e}\n")
    return None

def main():
    filepath = "/home/jacob/CS/fim/test"
    print(calculate_sha256(filepath))

if __name__ == "__main__":
    main()

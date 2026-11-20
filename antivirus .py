import os
import hashlib
from pathlib import Path

print("=== ULTRA-SIMPLE BASIC ANTIVIRUS SIMULATION ===")

# 1. Define known threat signature (EICAR test file hash)
EICAR_HASH = "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f"
MALICIOUS_HASHES = [EICAR_HASH]

# 2. Automatically create a test folder with a clean file and an EICAR test file
test_dir = Path("my_test_folder")
test_dir.mkdir(exist_ok=True)

# Create a normal clean file
(test_dir / "my_notes.txt").write_text("Hello, this is a clean file.", encoding="utf-8")

# Create the harmless 68-byte EICAR test file
eicar_string = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
(test_dir / "virus_test.txt").write_text(eicar_string, encoding="ascii")

print(f"[*] Created test folder: '{test_dir}' with clean and test files.\n")

# 3. Create the quarantine folder
quarantine_dir = Path("quarantine_folder")
quarantine_dir.mkdir(exist_ok=True)

# 4. Scan files in the folder one by one
for file_path in test_dir.iterdir():
    if file_path.is_file():
        # Read file and compute SHA-256 hash
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            hasher.update(f.read())
        file_hash = hasher.hexdigest()

        print(f"Scanning: {file_path.name}")
        print(f"  -> Hash: {file_hash}")

        # Check if hash matches our list
        if file_hash in MALICIOUS_HASHES:
            print("  -> [!] THREAT FOUND: Matches EICAR Test Signature!")
            # Move file to quarantine folder
            destination = quarantine_dir / file_path.name
            file_path.rename(destination)
            print(f"  -> [x] Action: Moved to '{destination}'\n")
        else:
            print("  -> [+] Status: CLEAN\n")

print("=== SCAN FINISHED ===")

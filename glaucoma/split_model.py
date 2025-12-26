import os

def split_file(file_path, chunk_size=60 * 1024 * 1024): # 60MB chunks
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    part_num = 0
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            part_name = f"{file_path}.{part_num:03d}"
            with open(part_name, 'wb') as chunk_file:
                chunk_file.write(chunk)
            print(f"Created chunk: {part_name}")
            part_num += 1
    
    print("Splitting complete.")
    # Verify
    print("Verifying chunks...")
    reconstructed_data = b''
    for i in range(part_num):
        part_name = f"{file_path}.{i:03d}"
        with open(part_name, 'rb') as pf:
            reconstructed_data += pf.read()
    
    original_size = os.path.getsize(file_path)
    if len(reconstructed_data) == original_size:
        print("Verification SUCCESS: Reconstructed data matches original size.")
    else:
        print("Verification FAILED.")

if __name__ == '__main__':
    split_file('model.tflite')

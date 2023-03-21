import os
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from PIL import Image

def clean_folders():
    for path in (Path('thread'), Path('multiprocess')):
        for file in path.glob('*.jpeg'):
            file.unlink()

def resize_image(filename, destination):
    with Image.open(filename) as img:
        width, height = img.size
        resized_img = img.resize((width // 2, height // 2))

        new_filename = Path(filename).stem + "_resized.jpeg"
        resized_img.save(destination / new_filename, "jpeg", quality=50)

def resize_images_thread():
    files = [entry.path for entry in os.scandir() if entry.name.endswith('.jpeg')]

    with ThreadPoolExecutor() as executor:
        executor.map(resize_image, files, [Path('thread')] * len(files))

def resize_images_multiprocess():
    files = [entry.path for entry in os.scandir() if entry.name.endswith('.jpeg')]

    with ProcessPoolExecutor() as executor:
        executor.map(resize_image, files, [Path('multiprocess')] * len(files))

if __name__ == "__main__":
    clean_folders()

    start = time.time()
    resize_images_thread()
    end = time.time()
    print("Time taken for thread: ", end - start)

    start = time.time()
    resize_images_multiprocess()
    end = time.time()
    print("Time taken for multiprocess: ", end - start)
    
# I don't know why multiprocess in this case is still faster than threading
# I/O-bound tasks, such as reading and writing images from/to disk, 
# take up most of the program's time. This causes the program to wait for 
# input/output operations to complete, instead of performing computationally intensive tasks. 
# In this case, a threading-based implementation may be faster than a multiprocessing-based 
# implementation as threads can release the Global Interpreter Lock (GIL) 
# while waiting for I/O operations to complete. This allows other threads to execute in the meantime. 
# Multiprocessing requires the overhead of creating separate processes.
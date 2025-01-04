from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Fill in blanks
# Source directory e.g. MacOS: "/Users/Username/Downloads"
# Source directory e.g. Windows: "C:\\Users\\Username\\Downloads"
source_dir = ""
destination_dir_music = ""
destination_dir_video = ""
destination_dir_image = ""
destination_dir_documents = ""
destination_dir_editing = ""
destination_dir_programming = ""

#image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

#video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

#audio types
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]

#document types
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

#editing type
editing_extensions = [".psd", ".veg", ".prproj", ".aep", ".drp", ".ai", ".eps", ".cdr", ".psb", ".abr", ".pat", ".atn"]

#programming types
programming_extensions = [".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".hxx", ".hh", ".cs", ".java", ".py", ".pyc", ".pyo", 
                          ".pyw", ".pyz", ".rb", ".erb", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".go", ".swift", ".kt", ".kts", ".rs", ".pl", 
                          ".pm", ".t", ".php", ".phtml", ".php3", ".php4", ".php5", ".phps", ".html", ".htm", ".css", ".scss", ".sass", ".less", ".xml", ".xsl"]


def makeUnique(destination, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{destination}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def fileMove(destination, entry, name):
    if exists(f"{destination}/{name}"):
        unique_name = makeUnique(destination, name)
        oldName = join(destination, name)
        newName = join(destination, unique_name)
        rename(oldName, newName)
    move(entry, destination)


class Mover(FileSystemEventHandler):
    # function runs when there's a change detected in source_dir
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)
                self.check_editing_files(entry, name)
                self.check_programming_files(entry, name)

    def check_audio_files(self, entry, name):  # * Checks all Audio Files
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                destination = destination_dir_music
                fileMove(destination, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                fileMove(destination_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  # * Checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                fileMove(destination_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):  # * Checks all Document Files
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                fileMove(destination_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_editing_files(self, entry, name): # * Checks all Editing files
        for editing_extension in editing_extensions:
            if name.endswith(editing_extension) or name.endswith(editing_extension.upper()):
                fileMove(destination_dir_editing, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_programming_files(self, entry, name): # * Checks all Programming files
        for programming_extension in programming_extensions:
            if name.endswith(programming_extension) or name.endswith(programming_extension.upper()):
                fileMove(destination_dir_programming, entry, name)
                logging.info(f"Moved document file: {name}")

# No changes necessary to code below
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = Mover()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
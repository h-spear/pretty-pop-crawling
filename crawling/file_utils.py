import os


class FileUtils:
    img_exts = ["jpg", "png", "JPEG", "GIF"]

    def exist_img_file(file_path):
        for ext in FileUtils.img_exts:
            if os.path.isfile(file_path + "." + ext):
                return True
        return False

    def create_directory(directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print("Error: Failed to create the directory.")

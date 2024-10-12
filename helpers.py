import os, time


def clear_target_path(provided_path):
    path = os.getcwd()

    if not provided_path:
        print(f"The path is not provided.")
    else:
        if not os.path.exists(provided_path):
            print(f"Error: The specified path does not exist: {provided_path}.")

        elif not os.path.isdir(provided_path):
            print(f"Error: The specified path is not a directory: {provided_path}.")
        else:
            path = provided_path

    print(f"The download directory is set to: {path}")

    return path


def get_tmp_download_location():
    project_root = os.path.abspath(os.path.dirname(__file__))
    tmp_folder = os.path.join(project_root, "tmp")

    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)

    return tmp_folder


def remove_old_tmp_files():
    now = time.time()
    max_file_age = 2 * 24 * 60 * 60  # 2 days in seconds
    tmp_folder = get_tmp_download_location()

    for filename in os.listdir(tmp_folder):
        file_path = os.path.join(tmp_folder, filename)

        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)

            if file_age > max_file_age:
                try:
                    os.remove(file_path)
                    print(f"Deleted tmp file: {file_path}")
                except Exception as e:
                    print(f"Failed to delete tmp file: {file_path}: {e}")

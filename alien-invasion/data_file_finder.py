import sys
import os


def find_data_file(file_name, file_type):
    if getattr(sys, "frozen", False):
        # when the application is frozen.
        data_dir = os.path.dirname(sys.executable)
    else:
        # when the application is not frozen.
        data_dir = os.path.dirname(__file__)
        data_dir += f"/assets/{file_type}/"
        print(os.path.join(data_dir, file_name))

    return os.path.join(data_dir, file_name)

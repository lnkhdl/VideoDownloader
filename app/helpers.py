import os

def get_target_path(provided_path):
    if not provided_path:
        path = os.getcwd()
        print(f"The path is not provided, using the current directory: {path}")
    else:
        if not os.path.exists(provided_path):
            print(f"Error: The specified path does not exist: {provided_path}")
            path = os.getcwd()
            
        elif not os.path.isdir(provided_path):
            print(f"Error: The specified path is not a directory: {provided_path}")
            path = os.getcwd()
        else:
            path = provided_path
    
    return path
import os

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

import os

def update_outjob_file(original_file_name, new_project_name, destination_file_name):
    """
    Updates an .OutJob file with a new project name, replaces a specific path with the script's current directory path,
    then saves the updated content to a new file.

    :param original_file_name: Name of the original .OutJob file.
    :param new_project_name: New project name to replace occurrences of "neural_reactor".
    :param destination_file_name: Name for the updated file to be saved.
    """
    current_directory = os.getcwd()  # Get the current working directory of the script
    try:
        with open(original_file_name, 'r', encoding='utf-8') as file:
            content = file.read()

        # Replace "neural_reactor" with the new project name
        content = content.replace("neural_reactor", new_project_name)

        # Replace "C:\git_projects\" with the current directory path
        content = content.replace("C:\\git_projects\\", current_directory + "\\")

        # Write the updated content to a new file
        with open(destination_file_name, 'w', encoding='utf-8') as new_file:
            new_file.write(content)

        print(f"File '{destination_file_name}' has been updated and saved in {current_directory}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Remember to replace 'original_file_name' and 'new_project_name' with the actual values when calling the function.
        
update_outjob_file("neural_reactor_documentation.OutJob", "test_project", 'output_job_file/output_job_usb_c_panel_rev1/usb_c_panel_documentation.OutJob')
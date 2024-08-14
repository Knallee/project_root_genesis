import os

def create_folders(base_path, structure, project_name):
    """
    Recursively creates folders and subfolders, replacing placeholders with the project name where specified.

    :param base_path: The base path where the folders will be created.
    :param structure: A nested dictionary where each key is a folder name and its value is the subfolder structure.
    :param project_name: The name of the project, used to replace placeholders.
    """
    for folder, substructure in structure.items():
        # Replace placeholder with the project name and "rev1" if present
        if "{{PROJECT_NAME}}" in folder:
            folder = folder.replace("{{PROJECT_NAME}}", project_name) + "_rev1"
        path = os.path.join(base_path, folder)
        os.makedirs(path, exist_ok=True)
        if isinstance(substructure, dict):  # Check if the folder has subfolders
            create_folders(path, substructure, project_name)  # Recursive call with the project name


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



# Step 1: Determine the script's current directory, assumed to be the project root
project_root = os.getcwd()
project_name = os.path.basename(project_root)

# Step 2: Define your desired complex folder structure with nested subfolders
folder_structure = {
    "schematics": {},
    "layout":{},
    "output_job_file":{
        "output_job_"+"{{PROJECT_NAME}}":{},
    },
    "draftsman_document":{},
    "rules_and_stackup":{},
    "production_data":{
        "{{PROJECT_NAME}}": {
            "fabrication_files":{
                "pcb":{},
                "panel":{},
                "pick&place":{},
            },
            "assembly_drawings":{},
            "pcb_datasheet":{},
            "schematic_pdf":{},
            "layout_pdf":{},
            "eq":{},
            "po_and_qoutation":{},
            "3d_model":{},
            "bill_of_material":{},
        },
    },
}

# Step 3: Use the recursive function to create the folders and subfolders, replacing placeholders
create_folders(project_root, folder_structure, project_name)


update_outjob_file("neural_reactor_documentation.OutJob", project_name, "output_job_file/output_job_" + project_name + "_rev1/" + project_name + "_documentation.OutJob")
update_outjob_file("neural_reactor_gerber_drill.OutJob", project_name, "output_job_file/output_job_" + project_name + "_rev1/" + project_name + "_gerber_drill.OutJob")

# Step 4: Create a .gitignore file
gitignore_content = """*.PrjPcbStructure
*.SchDoc
*.PcbDoc
*.PrjPCB
*.PcbLib
*.SchLib
*.IntLib
*.DsnWrk
*.OutJob
# Add other patterns to ignore
"""

with open(os.path.join(project_root, ".gitignore"), "w") as gitignore_file:
    gitignore_file.write(gitignore_content)


print(f"Project '{project_name}' setup complete with dynamic folder naming.")
print(f"Project directory is '{project_root}")

print(project_root + "____jej")
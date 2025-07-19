import os
import shutil

def create_folders(base_path, structure, project_name):
    """
    Recursively creates folders and subfolders, replacing placeholders with the project name where specified.

    :param base_path: The base path where the folders will be created.
    :param structure: A nested dictionary where each key is a folder name and its value is the subfolder structure.
    :param project_name: The name of the project, used to replace placeholders.
    """
    for folder, substructure in structure.items():
        if "{{PROJECT_NAME}}" in folder:
            folder = folder.replace("{{PROJECT_NAME}}", project_name)
        path = os.path.join(base_path, folder)
        os.makedirs(path, exist_ok=True)
        if isinstance(substructure, dict):
            create_folders(path, substructure, project_name)

def update_outjob_file(template_filename, project_name, destination_path):
    """
    Updates an .OutJob file with a new project name, replaces a specific path with the script's current directory path,
    then saves the updated content to a new file.
    """
    current_directory = os.getcwd()

    try:
        with open(template_filename, 'r', encoding='utf-8') as file:
            content = file.read()
        content = content.replace("neural_reactor", project_name)
        content = content.replace("C:\\git_projects\\", current_directory + "\\")
        with open(destination_path, 'w', encoding='utf-8') as new_file:
            new_file.write(content)
        print(f"File '{destination_path}' has been updated and saved in {current_directory}.")
    
        # Remove original template file
        os.remove(template_filename)
        print(f"Original template '{template_filename}' has been removed.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def populate_folders(project_root, project_name):
    """
    Moves and renames core project files, then injects them into the .PrjPcb file as [DocumentX] entries.
    """
    source_folder = os.path.join(project_root, "project_files")
    file_moves = {
        "neural_reactor.PcbDoc": os.path.join("layout", f"{project_name}.PcbDoc"),
        "neural_reactor.SchDoc": os.path.join("schematics", f"{project_name}.SchDoc"),
        "neural_reactor_assembly.PCBDwf": os.path.join("draftsman_document", f"{project_name}_assembly.PCBDwf"),
        "neural_reactor_layers.PCBDwf": os.path.join("draftsman_document", f"{project_name}_layers.PCBDwf"),
    }

    for src_name, dest_relative in file_moves.items():
        src_path = os.path.join(source_folder, src_name)
        if not os.path.exists(src_path):
            print(f"Warning: {src_name} not found in {source_folder}")
            continue
        dest_path = os.path.join(project_root, dest_relative)
        try:
            shutil.move(src_path, dest_path)
            print(f"Moved: {src_name} -> {dest_relative}")
        except Exception as e:
            print(f"Failed to move {src_name}: {e}")

    prjpcb_files = [f for f in os.listdir(project_root) if f.lower().endswith(".prjpcb")]
    if prjpcb_files:
        prjpcb_path = os.path.join(project_root, prjpcb_files[0])
        with open(prjpcb_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        doc_insert_index = 50 if len(lines) > 50 else len(lines)
        document_entries = [
            ("schematics", f"{project_name}.SchDoc", "OQVOPOFY"),
            ("layout", f"{project_name}.PcbDoc", "DSKQCGXM"),
            ("output_job_file", f"{project_name}_documentation.OutJob", ""),
            ("output_job_file", f"{project_name}_gerber_drill.OutJob", ""),
            ("draftsman_document", f"{project_name}_assembly.PCBDwf", "VOYHFPJL"),
            ("draftsman_document", f"{project_name}_layers.PCBDwf", "JKABZEPW")
        ]

        document_template = ""
        for i, (folder, filename, doc_id) in enumerate(document_entries, 1):
            document_template += f"[Document{i}]\n"
            document_template += f"DocumentPath={folder}\\{filename}\n"
            document_template += "AnnotationEnabled=1\n"
            document_template += "AnnotateStartValue=1\n"
            document_template += "AnnotationIndexControlEnabled=0\n"
            document_template += "AnnotateSuffix=\n"
            document_template += "AnnotateScope=All\n"
            document_template += "AnnotateOrder=-1\n"
            document_template += "DoLibraryUpdate=1\n"
            document_template += "DoDatabaseUpdate=1\n"
            document_template += "ClassGenCCAutoEnabled=1\n"
            document_template += "ClassGenCCAutoRoomEnabled=0\n"
            document_template += "ClassGenNCAutoScope=None\n"
            document_template += "DItemRevisionGUID=\n"
            document_template += "GenerateClassCluster=0\n"
            document_template += f"DocumentUniqueId={doc_id}\n\n"

        document_template = document_template.strip()
        lines = lines[:doc_insert_index] + document_template.strip().splitlines(keepends=True) + lines[doc_insert_index:]
        with open(prjpcb_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    # Remove project_files dir
    if os.path.isdir(source_folder):
        try:
            shutil.rmtree(source_folder)
            print(f"Removed folder: {source_folder}")
        except Exception as e:
            print(f"Failed to remove 'project_files' folder: {e}")
    

def add_project_parameters():
    """
    Adds predefined project parameters to an Altium .PrjPcb file before the [Configuration1] block.
    Automatically detects the .PrjPcb file in the current directory.
    Prompts the user for values where needed.
    """
    prjpcb_files = [f for f in os.listdir(os.getcwd()) if f.lower().endswith(".prjpcb")]
    if not prjpcb_files:
        print("No .PrjPcb file found in the current directory. Skipping parameter insertion.")
        return
    prjpcb_filename = prjpcb_files[0]
    print(f"Detected .PrjPcb file: {prjpcb_filename}")
    prjpcb_path = os.path.join(os.getcwd(), prjpcb_filename)
    
    drawn_by = input("Who is the designer?")
    project_name = input("Enter Project Name: ")

    parameters = [
        ("ItemName", project_name),
        ("ProjectTitle", project_name),
        ("PartNumber", input("Enter Part Number: ")),
        ("LayoutRevision",
            input("Enter Layout Revision (Default: 1.0.0): ") or "1.0.0"),
        ("SchematicRevision",
            input("Enter Schematic Revision (Default: 1.0.0): ") or "1.0.0"),
        ("BomRevision",
            input("Enter BOM Revision (Default: 1.0.0): ") or "1.0.0"),
        ("ApprovedBy", "N/A"),
        ("SchematicReviewer", "N/A"),
        ("LayoutReviewer", "N/A"),
        ("DrawnBy", drawn_by),
    ]

    with open(prjpcb_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    insert_index = next((i for i, line in enumerate(lines) if line.strip() == "[Configuration1]"), len(lines))
    existing_count = sum(1 for line in lines if line.strip().startswith("[Parameter"))
    next_index = existing_count + 1

    new_lines = []
    for name, value in parameters:
        new_lines.append(f"[Parameter{next_index}]\n")
        new_lines.append(f"Name={name}\n")
        new_lines.append(f"Value={value}\n\n")
        next_index += 1

    updated_lines = lines[:insert_index] + new_lines + lines[insert_index:]
    with open(prjpcb_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

    print(f"Added {len(parameters)} parameters to {prjpcb_filename}.")

# ---- Main Project Setup ----
def main():
    project_root = os.getcwd()
    project_name = os.path.basename(project_root)

    folder_structure = {
        "schematics": {},
        "layout": {},
        "bom_document": {},
        "output_job_file": {},
        "draftsman_document": {},
        "rules_and_stackup": {},
        "production_data": {
            "{{PROJECT_NAME}}": {
                "fabrication_files": {
                    "pcb": {},
                    "panel": {},
                },
                "fabrication_and_assembly": {},
                "schematic_pdf": {},
                "eq": {},
                "po_and_qoutation": {},
                "3d_model": {},
                "bill_of_material": {},
            },
        },
    }

    print("Creating project folders...")
    create_folders(project_root, folder_structure, project_name)

    outjob_templates = [
        "documentation.OutJob",
        "gerber_drill.OutJob"
        ]

    print("Updating .OutJob files...")
    for template in outjob_templates:
        dest_path = os.path.join("output_job_file", f"{project_name}_{template}")
        update_outjob_file(template, project_name, dest_path)

    
    populate_folders(project_root, project_name)

    print("Adding project parameters to .PrjPcb...")
    add_project_parameters()

    print(f"Project '{project_name}' setup complete with dynamic folder naming.")
    print(f"Project directory is '{project_root}'")

if __name__ == "__main__":
    main()

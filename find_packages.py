import os
import re
from collections import Counter

def find_imports_in_file(file_path):
    """
    Extract all imported modules from a Python file.
    """
    imports = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            # Match imports like `import module` or `from module import ...`
            match = re.match(r"^\s*(?:import|from)\s+([\w.]+)", line)
            if match:
                imports.append(match.group(1).split(".")[0])  # Extract base module
    return imports

def find_imports_in_project(root_dir):
    """
    Traverse the project directory and find all imported modules.
    """
    all_imports = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):  # Only process Python files
                file_path = os.path.join(root, file)
                try:
                    all_imports.extend(find_imports_in_file(file_path))
                except Exception as e:
                    print(f"Could not process {file_path}: {e}")
    return all_imports

def save_requirements(imports, output_file="Project-requirements.txt"):
    """
    Save the unique imported modules to a requirements.txt file.
    """
    with open(output_file, "w") as file:
        for module in sorted(imports):
            file.write(f"{module}\n")
    print(f"Requirements saved to {output_file}")

if __name__ == "__main__":
    # Set the project directory path
    project_dir = input("Enter the project directory path: ").strip()
    
    if not os.path.isdir(project_dir):
        print("Invalid directory path!")
    else:
        print("Scanning for imported modules...")
        imports = find_imports_in_project(project_dir)
        import_counts = Counter(imports)
        
        # Display and save the unique imports
        print("\nUnique Modules Found:")
        unique_imports = set(import_counts.keys())
        for module in unique_imports:
            print(module)
        
        save_requirements(unique_imports)

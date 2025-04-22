import subprocess
import os
import sys
import json  # Import the json module

def print_outdated_packages(outdated_packages):
    """Print the outdated packages in a formatted table."""
    print("\nOutdated Packages:")
    print("{:<40} {:<10} {:<10} {:<10}".format("Package", "Current", "Wanted", "Latest"))
    print("-" * 70)
    for package, details in outdated_packages.items():
        current_version = details.get("current", "N/A")
        wanted_version = details.get("wanted", "N/A")
        latest_version = details.get("latest", "N/A")
        print("{:<40} {:<10} {:<10} {:<10}".format(package, current_version, wanted_version, latest_version))
    print("-" * 70)

def get_outdated_packages(project_path):
    result = subprocess.run(['npm', 'outdated', '--json'], cwd=project_path, capture_output=True, text=True)
    if result.returncode != 0 and result.stderr:
        print("Error running npm outdated:", result.stderr)
        return {}
    
    try:
        outdated_packages = json.loads(result.stdout)  # Use json.loads instead of eval
        print_outdated_packages(outdated_packages)
    except Exception as e:
        print("Error parsing npm outdated output:", e)
        return {}
    
    return outdated_packages

def sanitize_json_output(output):
    """Sanitize JSON output to replace JavaScript-style values with Python-compatible values."""
    sanitized_output = output.replace("false", "false").replace("true", "true").replace("null", "null")
    return sanitized_output

def get_dependency_tree(project_path):
    """Fetch the dependency tree using npm ls."""
    try:
        result = subprocess.run(['npm', 'ls', '--json'], cwd=project_path, capture_output=True, text=True)
        sanitized_output = sanitize_json_output(result.stdout)
        dependency_tree = json.loads(sanitized_output)  # Use sanitized JSON output
    except Exception as e:
        print("Error parsing npm ls output:", e)
        return {}
    
    return dependency_tree

def resolve_update_order(outdated_packages, dependency_tree):
    """Determine the order of updates based on interdependencies among outdated packages."""
    resolved_order = []
    visited = set()

    def visit(package):
        if package in visited:
            return
        visited.add(package)
        dependencies = dependency_tree.get('dependencies', {}).get(package, {}).get('requires', {})
        for dep in dependencies:
            if dep in outdated_packages:  # Check if the dependency is also outdated
                visit(dep)
        resolved_order.append(package)

    for package in outdated_packages:
        visit(package)
    
    return resolved_order

def execute_script_if_exist(project_path, script_name="test"):
    """Check if the project has a script in package.json."""
    package_json_path = os.path.join(project_path, "package.json")
    if not os.path.isfile(package_json_path):
        return False
        
    try:
        with open(package_json_path, "r") as f:
            package_data = json.load(f)
        script_exists = script_name in package_data.get("scripts", {})
        returnCode = 0;
        if  script_exists:
            script_execute = subprocess.run(["npm", "run", script_name], cwd=project_path)
            returnCode = script_execute.returncode
        else :
            returnCode = 0
            print(f"No test script found in package.json. Skipping tests.returnCode: {returnCode}")
        return returnCode == 0
    except Exception as e:
        print(f"Error reading package.json: {e}")
        return False

def run_tests(project_path):
    print("\nRunning build...")
    resultBuild = execute_script_if_exist(project_path, "build")
    print("\nRunning tests...")
    resultTest = execute_script_if_exist(project_path, "test")
    if resultBuild == False or resultTest == False:
        raise Exception("Tests failed.")

def install_package(package, version, project_path):
    """Install a specific package version."""
    try:
        print(f"\nUpdating {package} to {version}...")
        subprocess.run(["npm", "install", f"{package}@{version}"], cwd=project_path, check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error installing {package}@{version}: {e}")
    return True

def install_package_and_run_tests(package, version, project_path):
    """Install a specific package version and run tests.""" 
    install_package(package, version, project_path)
    run_tests(project_path)
    print(f"{package} updated to version {version} successfully.")

def update_packages_in_order(outdated_packages, dependency_tree, project_path, safe_mode):   
    """Update packages in the resolved order."""
    update_order = resolve_update_order(outdated_packages, dependency_tree)
    print("\nUpdate Order:", update_order)
    
    failed_updates = []
    updated_packages = []

    for package in update_order:
        details = outdated_packages[package]
        current_version = details.get("current")
        wanted_version = details.get("wanted")
        latest_version = details.get("latest")
        final_version = current_version
        
        if safe_mode:
            print(f"\nTrying to update {package} to latest version {latest_version}...")
            try:
                install_package_and_run_tests(package, latest_version, project_path)
                final_version = latest_version
            except:
                print(f"Tests failed. Reverting to wanted version {wanted_version}...")
                try:
                    install_package_and_run_tests(package, wanted_version, project_path)
                    final_version = wanted_version
                except:
                    print(f"Tests failed again. Reverting to current version {current_version}...")
                    final_version = current_version
                    install_package_and_run_tests(package, current_version, project_path)
                    failed_updates.append(package)
        else:
            if current_version and wanted_version and current_version != wanted_version:
                try:
                    install_package_and_run_tests(package, wanted_version, project_path)
                    final_version = wanted_version
                except Exception as e:
                    failed_updates.append(package)
            else:
                print(f"Skipping {package}, already at wanted version or missing version info.")
        
        updated_packages.append((package, current_version, final_version))
    return updated_packages, failed_updates

def print_final_summary(all_updated_packages, all_failed_updates):
    """Print the final summary of updated packages."""
    print("\nFinal Update Summary:")
    print("{:<40} {:<10} {:<10}".format("Package", "Old Version", "New Version"))
    print("-" * 60)
    for pass_num, updated_packages in all_updated_packages:
        print(f"\n=== Pass {pass_num} ===")
        for package, old_version, new_version in updated_packages:
            print("{:<40} {:<10} {:<10}".format(package, old_version, new_version))
    print("-" * 60)

    if all_failed_updates:
        print("\nPackages that failed to update:")
        for package in set(all_failed_updates):
            print(f"- {package}")

def run_update_process(project_path, safe_mode, passes):
    all_updated_packages = []
    all_failed_updates = []
    
    for i in range(passes):
        print(f"\n=== Pass {i + 1} ===")
        outdated_packages = get_outdated_packages(project_path)
        if not outdated_packages:
            print("No more outdated packages found.")
            break
        
        dependency_tree = get_dependency_tree(project_path)
        updated_packages, failed_updates = update_packages_in_order(outdated_packages, dependency_tree, project_path, safe_mode)
        all_updated_packages.append((i + 1, updated_packages))
        all_failed_updates.extend(failed_updates)
    

    print("\nRunning final npm audit and build...")
    subprocess.run(["npm", "audit", "fix"], cwd=project_path)
    execute_script_if_exist(project_path, "build")
    print_final_summary(all_updated_packages, all_failed_updates)

def main():
    if len(sys.argv) < 2:
        print("No project path provided. Using the current directory as the project path.")
        project_path = os.getcwd()
    else:
        project_path = sys.argv[1]
    
    safe_mode = "--safe" in sys.argv
    pass_arg = next((arg for arg in sys.argv if arg.startswith("--pass=")), None)
    passes = int(pass_arg.split("=")[1]) if pass_arg else 1
    
    if not os.path.isdir(project_path):
        print(f"Error: {project_path} is not a valid directory.")
        sys.exit(1)
    
    run_update_process(project_path, safe_mode, passes)

if __name__ == "__main__":
    main()
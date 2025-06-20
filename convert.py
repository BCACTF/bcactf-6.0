#!/usr/bin/env python3
import yaml
import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

def run_docker_build_and_extract(base_dir, deploy_config, files_data):
    """
    Build Docker container and extract files for static deployment
    Returns list of extracted file paths
    """
    extracted_files = []
    
    if 'static' not in deploy_config:
        return extracted_files
    
    static_config = deploy_config['static']
    build_context = static_config.get('build', '.')
    
    # Build the Docker image
    build_path = base_dir / build_context if build_context != '.' else base_dir
    temp_image_name = f"ctf-extract-{base_dir.name}"
    
    print(f"Building Docker image for {base_dir.name}...")
    
    try:
        # Build the image
        subprocess.run([
            'docker', 'build', '-t', temp_image_name, str(build_path)
        ], check=True, capture_output=True)
        
        print(f"Successfully built image {temp_image_name}")
        
        # Extract files that are marked for static deployment
        for file_entry in files_data:
            if isinstance(file_entry, dict):
                src_path = file_entry.get('src')
                dest_path = file_entry.get('dest')
                container_type = file_entry.get('container')
                
                if container_type == 'static' and src_path and dest_path:
                    print(f"Extracting {src_path} to {dest_path}...")
                    
                    # Create a temporary container to extract the file
                    with tempfile.TemporaryDirectory() as temp_dir:
                        try:
                            # Run container and copy file out
                            subprocess.run([
                                'docker', 'run', '--rm', '-v', f'{temp_dir}:/extract',
                                temp_image_name, 'cp', src_path, '/extract/'
                            ], check=True, capture_output=True)
                            
                            # Move the extracted file to the destination
                            extracted_file_path = Path(temp_dir) / Path(src_path).name
                            final_dest_path = base_dir / dest_path
                            
                            if extracted_file_path.exists():
                                shutil.copy2(extracted_file_path, final_dest_path)
                                extracted_files.append(dest_path)
                                print(f"Successfully extracted {dest_path}")
                            else:
                                print(f"Warning: Could not find extracted file {src_path}")
                                
                        except subprocess.CalledProcessError as e:
                            print(f"Error extracting {src_path}: {e}")
        
        # Clean up the temporary image
        subprocess.run(['docker', 'rmi', temp_image_name], capture_output=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error building Docker image: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout.decode()}")
        if e.stderr:
            print(f"STDERR: {e.stderr.decode()}")
    
    return extracted_files

def convert_ctf_infra_to_ctfd(input_file, output_file=None, extract_files=True):
    """
    Convert CTF infra chall.yaml format to CTFd challenge.yml format
    """
    
    with open(input_file, 'r') as f:
        infra_data = yaml.safe_load(f)
    
    # Get the directory containing the input file for relative path operations
    base_dir = Path(input_file).parent
    
    # Initialize CTFd format structure
    ctfd_data = {
        'name': infra_data.get('name', 'Unknown Challenge'),
        'author': ', '.join(infra_data.get('authors', ['Unknown'])),
        'category': infra_data.get('categories', ['misc'])[0],  # Take first category
        'description': infra_data.get('description', ''),
        'attribution': f"Written by {', '.join(infra_data.get('authors', ['Unknown']))}",
        'value': infra_data.get('value', 100),
        'type': 'standard',
        'version': '0.1'
    }
    
    # Handle deployment/Docker setup
    deploy_config = infra_data.get('deploy', {})
    files_data = infra_data.get('files', [])
    extracted_files = []
    
    if deploy_config:
        # Check if there's a Dockerfile in the directory
        dockerfile_path = base_dir / 'Dockerfile'
        if dockerfile_path.exists():
            ctfd_data['image'] = '.'
        else:
            ctfd_data['image'] = None
        
        # Set protocol and connection_info based on deployment type
        if 'nc' in deploy_config:
            ctfd_data['protocol'] = 'tcp'
            nc_config = deploy_config['nc']
            if 'expose' in nc_config:
                port = nc_config['expose'].split('/')[0]  # Extract port from "8148/tcp"
                ctfd_data['connection_info'] = f'nc hostname {port}'
        elif 'static' in deploy_config:
            # Static deployment - build and extract files
            ctfd_data['protocol'] = None
            if extract_files:
                extracted_files = run_docker_build_and_extract(base_dir, deploy_config, files_data)
        else:
            ctfd_data['protocol'] = None
    else:
        ctfd_data['image'] = None
        ctfd_data['protocol'] = None
    
    # Set host to null (will be specified during deployment)
    ctfd_data['host'] = None
    
    # Handle flags
    flag_data = infra_data.get('flag')
    flags = []
    
    if isinstance(flag_data, str):
        # Simple string flag
        flags.append(flag_data)
    elif isinstance(flag_data, dict) and 'file' in flag_data:
        # Flag from file
        flag_file_path = base_dir / flag_data['file']
        if flag_file_path.exists():
            try:
                with open(flag_file_path, 'r') as f:
                    flag_content = f.read().strip()
                flags.append(flag_content)
            except Exception as e:
                print(f"Warning: Could not read flag file {flag_file_path}: {e}")
                flags.append("flag{placeholder}")
        else:
            print(f"Warning: Flag file {flag_file_path} not found")
            flags.append("flag{placeholder}")
    
    if flags:
        ctfd_data['flags'] = flags
    
    # Handle hints
    hints_data = infra_data.get('hints', [])
    if hints_data:
        ctfd_data['hints'] = hints_data
    
    # Handle files
    if files_data:
        ctfd_files = []
        for file_entry in files_data:
            if isinstance(file_entry, dict):
                # Handle complex file entries with src/dest
                if 'src' in file_entry:
                    dest_path = file_entry.get('dest')
                    container_type = file_entry.get('container')
                    
                    if container_type == 'static' and dest_path:
                        # This file should be extracted from container
                        if dest_path in extracted_files:
                            ctfd_files.append(dest_path)
                    else:
                        # Regular file
                        src_path = file_entry['src']
                        if src_path.startswith('./'):
                            src_path = src_path[2:]
                        elif src_path.startswith('/app/'):
                            src_path = src_path[5:]
                        ctfd_files.append(src_path)
            else:
                # Handle simple string file entries
                src_path = file_entry
                if isinstance(src_path, str):
                    if src_path.startswith('./'):
                        src_path = src_path[2:]
                    ctfd_files.append(src_path)
        
        if ctfd_files:
            ctfd_data['files'] = ctfd_files
    
    # Handle visibility/state
    visible = infra_data.get('visible', True)
    ctfd_data['state'] = 'visible' if visible else 'hidden'
    
    # Handle topics (convert categories to topics)
    categories = infra_data.get('categories', [])
    if len(categories) > 1:
        # Use additional categories as topics
        ctfd_data['topics'] = categories[1:]
    
    # Remove null/empty values to clean up the output
    ctfd_data = {k: v for k, v in ctfd_data.items() if v is not None and v != []}
    
    # Determine output file
    if output_file is None:
        output_file = base_dir / 'challenge.yml'
    
    # Write the converted data
    with open(output_file, 'w') as f:
        yaml.dump(ctfd_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"Converted {input_file} to {output_file}")
    return ctfd_data

def process_directory(directory, extract_files=True):
    """
    Process all chall.yaml files in subdirectories
    """
    base_path = Path(directory)
    
    if not base_path.exists():
        print(f"Error: Directory {directory} does not exist")
        return
    
    converted_count = 0
    
    # Look for chall.yaml files in subdirectories
    for subdir in base_path.iterdir():
        if subdir.is_dir():
            chall_yaml = subdir / 'chall.yaml'
            if chall_yaml.exists():
                try:
                    convert_ctf_infra_to_ctfd(chall_yaml, extract_files=extract_files)
                    converted_count += 1
                except Exception as e:
                    print(f"Error converting {chall_yaml}: {e}")
    
    print(f"Converted {converted_count} challenges")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Convert single file: python convert.py <chall.yaml> [--no-extract]")
        print("  Convert directory: python convert.py <directory> [--no-extract]")
        print("  Convert with custom output: python convert.py <chall.yaml> <output.yml> [--no-extract]")
        print("")
        print("Options:")
        print("  --no-extract    Skip Docker build and file extraction for static deployments")
        sys.exit(1)
    
    # Check for --no-extract flag
    extract_files = '--no-extract' not in sys.argv
    if not extract_files:
        sys.argv.remove('--no-extract')
    
    input_path = sys.argv[1]
    
    if os.path.isfile(input_path):
        # Single file conversion
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        convert_ctf_infra_to_ctfd(input_path, output_file, extract_files)
    elif os.path.isdir(input_path):
        # Directory conversion
        process_directory(input_path, extract_files)
    else:
        print(f"Error: {input_path} is not a valid file or directory")
        sys.exit(1)

if __name__ == "__main__":
    main()

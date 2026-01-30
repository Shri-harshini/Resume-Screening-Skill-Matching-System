import os
import shutil
from pathlib import Path

def remove_path(path):
    """Safely remove a file or directory."""
    try:
        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)
            print(f"Removed file: {path}")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Removed directory: {path}")
    except Exception as e:
        print(f"Error removing {path}: {e}")

def clean_project():
    project_root = Path(__file__).parent
    print(f"Cleaning project at: {project_root}")
    
    # Files and directories to keep
    keep_files = {
        'app.py', 'requirements.txt', 'setup.py', 'README.md', '.env',
        'src/resume_parser.py', 'src/resume_matcher.py', 'src/__init__.py'
    }
    
    # Directories to keep (empty directories will be kept)
    keep_dirs = {'src', 'data', 'tests', 'uploads'}
    
    # Remove __pycache__ directories and .pyc files
    for root, dirs, files in os.walk(project_root, topdown=False):
        # Remove __pycache__ directories
        if '__pycache__' in dirs:
            remove_path(os.path.join(root, '__pycache__'))
            dirs.remove('__pycache__')
        
        # Remove .pyc and .pyo files
        for file in files:
            if file.endswith(('.pyc', '.pyo', '.pyd')):
                file_path = os.path.join(root, file)
                remove_path(file_path)
    
    # Remove empty directories
    for root, dirs, files in os.walk(project_root, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                # Skip directories we want to keep
                if any(keep_dir in dir_path for keep_dir in keep_dirs):
                    continue
                    
                # Remove empty directories
                if not os.listdir(dir_path):
                    remove_path(dir_path)
            except OSError:
                pass
    
    # Clean up empty directories in src
    src_path = project_root / 'src'
    if src_path.exists():
        for item in src_path.iterdir():
            if item.is_dir() and not any((item / f).exists() for f in os.listdir(item) if not f.startswith('.')):
                if item.name not in {'parser', 'utils'} or not any(item.iterdir()):
                    remove_path(item)
    
    print("\nProject cleanup completed!")
    print("The following files and directories were kept:")
    print("\nCore files:")
    for f in sorted(keep_files):
        print(f"  - {f}")
    print("\nCore directories:")
    for d in sorted(keep_dirs):
        print(f"  - {d}/")

if __name__ == "__main__":
    clean_profile()

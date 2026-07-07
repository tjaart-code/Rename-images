import sys
from pathlib import Path

# Supported image extensions
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

def rename_images(directory, base_name):
    """
    Rename all images in a directory with a base name and sequential numbers.
    
    Args:
        directory (str): Path to the directory containing images
        base_name (str): Base name for renamed images
    
    Returns:
        tuple: (success_count, error_count)
    """
    directory_path = Path(directory).resolve()
    
    # Validate directory exists
    if not directory_path.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        return 0, 0
    
    if not directory_path.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        return 0, 0
    
    # Validate base name
    if not base_name or not base_name.strip():
        print("Error: Base name cannot be empty.")
        return 0, 0
    
    # Find all image files
    image_files = sorted([
        f for f in directory_path.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ])
    
    if not image_files:
        print(f"No image files found in '{directory}'.")
        return 0, 0
    
    # Show preview before proceeding
    print(f"\nFound {len(image_files)} image(s) to rename:")
    for i, file in enumerate(image_files[:5], 1):
        new_name = f"{base_name}-{i:02d}{file.suffix}"
        print(f"  {file.name} -> {new_name}")
    if len(image_files) > 5:
        print(f"  ... and {len(image_files) - 5} more")
    
    # Ask for confirmation
    confirm = input("\nProceed with renaming? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("Operation cancelled.")
        return 0, 0
    
    success_count = 0
    error_count = 0
    
    # Rename files
    for counter, old_file in enumerate(image_files, 1):
        try:
            new_name = f"{base_name}-{counter:02d}{old_file.suffix}"
            new_file_path = directory_path / new_name
            
            # Check if target already exists
            if new_file_path.exists():
                print(f"Skipped: {old_file.name} (target '{new_name}' already exists)")
                error_count += 1
                continue
            
            old_file.rename(new_file_path)
            print(f"Renamed: {old_file.name} -> {new_name}")
            success_count += 1
            
        except Exception as e:
            print(f"Error renaming {old_file.name}: {str(e)}")
            error_count += 1
    
    return success_count, error_count

if __name__ == "__main__":
    try:
        directory = input("Enter the path to the directory containing the images: ").strip()
        base_name = input("Enter the base name for the images (e.g., img): ").strip()
        
        success, errors = rename_images(directory, base_name)
        
        if success > 0 or errors > 0:
            print(f"\nSummary: {success} renamed, {errors} failed/skipped")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

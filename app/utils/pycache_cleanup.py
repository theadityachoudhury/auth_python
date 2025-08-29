import os
from app.config.database import logger
from pathlib import Path
import shutil


async def cleanup_pycache():
    """
    Remove all __pycache__ directories recursively from the project root.
    This function should only be called in development mode.
    """
    try:
        # Get the project root directory (3 levels up from this file)
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        
        logger.info(f"Starting __pycache__ cleanup in development mode: {project_root}")
        
        deleted_count = 0
        total_size = 0
        
        # Walk through all directories and find __pycache__ folders
        for root, dirs, files in os.walk(project_root):
            if '__pycache__' in dirs:
                pycache_path = Path(root) / '__pycache__'
                
                try:
                    # Calculate size before deletion
                    folder_size = sum(
                        f.stat().st_size for f in pycache_path.rglob('*') if f.is_file()
                    )
                    total_size += folder_size
                    
                    # Remove the __pycache__ directory
                    shutil.rmtree(pycache_path)
                    deleted_count += 1
                    
                    logger.debug(f"Deleted __pycache__ folder: {pycache_path}")
                    
                except PermissionError as e:
                    logger.warning(f"Permission denied deleting {pycache_path}: {e}")
                except Exception as e:
                    logger.error(f"Error deleting {pycache_path}: {e}")
                
                # Remove from dirs list to prevent os.walk from descending into it
                dirs.remove('__pycache__')
        
        if deleted_count > 0:
            size_mb = total_size / (1024 * 1024)
            logger.info(
                f"__pycache__ cleanup completed: {deleted_count} folders deleted, "
                f"{size_mb:.2f} MB freed"
            )
        else:
            logger.info("No __pycache__ folders found to clean up")
            
    except Exception as e:
        logger.error(f"Error during __pycache__ cleanup: {e}")
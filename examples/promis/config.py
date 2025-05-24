from pydantic import BaseModel, Field
import os
from typing import Dict, Optional, Union, Any
from pathlib import Path
from dotenv import load_dotenv
import logging

class ProjectPaths(BaseModel):
    
    # Project directory:
    proj_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[1])
    base_dir: Path = Field(default_factory=lambda: Path(os.path.dirname(os.path.abspath(__file__))))

    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True  # Enable Path objects
    
    def load_my_env(self, override: bool = False) -> None:
        """
        Load environment variables from .env file. 
        (.env file should be in the root dir or case dir(The .env in current example folder has a higher priority))
        Args:
            override: Whether to override the system environment variables with the variables from the .env file.
        """
        dotenv_proj_path = self.proj_dir / ".env"
        dotenv_case_path = self.base_dir / ".env"
        if dotenv_case_path.exists():
            env_path = dotenv_case_path
        else:
            if dotenv_proj_path.exists():
                env_path = dotenv_proj_path
            else:
                logging.warning(f"Environment file not found: {dotenv_proj_path}")
                return

        load_dotenv(dotenv_path=str(env_path), override=override)
        logging.info(f"Loaded environment from: {env_path}")

    def get_absproj_path(self, rel_path: Union[str, Path]) -> Path:
        """
        Get absolute path from the root of the project.
        Args:
            rel_path: Relative path
        """
        return self.proj_dir / Path(rel_path)

    def get_abscase_path(self, rel_path: Union[str, Path]) -> Path:
        """
        Get absolute path from the directory of current example.
        Args:
            rel_path: Relative path
        """
        return self.base_dir / Path(rel_path)

    def _get_path(self, category: str, file_name: Optional[str] = None) -> Path:
        """
        Get path for a specific category and optional file name of the example.
        Args:
            category: Specific folder from rel_paths
            file_name: Optional file name
        """
        if category not in self.rel_paths:
            raise ValueError(f"Unknown category: {category}. Available categories: {list(self.rel_paths.keys())}")
        
        path = self.get_abscase_path(self.rel_paths[category])
        
        # Create directory if it doesn't exist
        if not file_name:
            path.mkdir(parents=True, exist_ok=True)
            return path
            
        # Ensure parent directory exists before returning file path
        path.mkdir(parents=True, exist_ok=True)
        return path / file_name
        

    def save_as_file(self, content: Union[list, str, Any], filename: str, mode: str = "w"):
        # Save the file
        try:
            with open(filename, mode, encoding="utf-8") as f:
                f.write(content)
            logging.info(f"File saved successfully: {filename}")
            return filename
        except Exception as e:
            logging.error(f"Failed to save file {filename}: {str(e)}")
            raise

    def ensure_directories_exist(self) -> None:
        """Create all directories defined in rel_paths if they don't exist."""
        for category in self.rel_paths:
            path = self.get_abscase_path(self.rel_paths[category])
            path.mkdir(parents=True, exist_ok=True)
            logging.info(f"Ensured directory exists: {path}")


# Create a singleton instance
paths = ProjectPaths()
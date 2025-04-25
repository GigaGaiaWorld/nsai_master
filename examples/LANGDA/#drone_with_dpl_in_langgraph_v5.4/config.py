from pydantic import BaseModel, Field, validator
import os
from typing import Dict, List, Optional, Tuple, Union, Any, Literal
from pathlib import Path
from dotenv import load_dotenv
import logging


class ProjectPaths(BaseModel):
    """Configuration for project paths using Pydantic."""
    
    # Project directory:
    proj_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[3])
    base_dir: Path = Field(default_factory=lambda: Path(os.path.dirname(os.path.abspath(__file__))))

    # Relative path configurations:
    rel_paths: Dict[str, str] = Field(default={
        "origin_data": "data/origin",
        "biased_data": "data/biased",
        "rules": "rules",
        "models": "models",
        "history": "history",
        "prompts": "prompts"
    })

    # File name configurations:
    prompt_names: Dict[str, str] = Field(default={
        "generate": "system_generate_prompt_fullvision.txt",
        "evaluate": "system_evaluate_prompt_fullvision.txt",
        "regenerate": "system_regenerate_prompt_fullvision.txt"
    })

    workflow_files: Dict[str, str] = Field(default={
        "generated_result": "generated_result.txt",
        "evaluated_result": "evaluated_result.txt",
        "generated_codes": "generated_codes.txt",
        "evaluated_codes": "evaluated_codes.txt",
        "prompt_template": "prompt_template.txt",
        "final_code": "final_code.pl",
    })
    
    # Data file names
    data_files: Dict[str, str] = Field(default={
        "result_train": "result_train_data.txt",
        "result_test": "result_test_data.txt",
        "happen_train": "in_train_data.txt",
        "happen_test": "in_test_data.txt"
    })
    
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



    def get_data_path(self, dataset: str, file_type: str) -> Path:
        """
        Get path for data files with specific type and dataset.
        Args:
            dataset: One of ["origin", "biased"]
            file_type: One of ["result_train", "result_test", "happen_train", "happen_test"]
        """
        valid_datasets = ["origin", "biased"]
        valid_file_types = list(self.data_files.keys())
        
        if dataset not in valid_datasets:
            raise ValueError(f"Unknown dataset: {dataset}. Valid datasets: {valid_datasets}")
        
        if file_type not in valid_file_types:
            raise ValueError(f"Unknown file type: {file_type}. Valid file types: {valid_file_types}")
        
        dataset_path = f"{dataset}_data"
        file_name = self.data_files[file_type]
        
        return self._get_path(dataset_path, file_name)
    
    def get_prompt_path(self, prompt_name: str) -> Path:
        """
        Get path for prompt files.
        Args:
            prompt_name: One of ["evaluate", "generate", "regenerate"]
        """
        valid_prompts = list(self.prompt_names.keys())
        if prompt_name not in valid_prompts:
            raise ValueError(f"Unknown prompt: {prompt_name}. Valid prompts: {valid_prompts}")

        return self._get_path("prompts", self.prompt_names[prompt_name])
    
    def load_prompt(self, prompt: Literal["evaluate", "generate", "regenerate"]) -> str:
        """
        Load prompt content from file.
        Args:
            prompt: One of ["evaluate", "generate", "regenerate"]
        """
        path = self.get_prompt_path(prompt)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logging.error(f"Prompt file not found: {path}")
            raise

    def load_data(self, dataset: str, file_type: str) -> str:
        """
        Load data content from file.
        Args:
            dataset: One of ["origin", "biased"]
            file_type: One of ["result_train", "result_test", "happen_train", "happen_test"]
        """
        path = self.get_data_path(dataset, file_type)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logging.error(f"Data file not found: {path}")
            raise

    def save_as_file(self, content: Union[list, str, Any], filetype: str, prefix: str = ""):
        """
        Save the content as a file (with optional prefix).
        Args:
            content: Content to save (list, string, or other convertible object)
            filetype: Type of file to create, one of workflow_files keys or custom path, 
            one of [generated_result,evaluated_result,generated_codes,evaluated_codes]
                - "generated_result": "generated_result.txt"  -> output code blocks of llm 
                - "evaluated_result": "evaluated_result.txt"  -> output reports of llm 
                - "generated_codes": "generated_codes.txt"    -> code block list
                - "evaluated_codes": "evaluated_codes.txt"    -> report block list
                - "prompt_template": "prompt_template"        -> prompt template
                - "final_code": "final_code.pl"               -> generated final code
            prefix: Optional prefix for the filename
        """
        # Convert content to string
        if isinstance(content, list):
            contentstr = "\n".join(str(item) for item in content)
        else:
            contentstr = str(content)

        # Determine the save path
        if filetype in self.workflow_files:
            # Use predefined workflow file path
            filename = f"{prefix}_{self.workflow_files[filetype]}" if prefix else self.workflow_files[filetype]
            path = self._get_path("history", filename)
        else:
            # Use custom path
            path = self.get_abscase_path(filetype)
            logging.info(f"Using custom file path: {path}")
        
        # Ensure directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the file
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(contentstr)
            logging.info(f"File saved successfully: {path}")
            return path
        except Exception as e:
            logging.error(f"Failed to save file {path}: {str(e)}")
            raise

    def ensure_directories_exist(self) -> None:
        """Create all directories defined in rel_paths if they don't exist."""
        for category in self.rel_paths:
            path = self.get_abscase_path(self.rel_paths[category])
            path.mkdir(parents=True, exist_ok=True)
            logging.info(f"Ensured directory exists: {path}")


# Create a singleton instance
paths = ProjectPaths()

# Example usage:
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Ensure all directories exist
    paths.ensure_directories_exist()
    
    # Load environment variables
    paths.load_my_env()

    # Access paths
    print(f"Project directory: {paths.proj_dir}")
    print(f"Base directory: {paths.base_dir}")
    
    # Test accessing a prompt
    try:
        prompt_path = paths.get_prompt_path("generate")
        print(f"Generate prompt path: {prompt_path}")
    except ValueError as e:
        print(f"Error: {str(e)}")
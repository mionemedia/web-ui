"""WebUI Manager module for handling UI configurations and settings."""

# Standard library imports
import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Generator, List, Optional

# Third-party imports
import gradio as gr
from gradio.components import Component

# Local imports
from src.browser.custom_browser import CustomBrowser
from src.browser.custom_context import CustomBrowserContext
from src.controller.custom_controller import CustomController
from src.agent.deep_research.deep_research_agent import DeepResearchAgent


class WebuiManager:
    """Manager class for handling web UI configurations and settings."""
    
    def __init__(self, settings_save_dir: str | None = None):
        """Initialize the WebUI Manager.
        
        Args:
            settings_save_dir (str | None): Directory to save UI settings. If None,
                will try to get from environment variable WEBUI_SETTINGS_DIR or
                default to './webui_settings'
        """
        # Component mappings
        self.id_to_component: dict[str, Component] = {}
        self.component_to_id: dict[Component, str] = {}

        # Settings directory
        self.settings_save_dir = settings_save_dir or \
            os.getenv('WEBUI_SETTINGS_DIR') or \
            os.path.join(os.getcwd(), 'webui_settings')
        os.makedirs(self.settings_save_dir, exist_ok=True)
        print(f"UI settings will be saved to: {self.settings_save_dir}")
        
        # Browser use agent attributes
        self.bu_agent: Optional[CustomController] = None
        self.bu_browser: Optional[CustomBrowser] = None
        self.bu_browser_context: Optional[CustomBrowserContext] = None
        self.bu_controller: Optional[CustomController] = None
        self.bu_chat_history: List[Dict[str, Optional[str]]] = []
        self.bu_response_event: Optional[asyncio.Event] = None
        self.bu_user_help_response: Optional[str] = None
        self.bu_current_task: Optional[asyncio.Task] = None
        self.bu_agent_task_id: Optional[str] = None
        
        # Deep research agent attributes
        self.dr_agent: Optional[DeepResearchAgent] = None
        self.dr_current_task = None
        self.dr_agent_task_id: Optional[str] = None
        self.dr_save_dir: Optional[str] = None

    def init_browser_use_agent(self) -> None:
        """
        init browser use agent
        """
        self.bu_agent: Optional[Agent] = None
        self.bu_browser: Optional[CustomBrowser] = None
        self.bu_browser_context: Optional[CustomBrowserContext] = None
        self.bu_controller: Optional[CustomController] = None
        self.bu_chat_history: List[Dict[str, Optional[str]]] = []
        self.bu_response_event: Optional[asyncio.Event] = None
        self.bu_user_help_response: Optional[str] = None
        self.bu_current_task: Optional[asyncio.Task] = None
        self.bu_agent_task_id: Optional[str] = None

    def init_deep_research_agent(self) -> None:
        """
        init deep research agent
        """
        self.dr_agent: Optional[DeepResearchAgent] = None
        self.dr_current_task = None
        self.dr_agent_task_id: Optional[str] = None
        self.dr_save_dir: Optional[str] = None

    def add_components(self, tab_name: str, components_dict: dict[str, "Component"]) -> None:
        """
        Add tab components
        """
        for comp_name, component in components_dict.items():
            comp_id = f"{tab_name}.{comp_name}"
            self.id_to_component[comp_id] = component
            self.component_to_id[component] = comp_id

    def get_components(self) -> list["Component"]:
        """
        Get all components
        """
        return list(self.id_to_component.values())

    def get_component_by_id(self, comp_id: str) -> "Component":
        """
        Get component by id
        """
        return self.id_to_component[comp_id]

    def get_id_by_component(self, comp: "Component") -> str:
        """
        Get id by component
        """
        return self.component_to_id[comp]

    def save_config(self, *args) -> str:
        """Save config
        
        Args:
            *args: Components passed from Gradio
        
        Returns:
            str: Status message or path to saved file
        """
        try:
            print(f"save_config called with {len(args)} arguments")
            print(f"Settings directory: {self.settings_save_dir}")
            
            # Ensure settings directory exists
            os.makedirs(self.settings_save_dir, exist_ok=True)
            
            # Debug: Print the types of arguments
            for i, arg in enumerate(args):
                print(f"Arg {i}: {type(arg).__name__}")
                
            # Create a dictionary of component values
            components = {}
            all_components = self.get_components()
            print(f"Number of components: {len(all_components)}")
            
            for i, comp in enumerate(all_components):
                print(f"Component {i}: {type(comp).__name__} (ID: {self.get_id_by_component(comp) if comp in self.component_to_id else 'Unknown'})")
                if i < len(args):
                    if not isinstance(comp, gr.Button) and not isinstance(comp, gr.File) and \
                       str(getattr(comp, "interactive", True)).lower() != "false":
                        try:
                            comp_id = self.get_id_by_component(comp)
                            components[comp_id] = args[i]
                            print(f"Added component {comp_id} with value type: {type(args[i]).__name__}")
                        except Exception as comp_error:
                            print(f"Error processing component {i}: {str(comp_error)}")
            
            # Generate filename and save settings
            config_name = datetime.now().strftime("%Y%m%d-%H%M%S")
            save_path = os.path.join(self.settings_save_dir, f"{config_name}.json")
            print(f"Saving to: {save_path}")
            
            with open(save_path, "w") as fw:
                json.dump(components, fw, indent=4)
            
            return f"Settings saved to {save_path}"
        except Exception as e:
            import traceback
            print(f"Error in save_config: {str(e)}")
            print(traceback.format_exc())
            return f"Error saving settings: {str(e)}"

    def load_config(self, load_file) -> Generator[dict, None, None]:
        """Load configuration from a JSON file.
        
        Args:
            load_file: File object from gradio File component.
            
        Yields:
            dict: Updated component values.
        """
        try:
            if not load_file:
                yield {"load_save_config.config_status": "No file selected"}
                return

            # Check if load_file is a dictionary or a file object
            file_path = load_file.name if hasattr(load_file, 'name') else str(load_file)
            
            # Load settings from file
            with open(file_path, "r", encoding='utf-8') as fr:
                ui_settings = json.load(fr)
                
            # For now, just report success
            yield {"load_save_config.config_status": f"Settings loaded from {file_path}"}
            
            # TODO: Implement component value updating
            # Update components with loaded values will be implemented later
        except Exception as e:
            import traceback
            print(f"Error in load_config: {str(e)}")
            print(traceback.format_exc())
            yield {"load_save_config.config_status": f"Error loading file: {str(e)}"}

    def set_settings_dir(self, new_dir: str) -> str:
        """Set a new directory for saving UI settings
        
        Args:
            new_dir (str): New directory path for saving settings
            
        Returns:
            str: Status message indicating success or failure
        """
        try:
            os.makedirs(new_dir, exist_ok=True)
            self.settings_save_dir = new_dir
            return f"Successfully set settings directory to: {new_dir}"
        except Exception as e:
            return f"Error setting directory: {str(e)}"

"""WebUI Manager module for handling UI configurations and settings."""

# Standard library imports
import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

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
            './webui_settings'
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

    def save_config(self, save_file=None) -> str:
        """Save UI configuration to a JSON file.
        
        Args:
            save_file: Optional file object from gradio File component.
            
        Returns:
            str: Status message indicating success or failure.
        """
        try:
            # Collect current settings from components
            cur_settings = {}
            for comp in self.get_components():
                if not isinstance(comp, (gr.Button, gr.File)) and \
                   str(getattr(comp, "interactive", True)).lower() != "false":
                    comp_id = self.get_id_by_component(comp)
                    if comp_id:
                        cur_settings[comp_id] = comp.value

            # Determine save path
            if not save_file:
                config_name = datetime.now().strftime("%Y%m%d-%H%M%S")
                save_path = os.path.join(self.settings_save_dir, f"{config_name}.json")
            else:
                save_path = save_file.name

            # Ensure directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Save the settings
            with open(save_path, "w", encoding='utf-8') as fw:
                json.dump(cur_settings, fw, indent=4)

            return f"Settings saved to {os.path.basename(save_path)}"
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error saving settings:\n{error_details}")
            return f"Error saving settings: {str(e)}"

    def load_config(self, load_file) -> dict:
        """Load configuration from a JSON file.
        
        Args:
            load_file: File object from gradio File component.
            
        Returns:
            dict: Updated component values.
        """
        try:
            if not load_file:
                return {"load_save_config.config_status": "No file selected"}

            # Load settings from file
            with open(load_file.name, "r", encoding='utf-8') as fr:
                ui_settings = json.load(fr)

            # Update components with loaded values
            update_components = {}
            for comp_id, comp_val in ui_settings.items():
                if comp_id in self.id_to_component:
                    comp = self.id_to_component[comp_id]
                    if not isinstance(comp, (gr.Button, gr.File)):
                        update_components[comp] = comp.__class__(value=comp_val)

            # Update status message
            status_comp = self.id_to_component.get("load_save_config.config_status")
            if status_comp:
                update_components[status_comp] = gr.Textbox(
                    value=f"Successfully loaded config: {os.path.basename(load_file.name)}"
                )

            return update_components
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error loading settings:\n{error_details}")
            return {"load_save_config.config_status": f"Error loading config: {str(e)}"}

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

import os
import json
from datetime import datetime

import gradio as gr
from gradio.components import Component

from src.webui.webui_manager import WebuiManager
from src.utils import config


def create_load_save_config_tab(webui_manager: WebuiManager):
    """
    Creates a load and save config tab.
    """
    input_components = set(webui_manager.get_components())
    tab_components = {}

    config_file = gr.File(
        label="Load UI Settings from json",
        file_types=[".json"],
        interactive=True
    )
    with gr.Row():
        load_config_button = gr.Button("Load Config", variant="primary")
        save_config_button = gr.Button("Save UI Settings", variant="primary")

    config_status = gr.Textbox(
        label="Status",
        lines=2,
        interactive=False
    )

    tab_components.update(dict(
        load_config_button=load_config_button,
        save_config_button=save_config_button,
        config_status=config_status,
        config_file=config_file,
    ))

    webui_manager.add_components("load_save_config", tab_components)

    # Define a wrapper function to handle the component values properly
    def save_config_wrapper():
        try:
            print("save_config_wrapper called")
            
            # Check if running in Docker by looking for Docker-specific environment variables
            in_docker = os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') or os.environ.get('WEBUI_SETTINGS_DIR')
            
            # Use the appropriate directory based on environment
            if in_docker:
                # Use the Docker container's configured settings directory
                save_dir = os.environ.get('WEBUI_SETTINGS_DIR', '/app/webui_settings')
                print(f"Running in Docker, using directory: {save_dir}")
            else:
                # Use local directory when running directly on host
                project_root = os.getcwd()
                save_dir = os.path.join(project_root, 'webui_settings')
                print(f"Running on host, using directory: {save_dir}")
            
            # Create the directory if it doesn't exist
            os.makedirs(save_dir, exist_ok=True)
            print(f"Directory created/verified: {os.path.exists(save_dir)}")
            
            # Generate filename with timestamp
            config_name = f"settings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            save_path = os.path.join(save_dir, config_name)
            print(f"Save path: {save_path}")
            
            # Save a simple config file
            config_data = {
                "timestamp": str(datetime.now()),
                "app_version": "1.0.0",
                "saved_by": "save_config_wrapper",
                "environment": "docker" if in_docker else "host"
            }
            
            # Write the file with explicit error handling
            try:
                with open(save_path, "w") as fw:
                    json.dump(config_data, fw, indent=4)
                print("File written successfully")
            except IOError as io_err:
                print(f"IOError while writing file: {str(io_err)}")
                return f"Error saving settings (IO): {str(io_err)}"
            except Exception as write_err:
                print(f"Unexpected error writing file: {str(write_err)}")
                return f"Error saving settings (write): {str(write_err)}"
                
            # Verify the file was created
            if os.path.exists(save_path):
                print(f"File exists after save: True, size: {os.path.getsize(save_path)} bytes")
                return f"Settings saved to {save_path}"
            else:
                print("File does not exist after attempted save!")
                return "Error: File could not be saved (not found after save)"
        except Exception as e:
            import traceback
            print(f"Error in save_config_wrapper: {str(e)}")
            print(traceback.format_exc())
            return f"Error saving settings: {str(e)}"
    
    save_config_button.click(
        fn=save_config_wrapper,
        inputs=None,
        outputs=[config_status]
    )

    load_config_button.click(
        fn=webui_manager.load_config,
        inputs=[config_file],
        outputs=webui_manager.get_components(),
    )


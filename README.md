# Browser Use Web UI

![Browser Use Web UI](./assets/web-ui.png)

[![GitHub stars](https://img.shields.io/github/stars/browser-use/web-ui?style=social)](https://github.com/browser-use/web-ui/stargazers)
[![Discord](https://img.shields.io/discord/1303749220842340412?color=7289DA&label=Discord&logo=discord&logoColor=white)](https://link.browser-use.com/discord)
[![Documentation](https://img.shields.io/badge/Documentation-📕-blue)](https://docs.browser-use.com)
[![WarmShao](https://img.shields.io/twitter/follow/warmshao?style=social)](https://x.com/warmshao)

This project builds upon the foundation of the [browser-use](https://github.com/browser-use/browser-use), which is designed to make websites accessible for AI agents.

We would like to officially thank [WarmShao](https://github.com/warmshao) for his contribution to this project.

**WebUI:** is built on Gradio and supports most of `browser-use` functionalities. This UI is designed to be user-friendly and enables easy interaction with the browser agent.

**Expanded LLM Support:** We've integrated support for various Large Language Models (LLMs), including: Google, OpenAI, Azure OpenAI, Anthropic, DeepSeek, Ollama etc. And we plan to add support for even more models in the future.

**Custom Browser Support:** You can use your own browser with our tool, eliminating the need to re-login to sites or deal with other authentication challenges. This feature also supports high-definition screen recording.

**Persistent Browser Sessions:** You can choose to keep the browser window open between AI tasks, allowing you to see the complete history and state of AI interactions.

[Watch Demo Video](https://github.com/user-attachments/assets/56bc7080-f2e3-4367-af22-6bf2245ff6cb)

## Installation Guide

### Prerequisites
- Python 3.11 or higher
- Git (for cloning the repository)

### Option 1: Local Installation

Read the [quickstart guide](https://docs.browser-use.com/quickstart#prepare-the-environment) or follow the steps below to get started.

#### Step 1: Clone the Repository
```bash
git clone https://github.com/browser-use/web-ui.git
cd web-ui
```

#### Step 2: Set Up Python Environment
We recommend using [uv](https://docs.astral.sh/uv/) for managing the Python environment.

Using uv (recommended):
```bash
uv venv --python 3.11
```

Activate the virtual environment:
- Windows (Command Prompt):
```cmd
.venv\Scripts\activate
```
- Windows (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```
- macOS/Linux:
```bash
source .venv/bin/activate
```

#### Step 3: Install Dependencies
Install Python packages:
```bash
uv pip install -r requirements.txt
```

Install Browsers in Playwright:
You can install specific browsers by running:
```bash
playwright install --with-deps chromium
```

To install all browsers:
```bash
playwright install
```

#### Step 4: Configure Environment
1. Create a copy of the example environment file:
- Windows (Command Prompt):
```bash
copy .env.example .env
```
- macOS/Linux/Windows (PowerShell):
```bash
cp .env.example .env
```
2. Open `.env` in your preferred text editor and add your API keys and other settings

### Option 2: Docker Installation

#### Prerequisites
- Docker and Docker Compose installed
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/) (For Windows/macOS)
  - [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) (For Linux)

#### Option 1: Using Docker Compose with Local Build
1. Clone the repository:
```bash
git clone https://github.com/browser-use/web-ui.git
cd web-ui
```

2. Create a `.env` file:
```bash
cp .env.example .env
```

3. Build and run with Docker Compose:
```bash
docker-compose up
```

#### Option 2: Using Pre-built Docker Image (Recommended)
1. Create a new directory and navigate into it:
```bash
mkdir browser-use-webui
cd browser-use-webui
```

2. Create a `.env` file with your configuration:
```env
OLLAMA_ENDPOINT=http://host.docker.internal:11434
OLLAMA_MODELS=llama2:7b,codellama:7b,mistral:7b,mixtral:8x7b
BROWSER_USE_LOGGING_LEVEL=info
ANONYMIZED_TELEMETRY=false
```

3. Create a `docker-compose.yml` file:
```yaml
services:
  browser-use-webui:
    image: mionemedia/browser-use-webui:latest
    ports:
      - "7788:7788"  # Gradio default port
      - "6080:6080"  # noVNC web interface
      - "5901:5901"  # VNC port
      - "9222:9222"  # Chrome remote debugging port
    environment:
      - OLLAMA_ENDPOINT=${OLLAMA_ENDPOINT:-http://host.docker.internal:11434}
      - OLLAMA_MODELS=${OLLAMA_MODELS:-llama2:7b,codellama:7b,mistral:7b,mixtral:8x7b}
      - BROWSER_USE_LOGGING_LEVEL=${BROWSER_USE_LOGGING_LEVEL:-info}
      - ANONYMIZED_TELEMETRY=${ANONYMIZED_TELEMETRY:-false}
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix
      - ${PWD}/webui_settings:/app/webui_settings
    restart: unless-stopped
    shm_size: '2gb'
    cap_add:
      - SYS_ADMIN
    security_opt:
      - seccomp=unconfined
```

4. Create the settings directory:
```bash
mkdir webui_settings
```

5. Start the container:
```bash
docker-compose up
```

#### Option 3: Manual Installation
cd web-ui
```

2. Create and configure environment file:
- Windows (Command Prompt):
```bash
copy .env.example .env
```
- macOS/Linux/Windows (PowerShell):
```bash
cp .env.example .env
```
Edit `.env` with your preferred text editor and add your API keys

3. Run with Docker:
```bash
# Build and start the container with default settings (browser closes after AI tasks)
docker compose up --build
```
```bash
# Or run with persistent browser (browser stays open between AI tasks)
CHROME_PERSISTENT_SESSION=true docker compose up --build
```


4. Access the Application:
- Web Interface: Open `http://localhost:7788` in your browser
- VNC Viewer (for watching browser interactions): Open `http://localhost:6080/vnc.html`
  - Default VNC password: "youvncpassword"
  - Can be changed by setting `VNC_PASSWORD` in your `.env` file

## Troubleshooting

### Common Issues

1. **Cannot connect to Ollama**
   - Make sure Ollama is running locally
   - Check if the OLLAMA_ENDPOINT is correctly set to `http://host.docker.internal:11434`
   - For Linux hosts, you might need to use the host's IP address instead of `host.docker.internal`

2. **UI Settings not saving**
   - Ensure the `webui_settings` directory exists and has correct permissions
   - Check if the volume mount in `docker-compose.yml` is correct
   - Try using absolute paths for the volume mount

3. **Browser window not visible in VNC**
   - Wait a few seconds after container startup for all services to initialize
   - Check if you can access the noVNC interface at `http://localhost:6080/vnc.html`
   - Make sure no other service is using port 6080

4. **Container fails to start**
   - Check if all required ports (7788, 6080, 5901, 9222) are available
   - Ensure you have enough system resources (at least 2GB of memory)
   - Try increasing the `shm_size` in docker-compose.yml if browser crashes

## Usage

## Local Setup
1.  **Run the WebUI:**
    After completing the installation steps above, start the application:
    ```bash
    python webui.py --ip 127.0.0.1 --port 7788
    ```
2. WebUI options:
   - `--ip`: The IP address to bind the WebUI to. Default is `127.0.0.1`.
   - `--port`: The port to bind the WebUI to. Default is `7788`.
   - `--theme`: The theme for the user interface. Default is `Ocean`.
     - **Default**: The standard theme with a balanced design.
     - **Soft**: A gentle, muted color scheme for a relaxed viewing experience.
     - **Monochrome**: A grayscale theme with minimal color for simplicity and focus.
     - **Glass**: A sleek, semi-transparent design for a modern appearance.
     - **Origin**: A classic, retro-inspired theme for a nostalgic feel.
     - **Citrus**: A vibrant, citrus-inspired palette with bright and fresh colors.
     - **Ocean** (default): A blue, ocean-inspired theme providing a calming effect.
   - `--dark-mode`: Enables dark mode for the user interface.
3.  **Access the WebUI:** Open your web browser and navigate to `http://127.0.0.1:7788`.
4.  **Using Your Own Browser(Optional):**
    - Set `CHROME_PATH` to the executable path of your browser and `CHROME_USER_DATA` to the user data directory of your browser. Leave `CHROME_USER_DATA` empty if you want to use local user data.
      - Windows
        ```env
         CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
         CHROME_USER_DATA="C:\Users\YourUsername\AppData\Local\Google\Chrome\User Data"
        ```
        > Note: Replace `YourUsername` with your actual Windows username for Windows systems.
      - Mac
        ```env
         CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
         CHROME_USER_DATA="/Users/YourUsername/Library/Application Support/Google/Chrome"
        ```
    - Close all Chrome windows
    - Open the WebUI in a non-Chrome browser, such as Firefox or Edge. This is important because the persistent browser context will use the Chrome data when running the agent.
    - Check the "Use Own Browser" option within the Browser Settings.
5. **Keep Browser Open(Optional):**
    - Set `CHROME_PERSISTENT_SESSION=true` in the `.env` file.

### Docker Setup
1. **Environment Variables:**
   - All configuration is done through the `.env` file
   - Available environment variables:
     ```
     # LLM API Keys
     OPENAI_API_KEY=your_key_here
     ANTHROPIC_API_KEY=your_key_here
     GOOGLE_API_KEY=your_key_here

     # Browser Settings
     CHROME_PERSISTENT_SESSION=true   # Set to true to keep browser open between AI tasks
     RESOLUTION=1920x1080x24         # Custom resolution format: WIDTHxHEIGHTxDEPTH
     RESOLUTION_WIDTH=1920           # Custom width in pixels
     RESOLUTION_HEIGHT=1080          # Custom height in pixels

     # VNC Settings
     VNC_PASSWORD=your_vnc_password  # Optional, defaults to "vncpassword"
     ```

2. **Platform Support:**
   - Supports both AMD64 and ARM64 architectures
   - For ARM64 systems (e.g., Apple Silicon Macs), the container will automatically use the appropriate image

3. **Browser Persistence Modes:**
   - **Default Mode (CHROME_PERSISTENT_SESSION=false):**
     - Browser opens and closes with each AI task
     - Clean state for each interaction
     - Lower resource usage

   - **Persistent Mode (CHROME_PERSISTENT_SESSION=true):**
     - Browser stays open between AI tasks
     - Maintains history and state
     - Allows viewing previous AI interactions
     - Set in `.env` file or via environment variable when starting container

4. **Viewing Browser Interactions:**
   - Access the noVNC viewer at `http://localhost:6080/vnc.html`
   - Enter the VNC password (default: "vncpassword" or what you set in VNC_PASSWORD)
   - Direct VNC access available on port 5900 (mapped to container port 5901)
   - You can now see all browser interactions in real-time

5. **Container Management:**
   ```bash
   # Start with persistent browser
   CHROME_PERSISTENT_SESSION=true docker compose up -d

   # Start with default mode (browser closes after tasks)
   docker compose up -d

   # View logs
   docker compose logs -f

   # Stop the container
   docker compose down
   ```

## Changelog
- [x] **2025/01/26:** Thanks to @vvincent1234. Now browser-use-webui can combine with DeepSeek-r1 to engage in deep thinking!
- [x] **2025/01/10:** Thanks to @casistack. Now we have Docker Setup option and also Support keep browser open between tasks.[Video tutorial demo](https://github.com/browser-use/web-ui/issues/1#issuecomment-2582511750).
- [x] **2025/01/06:** Thanks to @richard-devbot. A New and Well-Designed WebUI is released. [Video tutorial demo](https://github.com/warmshao/browser-use-webui/issues/1#issuecomment-2573393113).

<div align="center">

# 🚀 Prompt Surfer

*A retro-styled terminal application for generating AI prompts across multiple creative platforms*

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- Replace with your actual screenshot -->
<pre>
  ██████╗ ██████╗  ██████╗ ███╗   ███╗██████╗ ████████╗
  ██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗╚══██╔══╝
  ██████╔╝██████╔╝██║   ██║██╔████╔██║██████╔╝   ██║
  ██╔═══╝ ██╔══██╗██║   ██║██║╚██╔╝██║██╔═══╝    ██║
  ██║     ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║        ██║
  ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝        ╚═╝
  ███████╗██╗   ██╗██████╗ ███████╗███████╗██████╗
  ██╔════╝██║   ██║██╔══██╗██╔════╝██╔════╝██╔══██╗
  ███████╗██║   ██║██████╔╝█████╗  █████╗  ██████╔╝
  ╚════██║██║   ██║██╔══██╗██╔══╝  ██╔══╝  ██╔══██╗
  ███████║╚██████╔╝██║  ██║██║     ███████╗██║  ██║
  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
   🤖 🏄
</pre>

</div>

## ✨ Features

- 🖼️ **Image Generation**: Create detailed Midjourney v7 prompts with style variations
- 🎵 **Music Creation**: Generate prompts for both Udio and Suno AI music platforms
- 🎸 **Instrumental Focus**: Specialized support for Suno AI instrumental music generation
- 🤖 **Advanced AI**: Powered by OpenAI's latest models including GPT-4.1 and GPT-4.5-preview
- 🔄 **Model Selection**: Easily switch between different AI models for varied results
- 📊 **Cost Tracking**: Real-time display of token usage and associated costs
- 📝 **History Management**: Browse, search, and reuse your previously generated prompts
- 📋 **Easy Copying**: One-click copying of prompts or variations to clipboard
- 📱 **Global Access**: Run from any terminal location after installation

## 🔧 Installation

### Method 1: Install from PyPI (Recommended for Users)

```bash
# Install directly from PyPI
pip install prompt-surfer
```

### Method 2: Install from Source (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/jadentripp/prompt-surfer.git
cd prompt-surfer

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e .
```

### Method 3: Install from GitHub

```bash
# Install directly from the GitHub repository
pip install git+https://github.com/jadentripp/prompt-surfer.git
```

### API Key Setup

You'll need an OpenAI API key to use this application. Set it up using one of these methods:

1. **Environment File** (recommended):
   ```bash
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

2. **Interactive Input in the TUI**:
   - Launch the application and select "Update OpenAI API key" from the menu
   - Enter your API key when prompted
   - You'll have the option to save it for future sessions

## 🚀 Usage

### Starting the Application

After installation, you can run the application from any directory:

```bash
prompt-surfer
```

### Retro-Cool Interface

The application features a stylish retro-inspired terminal interface with intuitive navigation:

<!-- Add your own screenshot here when available -->
<div align="center">
<pre>
═════════════════════════════════════════════════════════
? Select an option:
 » Generate Midjourney prompts for image creation
   Generate music prompts
   View history of previously generated prompts
   Switch model (Current: GPT-4.1 (Apr 2025))
   Update OpenAI API key
   Quit the application
</pre>
</div>

### Creating Prompts

#### For Midjourney Image Generation

1. Select **"Generate Midjourney prompts for image creation"**
2. Enter a detailed description of the image you want to create
3. The application will generate multiple prompt variations optimized for Midjourney v7
4. Select any variation to copy directly to your clipboard

<!-- Add your own screenshot here when available -->
<div align="center">
<pre>
╔════════════════════════════════════════════════════════╗
║ GENERATED OUTPUT                                       ║
╠════════════════════════════════════════════════════════╣
║ 1. A serene Japanese garden with cherry blossoms, zen  ║
║ stone path, koi pond, traditional wooden bridge,       ║
║ vibrant spring colors, soft natural lighting, shallow  ║
║ depth of field, 8k, highly detailed, Midjourney v7     ║
║                                                        ║
║ 2. Minimalist Japanese garden, stone lanterns, raked   ║
║ sand patterns, moss-covered rocks, maple trees, early  ║
║ morning mist, tranquil atmosphere, professional        ║
║ photography, Midjourney v7                             ║
╚════════════════════════════════════════════════════════╝
</pre>
</div>

#### For Music Generation

1. Select **"Generate music prompts"**
2. Choose between **Udio** (general music) or **Suno AI** (instrumental focus)
3. Describe the music style, mood, instruments, or genre you want
4. Copy the generated prompt to use with your chosen music AI platform

### Model Selection

The application supports multiple OpenAI models:

- **GPT-4o mini**: Faster and more cost-effective
- **GPT-4o (Nov 2024)**: Powerful snapshot model
- **GPT-4.5 Preview**: Latest preview model with premium capabilities
- **GPT-4.1 (Apr 2025)**: Advanced model with exceptional performance (default)

To change models, select **"Switch model"** from the main menu.

### History Management

Access your previously generated prompts:

1. Select **"View history of previously generated prompts"**
2. Choose which prompt type to view (Midjourney, Udio, or Suno)
3. Browse through your prompt history with full details
4. Copy any previous prompt directly to your clipboard

### Advanced Features

#### API Key Management

Update your OpenAI API key at any time:

1. Select **"Update OpenAI API key"** from the main menu
2. Enter your new API key (input is hidden for security)
3. Choose whether to save it to your .env file for future use

#### OpenAI Tracing Integration

Prompt CLI integrates with OpenAI's Agents SDK tracing system, allowing you to:

- View all your prompt generations in the OpenAI Traces dashboard
- Analyze token usage and performance metrics
- Debug and improve prompt quality over time

To access your traces:

1. Log in to your OpenAI account
2. Navigate to https://platform.openai.com/traces
3. View your prompt generation history with detailed analytics

## 🔍 How It Works

Prompt CLI leverages the OpenAI Agents SDK to create specialized AI agents for different creative platforms:

1. **System Prompts**: Each agent is initialized with carefully crafted system prompts that provide detailed instructions for generating high-quality outputs for specific platforms.

2. **Agent Architecture**: The application uses the OpenAI Agents SDK to create autonomous agents that can reason about user requests and generate appropriate responses.

3. **Tracing & Analytics**: All prompts are logged with OpenAI's tracing system, allowing for analysis and improvement of prompt quality over time.

4. **Token Optimization**: Prompts are designed to be efficient with token usage while maintaining high quality output.

5. **Retro-Cool UI**: The application features a stylish terminal interface with:
   - ASCII art header and box-drawing characters
   - Carefully selected color scheme for readability and aesthetic appeal
   - Intuitive navigation with keyboard controls
   - Clean, organized display of information in bordered panels

## 📁 Project Structure

```
cli/
├── cli/                      # Main package directory
│   ├── src/                  # Source code
│   │   ├── agents_config.py  # Agent configuration
│   │   ├── cli.py            # CLI entry point
│   │   ├── history.py        # History management
│   │   ├── prompt_composer.py # Main application logic
│   │   ├── tracing.py        # OpenAI tracing integration
│   │   ├── tracing_config.py # Tracing configuration
│   │   └── utils.py          # Utility functions
│   ├── prompts/              # System prompts
│   │   ├── midjourney.txt    # Midjourney system prompt
│   │   ├── suno.txt          # Suno AI system prompt
│   │   └── udio.txt          # Udio system prompt
│   └── output/               # Generated output storage
├── main.py                   # Development entry point
├── setup.py                  # Package installation
└── README.md                 # Documentation
```

## 📋 Requirements

- **Python**: 3.8 or higher
- **OpenAI API Key**: With access to GPT-4 models
- **Dependencies**:
  - openai
  - openai-agents>=0.0.11
  - python-dotenv
  - rich
  - questionary
  - tiktoken
  - pyperclip>=1.8.2

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for their powerful API and Agents SDK
- The Rich library for the beautiful terminal interface
- Questionary for the interactive prompt components

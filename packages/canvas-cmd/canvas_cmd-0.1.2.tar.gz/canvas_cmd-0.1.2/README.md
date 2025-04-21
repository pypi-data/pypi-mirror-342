# 🎓 Canvas CLI

![Status](https://img.shields.io/badge/Status-Pre--Release-yellow?style=for-the-badge&logo=github)
![Tests](https://img.shields.io/github/actions/workflow/status/PhantomOffKanagawa/canvas-cli/run-tests.yml?style=for-the-badge&branch=main&label=Main&logo=pytest)
![Tests](https://img.shields.io/github/actions/workflow/status/PhantomOffKanagawa/canvas-cli/run-tests.yml?style=for-the-badge&logo=pytest)
![Python](https://img.shields.io/badge/Python-3.6+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-GPLv3-green?style=for-the-badge)

> **Automate your Canvas LMS submissions with a git like command-line interface!**

Are you tired of navigating through the Canvas web interface to submit assignments? Canvas CLI puts the power of Canvas in your terminal, making it easy to submit assignments and manage your Canvas interactions with simple commands.

## ✨ Features

- 📤 **Submit assignments** directly from your terminal
- 🔄 **Initialize projects** with course and assignment information for quick submissions
- ⚙️ **Configure once, use anywhere** with global and project-specific settings
- 🚀 **Fast and efficient** workflow for developers and students who live in the terminal

## 🚨 Pre-Release Notice

This project is currently in pre-release status. Most features are working, but you might encounter some rough edges or features marked as "Not Implemented" (NI).

## 🛠️ Installation

```bash
# Clone this repository
git clone https://github.com/yourusername/canvas-cli.git
cd canvas-cli

# Install in development mode
pip install -e .
```

After installation, the `canvas` command will be available in your terminal!

## 🔧 Configuration

Before using the tool, configure it with your Canvas API token:

```bash
canvas config set --global token YOUR_CANVAS_API_TOKEN
canvas config set --global host your-institution.instructure.com
```

### 🔑 Getting Your Canvas API Token

1. Log in to your Canvas account
2. Go to Account > Settings
3. Scroll down to "Approved Integrations"
4. Click "New Access Token"
5. Generate a token with appropriate permissions
6. Copy the token for use with Canvas CLI

## 📝 Commands

### ⚡ Initialize a Project

```bash
canvas init
```

This interactive command helps you set up a project configuration for faster assignment submissions.

### 📤 Submit an Assignment

```bash
# Full command (works anywhere)
canvas push -cid COURSE_ID -aid ASSIGNMENT_ID -f path/to/submission.py

# In an initialized project directory:
canvas push                     # Uses saved course ID, assignment ID, and file
canvas push -f different.py     # Override the default file

# Get info on the course and assignment
canvas status --course_details
```

### ⚙️ View Configuration

```bash
canvas config --global list
canvas config --local list
```

## 🔍 Finding Course and Assignment IDs

Course and Assignment IDs can be found in the URLs of your Canvas pages:

- **Course ID**: The number in the URL after "courses/" 
  (e.g., `https://canvas.instructure.com/courses/123456` → Course ID is `123456`)
  
- **Assignment ID**: The number in the URL after "assignments/" 
  (e.g., `https://canvas.instructure.com/courses/123456/assignments/789012` → Assignment ID is `789012`)

## 📋 Example Workflow

```bash
# Create a new project directory
mkdir python_assignment
cd python_assignment

# Create your solution file
echo "print('Hello, Canvas!')" > solution.py

# Submit your solution when ready
canvas push -cid 123456 -aid 789012 -f solution.py
```

## 🚑 Troubleshooting

- **Authentication Error**: Make sure your API token is valid and has the required permissions
- **File Not Found**: Double-check the path to your submission file
- **Course/Assignment Not Found**: Verify the course and assignment IDs

## 📊 Requirements

- Python 3.6+
- Requests library

## 📜 License

This project is open source and available under the GPL v3 License.

## 📋 Roadmap & TODOs

Future improvements and features planned for Canvas CLI:

- 🔄 Consider git remote paradigm over npm package.json for `canvas init`
- ⬇️ Add `canvas pull` to download current submissions and assignment descriptions
- ⚙️ Implement cascading config scope like git
- 🔍 ~~Build a TUI for getting course ID and assignment ID from name~~
- 📊 Add ability to retrieve versioning of submissions
- 📅 ~~Implement `git status`-like command to get due dates, grading status, and comments~~
    - 🎓 Get grades via submissions
    - 🏛️ Show completed vs open assignments
- 💬 Add commands for commenting on submissions
- 🎨 Improve CLI interface and error handling
- 📜 Add more detailed documentation and examples
- 🎬 Add a github actions integration to automatically submit on push to main
- 📦 Package the tool for easy installation via pip or conda
- 🤐 Add support for zipping up multiple folders for submission
- 📦 Add support for submitting multiple files at once
- 📃 Add support for pagination
- 📂 Add file select support to TUIs

## 🤝 Contributing

Contributions are welcome! Feel free to submit pull requests or open issues to improve the tool.

## 🔗 Related Projects

Tired of clicking into a file module to download it? Try [canvas-file-downloader](https://github.com/PhantomOffKanagawa/canvas-file-downloader) for a simple extension to download files from Canvas.

---

Made with ❤️ by a student who was tired of clicking through Canvas

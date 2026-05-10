"""
Bash Tools Schema for LLM Integration
Defines all available bash tools and their parameters for LLM to call
"""

BASH_TOOLS_SCHEMA = [
    {
        "name": "bash_execution",
        "title": "Bash Command Execution",
        "description": "Execute bash commands and capture output",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to execute",
                    "example": "ls -la /home"
                }
            },
            "required": ["command"]
        },
        "returns": {
            "type": "object",
            "description": "Command execution result",
            "properties": {
                "stdout": {
                    "type": "string",
                    "description": "Standard output from the command"
                },
                "stderr": {
                    "type": "string",
                    "description": "Standard error output from the command"
                },
                "returncode": {
                    "type": "integer",
                    "description": "Command exit code (0 = success)"
                }
            }
        }
    },
    {
        "name": "run_command",
        "title": "Run Command",
        "description": "Execute shell command and capture output",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to execute",
                    "example": "python script.py --arg value, mkdir, ..."
                }
            },
            "required": ["command"]
        },
        "returns": {
            "type": "object",
            "description": "Command execution result",
            "properties": {
                "stdout": {
                    "type": "string",
                    "description": "Standard output from the command"
                },
                "stderr": {
                    "type": "string",
                    "description": "Standard error output from the command"
                },
                "returncode": {
                    "type": "integer",
                    "description": "Command exit code"
                }
            }
        }
    },
    {
        "name": "run_background",
        "title": "Run Background",
        "description": "Execute command in background without waiting for completion",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The command to run in background",
                    "example": "python server.py"
                }
            },
            "required": ["command"]
        },
        "returns": {
            "type": "object",
            "description": "Process information",
            "properties": {
                "pid": {
                    "type": "integer",
                    "description": "Process ID"
                },
                "message": {
                    "type": "string",
                    "description": "Confirmation message with PID"
                }
            }
        }
    },
    {
        "name": "read_file",
        "title": "Read File",
        "description": "Read content from a file",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the file to read",
                    "example": "/home/user/document.txt"
                }
            },
            "required": ["path"]
        },
        "returns": {
            "type": "string",
            "description": "File content"
        }
    },
    {
        "name": "write_file",
        "title": "Write File",
        "description": "Write content to a file (overwrites if exists)",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the file to write",
                    "example": "/home/user/document.txt"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                    "example": "Hello, World!"
                }
            },
            "required": ["path", "content"]
        },
        "returns": {
            "type": "string",
            "description": "Success message with file path"
        }
    },
    {
        "name": "list_directory",
        "title": "List Directory",
        "description": "List files and folders in a directory",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the directory to list (default: current directory)",
                    "example": "/home/user",
                    "default": "."
                }
            },
            "required": []
        },
        "returns": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "List of file and folder names in the directory"
        }
    },
    {
        "name": "find_files",
        "title": "Find Files",
        "description": "Find files by pattern in a directory",
        "parameters": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "File pattern to search for (e.g., *.py, *.txt)",
                    "example": "*.py"
                },
                "root": {
                    "type": "string",
                    "description": "Root directory to search from (default: current directory)",
                    "example": "/home/user/project",
                    "default": "."
                }
            },
            "required": ["pattern"]
        },
        "returns": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "List of file paths matching the pattern"
        }
    },
    {
        "name": "copy_file",
        "title": "Copy File",
        "description": "Copy a file from source to destination",
        "parameters": {
            "type": "object",
            "properties": {
                "src": {
                    "type": "string",
                    "description": "Source file path",
                    "example": "/home/user/file.txt"
                },
                "dst": {
                    "type": "string",
                    "description": "Destination file path",
                    "example": "/home/user/backup/file.txt"
                }
            },
            "required": ["src", "dst"]
        },
        "returns": {
            "type": "string",
            "description": "Success message with source and destination paths"
        }
    },
    {
        "name": "create_directory",
        "title": "Create Directory",
        "description": "Create a new directory (creates parent directories if needed)",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the directory to create",
                    "example": "/home/user/new_folder"
                }
            },
            "required": ["path"]
        },
        "returns": {
            "type": "string",
            "description": "Success message with directory path"
        }
    },
    {
        "name": "delete_file",
        "title": "Delete File",
        "description": "Delete a file",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the file to delete",
                    "example": "/home/user/old_file.txt"
                }
            },
            "required": ["path"]
        },
        "returns": {
            "type": "string",
            "description": "Confirmation message"
        }
    },
    {
        "name": "move_file",
        "title": "Move File",
        "description": "Move or rename a file",
        "parameters": {
            "type": "object",
            "properties": {
                "src": {
                    "type": "string",
                    "description": "Source file path",
                    "example": "/home/user/old_name.txt"
                },
                "dst": {
                    "type": "string",
                    "description": "Destination file path or new name",
                    "example": "/home/user/new_name.txt"
                }
            },
            "required": ["src", "dst"]
        },
        "returns": {
            "type": "string",
            "description": "Success message with source and destination paths"
        }
    }
]

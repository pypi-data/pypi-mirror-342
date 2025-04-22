# FastAPI Generator

A simple CLI tool to generate FastAPI project structure with best practices, ready-to-use configuration, and organized folder structure.

## Installation

```bash
# Install from PyPI
pip install fastapi-project-creator
```

# Or install directly from GitHub

```bash
pip install git+https://github.com/raihanhd12/fastapi-project-creator.git
```

## Note: Requires Python 3.7 or higher.

# Create a new FastAPI project

```bash
create-fastapi-app my-project-name
```

# This will generate a complete FastAPI project structure with the following features:

- Organized directory structure following best practices
- Pre-configured API router setup with controllers and services
- Database connection with SQLAlchemy
- Environment variable configuration with host and port settings
- Ready-to-use project structure with proper entry point

```
my-project-name/
├── app/
│ ├── api/
│ │ ├── endpoints/
│ │ │ └── **init**.py
│ │ ├── **init**.py
│ │ └── api.py
│ ├── controllers/
│ │ ├── **init**.py
│ │ └── base_controller.py
│ ├── core/
│ │ ├── **init**.py
│ │ └── config.py
│ ├── db/
│ │ ├── **init**.py
│ │ └── session.py
│ ├── models/
│ │ └── **init**.py
│ ├── schemas/
│ │ └── **init**.py
│ ├── services/
│ │ ├── **init**.py
│ │ └── base_service.py
│ ├── utils/
│ │ └── **init**.py
│ ├── **init**.py
│ └── main.py
├── tests/
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

# Development

To contribute to this project:

## Clone the repository

```bash

git clone https://github.com/raihanhd12/fastapi-project-creator.git
cd fastapi-project-creator
```

## Install in development mode

```bash
pip install -e .
```

## Make your changes and test them with

```bash

create-fastapi-app test-project
```

License
MIT
For more information, visit the project homepage. To report issues, please use the issue tracker.

#!/usr/bin/env python3

import os
import shutil
import sys
from pathlib import Path


def create_file(path, content=""):
    with open(path, "w") as f:
        f.write(content)
    print(f"Created: {path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: create-fastapi-app <project-name>")
        sys.exit(1)

    project_name = sys.argv[1]
    target_dir = Path(os.getcwd()) / project_name

    # Check if directory exists
    if target_dir.exists():
        reply = input(f"Directory {project_name} already exists. Overwrite? (y/n): ")
        if reply.lower() != "y":
            print("Aborted.")
            sys.exit(1)
        shutil.rmtree(target_dir)

    # Create main structure
    folders = [
        "",  # Root directory
        "src",
        "src/app",
        "src/app/controllers",
        "src/app/middleware",
        "src/app/models",
        "src/app/schemas",
        "src/app/services",
        "src/config",
        "src/database",
        "src/database/factories",
        "src/database/migrations",
        "src/public",
        "src/routes",
        "src/routes/api",
        "src/scripts",
        "test",
    ]

    for folder in folders:
        folder_path = target_dir / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        if (
            folder and folder != "test"
        ):  # Create __init__.py in all subfolders except root and test
            create_file(folder_path / "__init__.py", "")

    # Create basic files with updated paths
    create_file(target_dir / "main.py", MAIN_PY)
    create_file(target_dir / "src" / "routes" / "api" / "v1.py", API_PY)
    create_file(target_dir / "src" / "config" / "env.py", CONFIG_PY)
    create_file(target_dir / "src" / "config" / "security.py", CONFIG_PY)
    create_file(target_dir / "src" / "database" / "session.py", DB_SESSION_PY)
    create_file(
        target_dir / "src" / "app" / "services" / "base_service.py", BASE_SERVICE_PY
    )
    create_file(
        target_dir / "src" / "app" / "controllers" / "base_controller.py",
        BASE_CONTROLLER_PY,
    )
    create_file(target_dir / ".env", ENV_FILE)
    create_file(target_dir / ".gitignore", GITIGNORE)
    create_file(target_dir / "requirements.txt", REQUIREMENTS_TXT)
    create_file(target_dir / "README.md", README_MD.format(project_name=project_name))

    print(f"\n✅ FastAPI project created in {project_name}/")
    print(f"\nTo start your app:")
    print(f"  cd {project_name}")
    print(f"  pip install -r requirements.txt")
    print(f"  python main.py\n")


# Templates with updated imports
APP_MAIN_PY = """from fastapi import FastAPI
from src.routes.api.v1 import api_router
from src.config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}
"""

MAIN_PY = """import uvicorn
from src.config.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "src.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
"""

API_PY = """from fastapi import APIRouter

api_router = APIRouter()

# Include your routers here
# from src.app.controllers import some_controller
# api_router.include_router(some_controller.router, prefix="/some", tags=["some"])
"""

CONFIG_PY = """from pydantic import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # App settings
    PROJECT_NAME: str = "FastAPI App"
    DESCRIPTION: str = "FastAPI application"
    VERSION: str = "0.1.1"
    API_V1_STR: str = "/api/v1"

    # Server settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True

    # Database
    DATABASE_URL: Optional[str] = "sqlite:///./app.db"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
"""

DB_SESSION_PY = """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config.settings import settings

engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

BASE_SERVICE_PY = """from typing import Generic, TypeVar, Type, List, Optional, Union, Dict, Any
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.database.session import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = db_obj.__dict__
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
"""

BASE_CONTROLLER_PY = """from typing import Generic, TypeVar, Type, List, Dict, Any, Optional
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.app.services.base_service import BaseService

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ServiceType = TypeVar("ServiceType", bound=BaseService)

class BaseController(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ServiceType]):
    def __init__(self, service: Type[ServiceType]):
        self.service = service

    def get_all(
        self, db: Session = Depends(get_db), skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return self.service.get_multi(db, skip=skip, limit=limit)

    def get_one(self, id: Any, db: Session = Depends(get_db)) -> ModelType:
        db_obj = self.service.get(db, id=id)
        if db_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Resource with ID {id} not found"
            )
        return db_obj

    def create(self, obj_in: CreateSchemaType, db: Session = Depends(get_db)) -> ModelType:
        return self.service.create(db, obj_in=obj_in)

    def update(
        self, id: Any, obj_in: UpdateSchemaType, db: Session = Depends(get_db)
    ) -> ModelType:
        db_obj = self.service.get(db, id=id)
        if db_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Resource with ID {id} not found"
            )
        return self.service.update(db, db_obj=db_obj, obj_in=obj_in)

    def delete(self, id: Any, db: Session = Depends(get_db)) -> ModelType:
        db_obj = self.service.get(db, id=id)
        if db_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Resource with ID {id} not found"
            )
        return self.service.remove(db, id=id)
"""

ENV_FILE = """# App settings
PROJECT_NAME="FastAPI App"
DESCRIPTION="FastAPI application"
VERSION="0.1.1"
API_V1_STR="/api/v1"

# Server settings
HOST="127.0.0.1"
PORT=8000
DEBUG=true

# Database settings
DATABASE_URL="sqlite:///./app.db"
"""

GITIGNORE = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.env
.venv
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS specific
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
.pytest_cache/
.coverage
htmlcov/
.tox/
app.db
"""

REQUIREMENTS_TXT = """fastapi>=0.95.0
uvicorn>=0.22.0
sqlalchemy>=2.0.0
pydantic>=1.10.0
python-dotenv>=1.0.0
"""

README_MD = """# {project_name}

A FastAPI project with a well-organized structure.

## Project Structure

```
{project_name}/
├── src/
│   ├── app/
│   │   ├── controllers/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   ├── config/
│   │   ├── env.py
│   │   ├── security.py
│   ├── database/
│   │   ├── session.py
│   │   ├── factories/
│   │   ├── migrations/
│   ├── public/
│   ├── routes/
│   │   ├── api/
│   │   │   ├── v1.py
│   ├── scripts/
├── test/
├── .env
├── .gitignore
├── main.py
└── requirements.txt
```

## Installation

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

## Run the application

```bash
python main.py
```

The application will run at http://127.0.0.1:8000 by default. You can change the host and port in the .env file.

## API Documentation

Visit http://127.0.0.1:8000/docs for the Swagger UI documentation.

## Environment Variables

Configure your application by editing the .env file:

```
# App settings
PROJECT_NAME="Your App Name"
DESCRIPTION="Your app description"
VERSION="0.1.0"
API_V1_STR="/api/v1"

# Server settings
HOST="127.0.0.1"
PORT=8000
DEBUG=true

# Database settings
DATABASE_URL="sqlite:///./app.db"
```
"""

if __name__ == "__main__":
    main()

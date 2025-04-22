# Common CRUD

A lightweight, flexible library for common CRUD (Create, Read, Update, Delete) operations with SQLAlchemy and FastAPI.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![SQLAlchemy 2.0+](https://img.shields.io/badge/sqlalchemy-2.0+-green.svg)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

Common CRUD provides a clean, reusable base class (`BaseCRUD`) that handles standard database operations for SQLAlchemy models. It's designed to:

- Reduce boilerplate code for common database operations
- Provide consistent error handling and logging
- Support both simple and advanced filtering options
- Work seamlessly with SQLAlchemy's async functionality

## Installation

```bash
pip install common-crud
```

Or with Poetry:

```bash
poetry add common-crud
```

## Dependencies

- Python 3.11+
- SQLAlchemy 2.0+

## Usage

### Basic Setup

Create a CRUD class for your SQLAlchemy model:

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from common_crud import BaseCRUD

# Define your SQLAlchemy model
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

# Create a CRUD class for your model
class UserCRUD(BaseCRUD):
    model = User
    # Optional: Define fields that should use ILIKE for case-insensitive search
    filter_fields = {"name": "ilike", "email": "ilike"}
```

### Basic Operations

```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Create engine and session
engine = create_async_engine("sqlite+aiosqlite:///database.db")
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def main():
    async with async_session() as session:
        # Create
        new_user = await UserCRUD.add(
            session=session, 
            name="John Doe",
            email="john@example.com"
        )
        print(f"Added user: {new_user.id}")
        
        # Read by ID
        user = await UserCRUD.find_one_or_none_by_id(
            session=session,
            data_id=new_user.id
        )
        print(f"Found user: {user.name}")
        
        # Read with filter
        users = await UserCRUD.find_all(
            session=session, 
            name="John"  # Will use ILIKE since it's in filter_fields
        )
        print(f"Found {len(users)} users")
        
        # Update
        rows_updated = await UserCRUD.update(
            session=session,
            filter_by={"id": new_user.id},
            name="John Smith"
        )
        print(f"Updated {rows_updated} rows")
        
        # Delete
        rows_deleted = await UserCRUD.delete(
            session=session,
            id=new_user.id
        )
        print(f"Deleted {rows_deleted} rows")

# Run the async function
asyncio.run(main())
```

### Advanced Features

#### Time Range Filtering

Filter records based on a date/time field:

```python
# Find all records created between two dates
records = await MyCRUD.find_all_in_time_range(
    session=session,
    start_time=datetime(2023, 1, 1),
    end_time=datetime(2023, 12, 31),
    param="created_at"  # Default field name
)
```

#### Bulk Insert

Efficiently insert multiple records:

```python
rows_inserted = await UserCRUD.bulk_insert(
    session=session,
    data=[
        {"name": "User 1", "email": "user1@example.com"},
        {"name": "User 2", "email": "user2@example.com"},
        {"name": "User 3", "email": "user3@example.com"}
    ]
)
```

### Error Handling

The library provides specialized exceptions:

```python
from common_crud.exceptions import CRUDError, ModelNotSetError, InvalidFilterError, DatabaseError

try:
    await UserCRUD.update(session=session, filter_by={}, name="New Name")
except InvalidFilterError:
    print("Need to provide filter criteria for update")
except DatabaseError as e:
    print(f"Database error: {e}")
except CRUDError as e:
    print(f"Generic error: {e}")
```

## FastAPI Integration

Works seamlessly with FastAPI:

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session  # Your session dependency
from models import User, UserCRUD
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        orm_mode = True

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        db_user = await UserCRUD.add(session=session, **user.dict())
        return db_user
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await UserCRUD.find_one_or_none_by_id(session=session, data_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE)  file for details. 
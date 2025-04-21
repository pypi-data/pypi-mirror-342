<p align="center">
  <a href="https://github.com/biisal/flashdb">
    <img src="https://github.com/biisal/flashdb/blob/main/docs/assets/flashdb.png?raw=true" alt="flashDB." width="50%" height="auto">
  </a>
</p>

<p align="center">
<i>Follow DRY principles and keep your code DRY with FlashDB</i>
<br>
<i> <span style="font-weight: bold;">FlashDB </span> is a high-performance, generic CRUD operations package combining SQLAlchemy async ORM with Redis caching.</i>
</p>

---

## Features
- **Type-Safe CRUD Operations**: Built with Python type hints and generics for robust type checking
- **SQLAlchemy Integration**: Seamless integration with SQLAlchemy for database operations
- **Redis Caching**: Integrated Redis caching with automatic cache invalidation
- **Async Support**: Fully asynchronous operations using SQLAlchemy async ORM and Redis
- **Pagination**: Built-in pagination support with customizable limits and page numbers
- **Pydantic Integration**: Seamless integration with Pydantic for schema validation
- **Generic Base Class**: Extensible base class for creating custom CRUD operations
- **Automatic Cache Management**: Smart cache invalidation on data modifications
- **Error Handling**: Consistent error handling with custom exceptions

---
## Note 
- ⚡ FlashDB is designed with FastAPI (Fastest Python Web Framework) in mind, providing optimal support for asynchronous operations, dependency injection, and Pydantic-based validation.

- However, FlashDB is framework-agnostic — you can use it with any Python async environment (such as plain asyncio, Quart, Starlette, etc.), as long as you're using SQLAlchemy's async ORM.

- Whether you're building REST APIs, microservices, or internal tooling, FlashDB can boost your productivity with clean and reusable CRUD operations. 💡

---
## Requirements

- Python 3.10 or higher
- SQLAlchemy
- Redis
- Pydantic
- orjson

*You only need to ensure Python version compatibility. All other dependencies will be installed automatically with FlashDB.*

---

## Installation

 - Using uv

First create a virtual environment and activate it<br> 
<i> (if not already done and it's a good practice to keep your dependencies in a virtual environment) </i> :
    
```console
uv venv
source .venv/bin/activate 
```

Install FlashDB:
```console
uv pip install flashdb
```


 - Using pip

Create a virtual environment and activate it:

    
```console
python3 -m venv venv
source venv/bin/activate
```
Install FlashDB:

```console
pip install flashdb
```
Now you are ready to use FlashDB! 🤩

---


## Tutorial

Click [here](https://biisal.github.io/flashdb/tutorial) to see a complete example

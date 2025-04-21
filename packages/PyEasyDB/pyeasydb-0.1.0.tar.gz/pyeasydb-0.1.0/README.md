```md
# PyEasyDB

PyEasyDB is a lightweight and simple Python library for managing a database with ease. It allows you to store and retrieve dictionaries in an SQLite database without dealing with complex database operations.

## Features

- Store Python dictionaries in an SQLite database
- Retrieve dictionaries using a unique identifier
- Automatically initializes the database table if it doesn't exist
- Easy-to-use API for quick integration

## Installation

To install PyEasyDB, use the following command:

```bash
pip install PyEasyDB
```

> **Note**: Ensure you are in the project directory containing the `setup.py` file.

## Usage

### 1. Save a Dictionary

Use the `save` function to store a dictionary in the database:

```python
from PyEasyDB import save

data = {"name": "Alice", "age": 25, "city": "London"}
save(data, "user_1")
```

### 2. Load a Dictionary

Use the `load` function to retrieve a dictionary from the database:

```python
from PyEasyDB import load

retrieved_data = load("user_1")
print(retrieved_data)  # Output: {'name': 'Alice', 'age': 25, 'city': 'London'}
```

## Core Functions

### `save(dictionary, dict_id)`

- **Parameters**:
  - `dictionary` (dict): The dictionary to save.
  - `dict_id` (str): A unique identifier for the dictionary.
- **Description**: Serializes the dictionary into JSON format and stores it in the database. If an entry with the same ID exists, it will be replaced.

### `load(dict_id)`

- **Parameters**:
  - `dict_id` (str): The unique identifier of the dictionary to retrieve.
- **Returns**: The dictionary as a Python `dict` if found, otherwise `None`.
- **Raises**:
  - `sqlite3.Error`: If a database error occurs.
  - `json.JSONDecodeError`: If the retrieved data cannot be decoded as JSON.

## Requirements

- Python 3.6 or higher
- SQLite (included by default with Python)

## Contributing

Contributions are welcome! To contribute:

1. Fork this repository.
2. Make your changes.
3. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

- **RedSnows**  
  Email: id.suzuya@email.com
```
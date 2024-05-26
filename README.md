# py-redis-adapter

A basic adapter for python-redis

## Installation

Clone this repo, copy the whole folder to your project, rename it to "redisadapter", and import the package.
```python
from redisadapter.cache import Cache
```

## Usage

Initialization
```python
from redisadapter.cache import Cache

cache = Cache('my_cache', '127.0.0.1', 6379)
cache.setup_passphrase('my-passphrase')
```

Create a new sub*
```python
cache.create_sub('users', {
    'uid': 'INTEGER',
    'name': 'TEXT',
    'status': 'BOOLEAN'
}, passphrase='my-passphrase')
```
Notes:
* The first element is always be a key for Redis cache, and must be a TEXT or an INTEGER.
* Available data types: TEXT, INTEGER, REAL, BOOLEAN
* Available data modifier: NOT NULL

Delete an existing sub*
```python
cache.delete_sub('users', passphrase='my-passphrase')
```
<sub>*Passphrase is required for performing administrative task such as creating and deleting tables.<sub>

***

Run an SET statement
```python
cache.sub('users').set(800099, {
    'name': 'Alex',
    'status': True
})
```

Run an SET-MANY statement
```python
cache.sub('users').set_many({
    800100: {
        'name': 'Becky',
        'status': False
    },
    800209: {
        'name': 'Cockney',
        'status': True
    },
    803333: {
        'name': 'Doodle',
        'status': True
    }
})
```

Run a GET statement
```python
cache.sub('users').get(800100)
```

Run a GET-MANY statement
```python
cache.sub('users').get_many([800099, 800209])
```

Run a GET-ALL statement
```python
cache.sub('users').get_all()
```

Run a UNSET statement
```python
cache.sub('users').unset(800099)
```

Run a UNSET-MANY statement
```python
cache.sub('users').unset_many([800209, 800100])
```

Run a UNSET-ALL statement
```python
cache.sub('users').unset_all()
```

---
For the complete example please run [main.py](https://github.com/thisismyracle/py-sqlite3-adapter/blob/main/main.py).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
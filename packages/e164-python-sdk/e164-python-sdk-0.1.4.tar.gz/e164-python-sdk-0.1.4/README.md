# E164 Python SDK

A Python library for handling E.164 formatted phone numbers. This library allows you to validate and retrieve metadata about phone numbers using the e164.com API.

## Installation

```bash
pip install e164-python-sdk
```

## Usage

Here's a quickstart guide to using the library:

```python
#!/usr/bin/env python3
from e164_python import E164

def main():
    try:
        e164_instance = E164()

        response = e164_instance.lookup("441133910781")

        print(f"{response.prefix}")
        print(f"{response.calling_code}")
        print(f"{response.iso3}")
        print(f"{response.tadig}")
        print(f"{response.mccmnc}")
        print(f"{response.type}")
        print(f"{response.location}")
        print(f"{response.operator_brand}")
        print(f"{response.operator_company}")
        print(f"{response.total_length_min}")
        print(f"{response.total_length_max}")
        print(f"{response.weight}")
        print(f"{response.source}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

## Features

- Validate E.164 formatted phone numbers.
- Retrieve metadata such as country code, operator, and phone number type.
- Easy-to-use Python interface.

For more details, refer to the documentation or explore the source code.

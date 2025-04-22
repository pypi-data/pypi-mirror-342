# Stukk

> **Warning**: This library is currently in development and is not yet ready for production use. The features mentioned are still being worked on, and there may be significant changes in future updates. Use with caution.

**Stukk** is a library for creating graphical user interfaces (GUIs) with Tkinter in a simple way, allowing for efficient definition of structures and styles.

## Installation

To install **Stukk** from PyPI, use `pip`:

```bash
pip install stukk
```

## Basic Usage Example

```python
from stukk import stk

stk.window(
    settings={
        "title": "My App",
        "size": (400, 300)
    },
    layout=[
        # Definition of widgets here...
    ],
    styles={
        # Optional styles...
    }
)
```

## Features

- Definition of widgets like `Label`, `Button`, `Entry`, etc.
- Simple styling system similar to CSS.
- Support for custom events.

## Contributing

Contributions are welcome. If you find a bug or have an enhancement in mind, please open an issue or a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

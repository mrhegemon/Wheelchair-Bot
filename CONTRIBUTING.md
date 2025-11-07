# Contributing to Wheelchair-Bot

Thank you for your interest in contributing to Wheelchair-Bot! This project aims to provide a safe and accessible interface for controlling electric wheelchairs.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Wheelchair-Bot.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Install dependencies: `pip install -r requirements.txt`
5. Install in development mode: `pip install -e .`

## Development

### Running Tests

Run the integration tests to ensure everything works:

```bash
python tests/test_integration.py
```

### Running Examples

Test your changes with the example scripts:

```bash
python examples/show_models.py
python examples/simulated_control.py
```

## Adding a New Wheelchair Model

To add support for a new wheelchair model:

1. Create a new class in `wheelchair_bot/wheelchairs/models.py` that inherits from `Wheelchair`
2. Implement the `get_motor_config()` method
3. Add your model to the imports in `wheelchair_bot/wheelchairs/__init__.py`
4. Update the examples and documentation

Example:

```python
class MyWheelchair(Wheelchair):
    def __init__(self):
        super().__init__(
            name="My Wheelchair Model",
            max_speed=2.0,  # m/s
            wheel_base=0.45,  # meters
            wheel_diameter=0.35,  # meters
        )
    
    def get_motor_config(self):
        return {
            "type": "mid_wheel_drive",
            "motor_count": 2,
            "motor_type": "brushless_dc",
            "max_voltage": 24,
            "max_current": 50,
        }
```

## Adding a New Controller Type

To add support for a new controller:

1. Create a new file in `wheelchair_bot/controllers/`
2. Create a class that inherits from `Controller`
3. Implement all abstract methods: `connect()`, `disconnect()`, `read_input()`, `is_connected()`
4. Add your controller to the imports in `wheelchair_bot/controllers/__init__.py`

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all classes and methods
- Keep functions focused and simple
- Add comments for complex logic

## Safety Considerations

This project deals with wheelchair control, which has real-world safety implications:

- Always prioritize safety in your contributions
- Test thoroughly before submitting
- Document any safety-related changes
- Consider edge cases and failure modes
- Never remove or weaken existing safety features without discussion

## Pull Request Process

1. Ensure your code follows the style guidelines
2. Run all tests and make sure they pass
3. Update the README if you've added new features
4. Write clear commit messages
5. Submit a pull request with a description of your changes

## Questions?

Feel free to open an issue if you have questions or need help!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

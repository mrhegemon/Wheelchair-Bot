# Shared Package

This package contains shared utilities, types, and constants used across the Wheelchair Bot project.

## Features

- Common data models and types using Pydantic
- Shared constants and configurations
- Reusable utilities

## Installation

```bash
cd packages/shared
pip install -e .
```

## Usage

```python
from wheelchair_bot_shared.types import Direction, BotStatus, MoveCommand
from wheelchair_bot_shared.constants import MAX_SPEED, MIN_SPEED

# Create a status object
status = BotStatus(
    battery_level=85,
    is_moving=False,
    speed=0,
    direction=None
)

# Create a move command
cmd = MoveCommand(direction=Direction.FORWARD, speed=50)
```

## Testing

```bash
pytest
```

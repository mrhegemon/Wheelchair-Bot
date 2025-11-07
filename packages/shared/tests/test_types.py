"""Tests for shared types."""

import pytest
from wheelchair_bot_shared.types import BotStatus, Direction, MoveCommand


def test_direction_enum():
    """Test Direction enum values."""
    assert Direction.FORWARD == "forward"
    assert Direction.BACKWARD == "backward"
    assert Direction.LEFT == "left"
    assert Direction.RIGHT == "right"
    assert Direction.STOP == "stop"


def test_bot_status_valid():
    """Test valid BotStatus creation."""
    status = BotStatus(
        battery_level=85,
        is_moving=False,
        speed=0,
        direction=None,
    )
    assert status.battery_level == 85
    assert status.is_moving is False
    assert status.speed == 0
    assert status.direction is None


def test_bot_status_invalid_battery():
    """Test BotStatus with invalid battery level."""
    with pytest.raises(Exception):
        BotStatus(battery_level=150, is_moving=False, speed=0)


def test_move_command_valid():
    """Test valid MoveCommand creation."""
    cmd = MoveCommand(direction=Direction.FORWARD, speed=50)
    assert cmd.direction == Direction.FORWARD
    assert cmd.speed == 50


def test_move_command_default_speed():
    """Test MoveCommand with default speed."""
    cmd = MoveCommand(direction=Direction.STOP)
    assert cmd.direction == Direction.STOP
    assert cmd.speed == 50  # Default speed


def test_move_command_invalid_speed():
    """Test MoveCommand with invalid speed."""
    with pytest.raises(Exception):
        MoveCommand(direction=Direction.FORWARD, speed=150)

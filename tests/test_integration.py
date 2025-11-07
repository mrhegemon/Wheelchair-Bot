"""
Comprehensive integration test for wheelchair control system
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wheelchair_bot.wheelchairs.models import (
    PermobilM3Corpus,
    QuantumQ6Edge,
    InvacareTPG,
    PrideJazzy,
)
from wheelchair_bot.controllers.joystick import JoystickController
from wheelchair_bot.motors.differential import DifferentialDriveController
from wheelchair_bot.system import WheelchairControlSystem
from wheelchair_bot.safety.limiter import SpeedLimiter, AccelerationLimiter
from wheelchair_bot.safety.deadman import DeadmanSwitch


def test_wheelchair_models():
    """Test all wheelchair models can be instantiated."""
    print("Testing wheelchair models...")
    
    models = [
        PermobilM3Corpus(),
        QuantumQ6Edge(),
        InvacareTPG(),
        PrideJazzy(),
    ]
    
    for model in models:
        assert model.name is not None
        assert model.max_speed > 0
        assert model.wheel_base > 0
        assert model.wheel_diameter > 0
        
        config = model.get_motor_config()
        assert 'type' in config
        assert 'motor_count' in config
        
        # Test velocity methods
        model.set_velocity(0.5, 0.3)
        linear, angular = model.get_velocity()
        assert abs(linear - 0.5) < 0.01
        assert abs(angular - 0.3) < 0.01
        
        model.stop()
        linear, angular = model.get_velocity()
        assert linear == 0.0
        assert angular == 0.0
    
    print("✓ All wheelchair models working correctly")


def test_controllers():
    """Test controller implementations."""
    print("Testing controllers...")
    
    controller = JoystickController()
    assert controller.connect()
    assert controller.is_connected()
    
    # Disable deadzone for precise testing
    controller.set_deadzone(0.0)
    
    # Test input
    controller.set_input(0.7, 0.3)
    linear, angular = controller.read_input()
    assert abs(linear - 0.7) < 0.01
    assert abs(angular - 0.3) < 0.01
    
    # Test deadzone
    controller.set_deadzone(0.2)
    controller.set_input(0.15, 0.0)
    linear, angular = controller.read_input()
    assert linear == 0.0  # Below deadzone
    
    controller.disconnect()
    assert not controller.is_connected()
    
    print("✓ Controllers working correctly")


def test_motor_controller():
    """Test motor controller."""
    print("Testing motor controller...")
    
    motor = DifferentialDriveController()
    motor.enable()
    assert motor.is_enabled()
    
    # Test differential drive kinematics
    motor.set_velocity(0.5, 0.0)  # Forward
    left, right = motor.get_motor_speeds()
    assert abs(left - 0.5) < 0.01
    assert abs(right - 0.5) < 0.01
    
    motor.set_velocity(0.0, 0.5)  # Turn right
    left, right = motor.get_motor_speeds()
    assert left < 0  # Left wheel backward
    assert right > 0  # Right wheel forward
    
    motor.set_velocity(0.5, 0.5)  # Forward + turn
    left, right = motor.get_motor_speeds()
    assert left < right  # Right faster than left
    
    motor.disable()
    assert not motor.is_enabled()
    
    print("✓ Motor controller working correctly")


def test_safety_features():
    """Test safety features."""
    print("Testing safety features...")
    
    # Speed limiter
    limiter = SpeedLimiter(max_linear=0.5, max_angular=0.5)
    linear, angular = limiter.limit(0.8, 0.8)
    assert linear == 0.5
    assert angular == 0.5
    
    # Acceleration limiter
    accel = AccelerationLimiter(max_linear_accel=1.0, max_angular_accel=1.0)
    accel.reset()
    
    import time
    time.sleep(0.1)
    linear, angular = accel.limit(1.0, 1.0)
    # Should be limited by acceleration
    assert linear < 1.0
    assert angular < 1.0
    
    # Deadman switch
    deadman = DeadmanSwitch(timeout=0.1)
    deadman.confirm()
    assert deadman.is_active()
    
    time.sleep(0.15)
    assert not deadman.is_active()
    
    print("✓ Safety features working correctly")


def test_integration():
    """Test complete system integration."""
    print("Testing system integration...")
    
    wheelchair = QuantumQ6Edge()
    controller = JoystickController()
    motor_controller = DifferentialDriveController()
    
    system = WheelchairControlSystem(
        wheelchair=wheelchair,
        controller=controller,
        motor_controller=motor_controller,
    )
    
    # Start system
    assert system.start()
    
    # Set input and update
    controller.set_input(0.5, 0.0)
    system.deadman_switch.confirm()
    system.update()
    
    # Check status
    status = system.get_status()
    assert status['running']
    assert not status['emergency_stop']
    assert status['controller_connected']
    assert status['motors_enabled']
    
    # Test emergency stop
    system.emergency_stop_trigger()
    status = system.get_status()  # Get status after emergency stop
    assert status['emergency_stop']
    
    system.stop()
    
    print("✓ System integration working correctly")


def main():
    """Run all tests."""
    print("=" * 60)
    print("WHEELCHAIR-BOT INTEGRATION TEST")
    print("=" * 60)
    print()
    
    try:
        test_wheelchair_models()
        test_controllers()
        test_motor_controller()
        test_safety_features()
        test_integration()
        
        print()
        print("=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

"""
Simple integration test for Wheelchair-Bot services
Tests basic functionality of each service
"""
import asyncio
import time
import requests
import json

def test_service(name, url):
    """Test if a service is responding"""
    print(f"Testing {name}...", end=" ")
    try:
        response = requests.get(f"{url}/", timeout=2)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ OK - {data.get('service', 'unknown')} v{data.get('version', '?')}")
            return True
        else:
            print(f"✗ FAIL - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ FAIL - {str(e)}")
        return False


def test_teleopd():
    """Test teleopd service"""
    print("\n=== Testing Teleopd Service ===")
    
    base_url = "http://localhost:8000"
    
    # Test root endpoint
    if not test_service("Teleopd", base_url):
        return False
    
    # Test status endpoint
    print("Testing status endpoint...", end=" ")
    try:
        response = requests.get(f"{base_url}/status", timeout=2)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ OK - {data['connected_clients']} clients")
        else:
            print(f"✗ FAIL - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ FAIL - {str(e)}")
        return False
    
    # Test config endpoint
    print("Testing config endpoint...", end=" ")
    try:
        response = requests.get(f"{base_url}/config", timeout=2)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ OK - max_speed: {data['max_speed']}")
        else:
            print(f"✗ FAIL - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ FAIL - {str(e)}")
        return False
    
    return True


def test_streamer():
    """Test streamer service"""
    print("\n=== Testing Streamer Service ===")
    
    base_url = "http://localhost:8001"
    
    # Test root endpoint
    if not test_service("Streamer", base_url):
        return False
    
    # Test status endpoint
    print("Testing status endpoint...", end=" ")
    try:
        response = requests.get(f"{base_url}/status", timeout=2)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ OK - active: {data['active']}, connections: {data['peer_connections']}")
        else:
            print(f"✗ FAIL - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ FAIL - {str(e)}")
        return False
    
    return True


def test_safety_agent():
    """Test safety agent service"""
    print("\n=== Testing Safety Agent Service ===")
    
    base_url = "http://localhost:8002"
    
    # Test root endpoint
    if not test_service("Safety Agent", base_url):
        return False
    
    # Give it a moment to start monitoring
    time.sleep(2)
    
    # Test status endpoint
    print("Testing status endpoint...", end=" ")
    try:
        response = requests.get(f"{base_url}/status", timeout=2)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ OK - monitoring: {data['monitoring_active']}, estop: {data['estop_active']}")
        else:
            print(f"✗ FAIL - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ FAIL - {str(e)}")
        return False
    
    # Test alerts endpoint
    print("Testing alerts endpoint...", end=" ")
    try:
        response = requests.get(f"{base_url}/alerts", timeout=2)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ OK - {data['total']} alerts")
        else:
            print(f"✗ FAIL - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ FAIL - {str(e)}")
        return False
    
    return True


def test_net_agent():
    """Test net agent service"""
    print("\n=== Testing Net Agent Service ===")
    
    base_url = "http://localhost:8003"
    
    # Test root endpoint
    if not test_service("Net Agent", base_url):
        return False
    
    # Give it a moment to start monitoring
    time.sleep(2)
    
    # Test status endpoint
    print("Testing status endpoint...", end=" ")
    try:
        response = requests.get(f"{base_url}/status", timeout=2)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ OK - interfaces: {len(data['interfaces'])}, internet: {data['internet_accessible']}")
        else:
            print(f"✗ FAIL - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ FAIL - {str(e)}")
        return False
    
    return True


def main():
    """Main test runner"""
    print("=" * 60)
    print("Wheelchair-Bot Service Integration Tests")
    print("=" * 60)
    print("\nNOTE: Make sure all services are running before testing.")
    print("Run: ./start.sh\n")
    
    time.sleep(1)
    
    results = {
        "Teleopd": test_teleopd(),
        "Streamer": test_streamer(),
        "Safety Agent": test_safety_agent(),
        "Net Agent": test_net_agent(),
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for service, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{service:20s} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed. Check service logs.")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

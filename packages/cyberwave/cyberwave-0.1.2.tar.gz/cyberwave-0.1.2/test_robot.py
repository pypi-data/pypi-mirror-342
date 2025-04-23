from cyberwave import Robot

def test_drone_operations():
    print("Starting drone test sequence...")
    
    # Step 1: Instantiate the drone
    print("\nStep 1: Creating drone instance")
    my_drone = Robot("dji/tello")
    
    # Step 2: Connect to the drone
    print("\nStep 2: Connecting to drone")
    my_drone.connect(ip_address="192.168.1.10")
    
    # Initialize sensors
    print("\nStep 3: Initializing sensors")
    my_drone.initialize_sensors(["camera", "lidar"])
    
    # Step 4: Execute high-level autonomous task
    print("\nStep 4: Executing autonomous operations")
    print("Taking off...")
    my_drone.takeoff()
    
    print("\nScanning environment...")
    my_drone.scan_environment()
    
    print("\nSearching for target...")
    location = my_drone.find_object(instruction='red landing target')
    
    print("\nNavigating to target...")
    my_drone.fly_to(location)
    
    print("\nLanding...")
    my_drone.land()
    
    print("\nTest sequence completed!")

if __name__ == "__main__":
    test_drone_operations() 
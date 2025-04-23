# CyberWave

CyberWave is a powerful Python client for controlling various types of robots through simple, AI-driven APIs. The platform provides a unified interface for interacting with different robotic systems, from aerial drones to industrial robotic arms, making it easy to implement complex robotic operations with minimal code.

## Features

- **Unified Robot Control**: Control different types of robots (drones, robotic arms) through a single, consistent API
- **AI-Powered Operations**: Leverage machine learning for complex tasks like object detection and autonomous navigation
- **Sensor Integration**: Easy integration with various sensors (cameras, force sensors, etc.)
- **Video-Based Training**: Train models using video demonstrations for complex tasks
- **Safety First**: Built-in safety checks and error handling for all operations

## Supported Robots

- **Aerial Robots**: DJI Tello and compatible drones
- **Robotic Arms**: KUKA KR3 Agilus and compatible industrial arms
- More robot types coming soon!

## Installation

```bash
pip install cyberwave
```

## Quick Start

### Controlling a Drone

```python
from cyberwave import Robot

# Initialize and connect to a drone
drone = Robot("dji/tello")
drone.connect(ip_address="192.168.1.10")

# Execute autonomous flight operations
drone.takeoff()
drone.scan_environment()
location = drone.find_object(instruction='red landing target')
drone.fly_to(location)
drone.land()
```

### Controlling a Robotic Arm

```python
from cyberwave import Robot, VideoTrainer, perform_welding
import asyncio

# Initialize and connect to a robotic arm
arm = Robot("kuka/kr3_agilus")
arm.connect(ip_address="192.168.1.100")
arm.initialize_sensors(["camera", "force_sensor"])

# Train the arm using video demonstrations
trainer = VideoTrainer(model_type="welding")
trainer.train_from_videos(["weld_example1.mp4", "weld_example2.mp4"])

# Execute the trained welding operation
asyncio.run(perform_welding(arm, trainer.model))
```

## Key Features

### 1. Unified Robot Control
- Single API for different robot types
- Consistent command structure across platforms
- Automatic robot type detection and appropriate safety measures

### 2. AI-Powered Operations
- Computer vision for object detection and tracking
- Autonomous navigation and path planning
- Machine learning for complex task execution
- Video-based training for new operations

### 3. Sensor Integration
- Easy sensor initialization and calibration
- Support for multiple sensor types:
  - Cameras
  - Force sensors
  - LIDAR
  - More coming soon

### 4. Safety Features
- Automatic safety checks before operations
- Error handling and recovery procedures
- Collision avoidance
- Emergency stop capabilities

## Development

To set up the development environment:

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:
```bash
pip install -r requirements.txt
```

## Documentation

For detailed documentation, visit our [documentation site](https://cyberwave.ai/docs).

## License

MIT License

## Contributing

We welcome contributions! Please see our [contributing guide](https://cyberwave.ai/contributing) for details.
# Wheelchair Bot Android Controller

An Android application for controlling a wheelchair robot remotely via WebSocket and WebRTC.

## Features

- **Joystick Control**: Intuitive touch-based joystick for directional control
- **WebSocket Communication**: Real-time command transmission to the wheelchair bot
- **WebRTC Video Streaming**: Live video feed from the wheelchair's camera
- **Emergency Stop**: Dedicated emergency stop button for safety
- **Configurable Server**: Easy-to-use settings interface for server configuration
- **Connection Status**: Real-time connection status indicator

## Architecture

The app is built using Kotlin and follows modern Android development practices:

- **UI Components**:
  - `MainActivity`: Main control interface with joystick and video stream
  - `SettingsActivity`: Configuration interface for server settings
  - `JoystickView`: Custom view for touch-based joystick control

- **Network Components**:
  - `WebSocketClient`: Handles WebSocket connection and command transmission
  - `WebRTCClient`: Manages WebRTC peer connection for video streaming

## Requirements

- Android SDK 24 (Android 7.0) or higher
- Target SDK: 34 (Android 14)
- Kotlin 1.9.0
- Gradle 8.0

## Dependencies

- AndroidX Core and AppCompat libraries
- Material Design Components
- WebRTC (org.webrtc:google-webrtc:1.0.32006)
- OkHttp for WebSocket communication
- Gson for JSON serialization
- Kotlin Coroutines

## Building the App

### Prerequisites

1. Install [Android Studio](https://developer.android.com/studio)
2. Install JDK 8 or higher

### Build Steps

1. Open the project in Android Studio:
   ```bash
   cd android-controller
   # Open the android-controller directory in Android Studio
   ```

2. Sync Gradle dependencies:
   - Android Studio will automatically prompt to sync Gradle
   - Or manually: File → Sync Project with Gradle Files

3. Build the project:
   - From Android Studio: Build → Make Project
   - From command line:
     ```bash
     ./gradlew build
     ```

4. Run on a device or emulator:
   - From Android Studio: Run → Run 'app'
   - From command line:
     ```bash
     ./gradlew installDebug
     ```

### Building APK

To build a debug APK:
```bash
./gradlew assembleDebug
```

The APK will be located at: `app/build/outputs/apk/debug/app-debug.apk`

To build a release APK (requires signing configuration):
```bash
./gradlew assembleRelease
```

## Usage

### First Time Setup

1. Launch the app on your Android device
2. Tap the "Settings" button
3. Enter the WebSocket server URL (e.g., `ws://192.168.1.100:8080`)
4. Tap "Save"

### Connecting to the Wheelchair Bot

1. Ensure your Android device and the wheelchair bot are on the same network (or have internet connectivity)
2. Tap the "Connect" button
3. Wait for the connection status to show "Connected"
4. The video stream should appear automatically

### Controlling the Wheelchair

1. Use the joystick on the right panel to control movement:
   - Touch and drag within the joystick area
   - The angle determines the direction
   - The distance from center determines the speed
2. Release the joystick to stop movement

### Emergency Stop

- Tap the red "EMERGENCY STOP" button to immediately halt all movement
- This sends a stop command to the wheelchair bot

## Command Protocol

The app sends commands to the server via WebSocket in JSON format:

### Movement Command
```json
{
  "type": "movement",
  "timestamp": 1699999999999,
  "data": {
    "angle": 45.0,
    "speed": 75.0
  }
}
```

### Emergency Stop Command
```json
{
  "type": "emergency_stop",
  "timestamp": 1699999999999,
  "data": {
    "stop": true
  }
}
```

## Permissions

The app requires the following permissions:
- `INTERNET`: For network communication
- `ACCESS_NETWORK_STATE`: To check network connectivity
- `CAMERA`: For WebRTC (receive video)
- `RECORD_AUDIO`: For WebRTC (receive audio)
- `MODIFY_AUDIO_SETTINGS`: For WebRTC audio configuration
- `WAKE_LOCK`: To keep the device awake during operation

## Configuration

Settings are stored in SharedPreferences and persist between app sessions:
- Server URL: The WebSocket server address

## Troubleshooting

### Connection Issues

1. **Cannot connect to server**:
   - Verify the server URL is correct
   - Check network connectivity
   - Ensure the server is running and accessible

2. **No video stream**:
   - Check that WebRTC is properly initialized on the server
   - Verify camera permissions are granted
   - Check network bandwidth

3. **Joystick not responding**:
   - Ensure you're connected to the server
   - Check that the joystick view is enabled (should be after connection)

### Building Issues

1. **Gradle sync failed**:
   - Ensure you have a stable internet connection
   - Try File → Invalidate Caches / Restart in Android Studio

2. **Compilation errors**:
   - Verify you're using the correct SDK versions
   - Check that all dependencies are properly downloaded

## Development

### Project Structure

```
android-controller/
├── app/
│   ├── build.gradle              # App-level build configuration
│   ├── proguard-rules.pro        # ProGuard rules
│   └── src/
│       └── main/
│           ├── AndroidManifest.xml
│           ├── java/com/wheelchairbot/controller/
│           │   ├── MainActivity.kt
│           │   ├── SettingsActivity.kt
│           │   ├── JoystickView.kt
│           │   ├── WebSocketClient.kt
│           │   └── WebRTCClient.kt
│           └── res/
│               ├── layout/
│               │   ├── activity_main.xml
│               │   └── activity_settings.xml
│               ├── values/
│               │   ├── strings.xml
│               │   ├── colors.xml
│               │   └── themes.xml
│               └── mipmap-*/      # App icons
├── build.gradle                   # Project-level build configuration
├── settings.gradle                # Gradle settings
├── gradle.properties              # Gradle properties
└── README.md                      # This file
```

### Adding Features

To add new features:

1. Update the UI in the relevant layout XML files
2. Add business logic in the appropriate Activity or create new components
3. Update the WebSocket protocol if needed
4. Test thoroughly on physical devices

## License

This project is part of the Wheelchair-Bot tele-robotics kit.

## Contributing

When contributing to this project:
1. Follow Kotlin coding conventions
2. Maintain backward compatibility
3. Add appropriate comments and documentation
4. Test on multiple Android versions and devices
5. Update this README if adding new features or changing functionality

## Support

For issues or questions, please refer to the main Wheelchair-Bot repository.

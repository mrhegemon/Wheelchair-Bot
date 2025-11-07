# Quick Start Guide - Android Controller App

## For Developers

### Prerequisites
1. Install Android Studio (latest version recommended)
2. Install Android SDK Platform 34
3. Install Android SDK Build-Tools
4. Have a physical Android device or AVD (Android Virtual Device) ready

### Getting Started (5 minutes)

#### Step 1: Open the Project
```bash
# Navigate to the android-controller directory
cd android-controller

# Open in Android Studio
# File > Open > Select 'android-controller' folder
```

#### Step 2: Sync Dependencies
Android Studio will automatically prompt to sync Gradle. If not:
- File → Sync Project with Gradle Files
- Wait for dependencies to download (~2-5 minutes on first run)

#### Step 3: Run the App
1. Connect an Android device via USB with USB debugging enabled, OR
2. Start an Android Virtual Device (AVD)
3. Click the green "Run" button (▶) in Android Studio
4. Select your device/emulator
5. Wait for the app to install and launch

### First Run Setup

When the app launches:
1. Grant camera and audio permissions when prompted
2. Tap "Settings" button
3. Enter your wheelchair bot server URL (e.g., `ws://192.168.1.100:8080`)
4. Tap "Save"
5. Return to main screen
6. Tap "Connect"

### Testing Without a Server

If you don't have a wheelchair bot server running yet:
1. You can still test the UI and joystick
2. The app will show "Connection Error" when trying to connect
3. The joystick will display angle and speed values

### Building APK for Distribution

#### Debug APK (for testing)
```bash
./gradlew assembleDebug
```
Output: `app/build/outputs/apk/debug/app-debug.apk`

#### Release APK (requires signing)
1. Create a keystore (one-time setup):
```bash
keytool -genkey -v -keystore my-release-key.keystore \
  -alias wheelchair-bot -keyalg RSA -keysize 2048 -validity 10000
```

2. Configure signing in `app/build.gradle`:
```gradle
android {
    signingConfigs {
        release {
            storeFile file('my-release-key.keystore')
            storePassword 'your-password'
            keyAlias 'wheelchair-bot'
            keyPassword 'your-password'
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            // ... other settings
        }
    }
}
```

3. Build release APK:
```bash
./gradlew assembleRelease
```
Output: `app/build/outputs/apk/release/app-release.apk`

### Common Development Tasks

#### Changing App Name
Edit `app/src/main/res/values/strings.xml`:
```xml
<string name="app_name">Your App Name</string>
```

#### Changing App Icon
Replace icons in `app/src/main/res/mipmap-*` folders with your own

#### Adding New Features
1. UI changes: Edit `activity_main.xml` or `activity_settings.xml`
2. Logic changes: Edit `MainActivity.kt` or create new classes
3. New dependencies: Add to `app/build.gradle`, then sync

#### Debugging
1. Use Logcat in Android Studio to view logs
2. Add log statements:
```kotlin
import android.util.Log
Log.d("MyTag", "Debug message")
```
3. Set breakpoints and use debugger (click line numbers, then Debug ▶)

### Project Structure Quick Reference
```
android-controller/
├── app/
│   ├── build.gradle          # App dependencies and configuration
│   └── src/main/
│       ├── AndroidManifest.xml      # App permissions and activities
│       ├── java/.../controller/     # Kotlin source files
│       │   ├── MainActivity.kt      # Main screen logic
│       │   ├── SettingsActivity.kt  # Settings screen logic
│       │   ├── JoystickView.kt      # Custom joystick control
│       │   ├── WebSocketClient.kt   # WebSocket communication
│       │   └── WebRTCClient.kt      # Video streaming
│       └── res/
│           ├── layout/              # UI layouts (XML)
│           ├── values/              # Strings, colors, themes
│           └── mipmap-*/            # App icons
├── build.gradle              # Project-level configuration
├── settings.gradle           # Gradle settings
└── README.md                 # Full documentation
```

### Keyboard Shortcuts (Android Studio)

- **Run**: Shift + F10
- **Debug**: Shift + F9
- **Build**: Ctrl + F9 (Cmd + F9 on Mac)
- **Find**: Ctrl + F (Cmd + F on Mac)
- **Navigate to Class**: Ctrl + N (Cmd + O on Mac)
- **Reformat Code**: Ctrl + Alt + L (Cmd + Option + L on Mac)

### Troubleshooting

#### "SDK location not found"
Create `local.properties` file:
```properties
sdk.dir=/path/to/your/Android/sdk
```

#### "Gradle sync failed"
1. File → Invalidate Caches / Restart
2. Delete `.gradle` folder and re-sync

#### "Manifest merger failed"
Check for conflicting permissions or activities in AndroidManifest.xml

#### App crashes on launch
1. Check Logcat for error messages
2. Verify all permissions are granted
3. Ensure device meets minimum SDK requirements (API 24+)

### Next Steps

1. **Read the Full Documentation**: See README.md for complete details
2. **Review Implementation**: See IMPLEMENTATION.md for architecture details
3. **Customize the App**: Modify colors, strings, and layouts to match your needs
4. **Set Up a Server**: Implement or connect to a wheelchair bot server
5. **Test Thoroughly**: Test on multiple devices and Android versions

### Getting Help

- Check the README.md for detailed information
- Review the IMPLEMENTATION.md for architecture details
- Search Android Studio logs (Logcat) for error messages
- Refer to official Android documentation: https://developer.android.com

### Performance Tips

1. **Test on Real Devices**: Emulators may not accurately represent performance
2. **Monitor Memory**: Use Android Profiler in Android Studio
3. **Optimize Video**: Adjust WebRTC settings for your network conditions
4. **Battery Usage**: Test with battery monitoring tools

Happy coding! 🚀

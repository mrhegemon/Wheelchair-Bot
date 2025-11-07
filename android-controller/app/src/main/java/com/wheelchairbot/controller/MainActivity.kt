package com.wheelchairbot.controller

import android.Manifest
import android.content.Intent
import android.content.SharedPreferences
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import org.webrtc.MediaStream
import org.webrtc.RendererCommon
import org.webrtc.SurfaceViewRenderer

class MainActivity : AppCompatActivity() {
    
    private lateinit var surfaceView: SurfaceViewRenderer
    private lateinit var connectionStatus: TextView
    private lateinit var connectButton: Button
    private lateinit var settingsButton: Button
    private lateinit var joystick: JoystickView
    private lateinit var speedLabel: TextView
    private lateinit var directionLabel: TextView
    private lateinit var emergencyStopButton: Button
    
    private var webSocketClient: WebSocketClient? = null
    private var webRTCClient: WebRTCClient? = null
    private lateinit var sharedPreferences: SharedPreferences
    
    private var isConnected = false
    
    companion object {
        private const val PERMISSION_REQUEST_CODE = 1001
        private const val PREFS_NAME = "WheelchairBotPrefs"
        private const val KEY_SERVER_URL = "server_url"
        private const val DEFAULT_SERVER_URL = "ws://192.168.1.100:8080"
    }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        sharedPreferences = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
        
        initializeViews()
        requestPermissions()
        setupListeners()
        initializeWebRTC()
    }
    
    private fun initializeViews() {
        surfaceView = findViewById(R.id.surfaceView)
        connectionStatus = findViewById(R.id.connectionStatus)
        connectButton = findViewById(R.id.connectButton)
        settingsButton = findViewById(R.id.settingsButton)
        joystick = findViewById(R.id.joystick)
        speedLabel = findViewById(R.id.speedLabel)
        directionLabel = findViewById(R.id.directionLabel)
        emergencyStopButton = findViewById(R.id.emergencyStopButton)
        
        // Disable controls until connected
        joystick.isEnabled = false
        emergencyStopButton.isEnabled = false
    }
    
    private fun requestPermissions() {
        val permissions = arrayOf(
            Manifest.permission.CAMERA,
            Manifest.permission.RECORD_AUDIO,
            Manifest.permission.INTERNET,
            Manifest.permission.ACCESS_NETWORK_STATE
        )
        
        val permissionsToRequest = permissions.filter {
            ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED
        }
        
        if (permissionsToRequest.isNotEmpty()) {
            ActivityCompat.requestPermissions(
                this,
                permissionsToRequest.toTypedArray(),
                PERMISSION_REQUEST_CODE
            )
        }
    }
    
    private fun initializeWebRTC() {
        surfaceView.init(null, null)
        surfaceView.setScalingType(RendererCommon.ScalingType.SCALE_ASPECT_FIT)
        surfaceView.setEnableHardwareScaler(true)
        
        webRTCClient = WebRTCClient(this)
        webRTCClient?.initialize()
        
        webRTCClient?.onStreamReceived = { stream ->
            runOnUiThread {
                if (stream.videoTracks.isNotEmpty()) {
                    val videoTrack = stream.videoTracks[0]
                    videoTrack.addSink(surfaceView)
                }
            }
        }
        
        webRTCClient?.onError = { error ->
            runOnUiThread {
                Toast.makeText(this, "WebRTC Error: $error", Toast.LENGTH_SHORT).show()
            }
        }
    }
    
    private fun setupListeners() {
        connectButton.setOnClickListener {
            if (isConnected) {
                disconnect()
            } else {
                connect()
            }
        }
        
        settingsButton.setOnClickListener {
            startActivity(Intent(this, SettingsActivity::class.java))
        }
        
        joystick.onJoystickMoveListener = { angle, strength ->
            speedLabel.text = getString(R.string.speed_label, strength.toInt())
            directionLabel.text = getString(R.string.direction_label, angle)
            
            if (isConnected) {
                webSocketClient?.sendMovementCommand(angle, strength)
            }
        }
        
        emergencyStopButton.setOnClickListener {
            if (isConnected) {
                webSocketClient?.sendEmergencyStop()
                Toast.makeText(this, "Emergency Stop Activated!", Toast.LENGTH_SHORT).show()
            }
        }
    }
    
    private fun connect() {
        val serverUrl = sharedPreferences.getString(KEY_SERVER_URL, DEFAULT_SERVER_URL) ?: DEFAULT_SERVER_URL
        
        connectionStatus.text = getString(R.string.connecting)
        
        webSocketClient = WebSocketClient(serverUrl)
        
        webSocketClient?.onConnectionStateChanged = { connected ->
            runOnUiThread {
                isConnected = connected
                updateConnectionUI()
            }
        }
        
        webSocketClient?.onMessageReceived = { message ->
            // Handle incoming messages from server
        }
        
        webSocketClient?.onError = { error ->
            runOnUiThread {
                Toast.makeText(this, "Connection Error: $error", Toast.LENGTH_SHORT).show()
            }
        }
        
        webSocketClient?.connect()
    }
    
    private fun disconnect() {
        webSocketClient?.disconnect()
        webSocketClient = null
        isConnected = false
        updateConnectionUI()
    }
    
    private fun updateConnectionUI() {
        if (isConnected) {
            connectionStatus.text = getString(R.string.connected)
            connectionStatus.setTextColor(getColor(R.color.green))
            connectButton.text = getString(R.string.disconnect)
            joystick.isEnabled = true
            emergencyStopButton.isEnabled = true
        } else {
            connectionStatus.text = getString(R.string.disconnected)
            connectionStatus.setTextColor(getColor(R.color.red))
            connectButton.text = getString(R.string.connect)
            joystick.isEnabled = false
            emergencyStopButton.isEnabled = false
        }
    }
    
    override fun onDestroy() {
        super.onDestroy()
        disconnect()
        webRTCClient?.cleanup()
        surfaceView.release()
    }
    
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == PERMISSION_REQUEST_CODE) {
            val allGranted = grantResults.all { it == PackageManager.PERMISSION_GRANTED }
            if (!allGranted) {
                Toast.makeText(
                    this,
                    "Permissions are required for this app to function",
                    Toast.LENGTH_LONG
                ).show()
            }
        }
    }
}

package com.wheelchairbot.controller

import android.content.SharedPreferences
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class SettingsActivity : AppCompatActivity() {
    
    private lateinit var serverAddressInput: EditText
    private lateinit var saveButton: Button
    private lateinit var cancelButton: Button
    private lateinit var sharedPreferences: SharedPreferences
    
    companion object {
        private const val PREFS_NAME = "WheelchairBotPrefs"
        private const val KEY_SERVER_URL = "server_url"
        private const val DEFAULT_SERVER_URL = "ws://192.168.1.100:8080"
    }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_settings)
        
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        
        sharedPreferences = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
        
        initializeViews()
        loadSettings()
        setupListeners()
    }
    
    private fun initializeViews() {
        serverAddressInput = findViewById(R.id.serverAddressInput)
        saveButton = findViewById(R.id.saveButton)
        cancelButton = findViewById(R.id.cancelButton)
    }
    
    private fun loadSettings() {
        val serverUrl = sharedPreferences.getString(KEY_SERVER_URL, DEFAULT_SERVER_URL)
        serverAddressInput.setText(serverUrl)
    }
    
    private fun setupListeners() {
        saveButton.setOnClickListener {
            saveSettings()
        }
        
        cancelButton.setOnClickListener {
            finish()
        }
    }
    
    private fun saveSettings() {
        val serverUrl = serverAddressInput.text.toString().trim()
        
        if (serverUrl.isEmpty()) {
            Toast.makeText(this, "Server address cannot be empty", Toast.LENGTH_SHORT).show()
            return
        }
        
        if (!serverUrl.startsWith("ws://") && !serverUrl.startsWith("wss://")) {
            Toast.makeText(this, "Server address must start with ws:// or wss://", Toast.LENGTH_SHORT).show()
            return
        }
        
        sharedPreferences.edit().apply {
            putString(KEY_SERVER_URL, serverUrl)
            apply()
        }
        
        Toast.makeText(this, "Settings saved", Toast.LENGTH_SHORT).show()
        finish()
    }
    
    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }
}

package com.wheelchairbot.controller

import com.google.gson.Gson
import okhttp3.*
import java.util.concurrent.TimeUnit

class WebSocketClient(private val serverUrl: String) {
    
    private var webSocket: WebSocket? = null
    private val client = OkHttpClient.Builder()
        .pingInterval(30, TimeUnit.SECONDS)
        .build()
    
    private val gson = Gson()
    
    var onConnectionStateChanged: ((Boolean) -> Unit)? = null
    var onMessageReceived: ((String) -> Unit)? = null
    var onError: ((String) -> Unit)? = null
    
    fun connect() {
        val request = Request.Builder()
            .url(serverUrl)
            .build()
        
        webSocket = client.newWebSocket(request, object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: Response) {
                onConnectionStateChanged?.invoke(true)
            }
            
            override fun onMessage(webSocket: WebSocket, text: String) {
                onMessageReceived?.invoke(text)
            }
            
            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                onConnectionStateChanged?.invoke(false)
                onError?.invoke(t.message ?: "Unknown error")
            }
            
            override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                onConnectionStateChanged?.invoke(false)
            }
        })
    }
    
    fun disconnect() {
        webSocket?.close(1000, "User disconnected")
        webSocket = null
    }
    
    fun sendCommand(command: Command) {
        val json = gson.toJson(command)
        webSocket?.send(json)
    }
    
    fun sendEmergencyStop() {
        val command = Command(
            type = "emergency_stop",
            data = EmergencyStopData()
        )
        sendCommand(command)
    }
    
    fun sendMovementCommand(angle: Double, speed: Double) {
        val command = Command(
            type = "movement",
            data = MovementData(angle, speed)
        )
        sendCommand(command)
    }
    
    fun isConnected(): Boolean {
        return webSocket != null
    }
    
    data class Command(
        val type: String,
        val timestamp: Long = System.currentTimeMillis(),
        val data: Any
    )
    
    data class MovementData(
        val angle: Double,
        val speed: Double
    )
    
    data class EmergencyStopData(
        val stop: Boolean = true
    )
}

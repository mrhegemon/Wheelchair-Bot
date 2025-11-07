package com.wheelchairbot.controller

import android.content.Context
import org.webrtc.*

class WebRTCClient(private val context: Context) {
    
    private var peerConnectionFactory: PeerConnectionFactory? = null
    private var peerConnection: PeerConnection? = null
    private var videoTrack: VideoTrack? = null
    private var audioTrack: AudioTrack? = null
    
    var onStreamReceived: ((MediaStream) -> Unit)? = null
    var onError: ((String) -> Unit)? = null
    
    fun initialize() {
        val options = PeerConnectionFactory.InitializationOptions.builder(context)
            .setEnableInternalTracer(true)
            .createInitializationOptions()
        PeerConnectionFactory.initialize(options)
        
        val encoderFactory = DefaultVideoEncoderFactory(
            EglBase.create().eglBaseContext,
            true,
            true
        )
        val decoderFactory = DefaultVideoDecoderFactory(EglBase.create().eglBaseContext)
        
        peerConnectionFactory = PeerConnectionFactory.builder()
            .setVideoEncoderFactory(encoderFactory)
            .setVideoDecoderFactory(decoderFactory)
            .createPeerConnectionFactory()
    }
    
    fun createPeerConnection(iceServers: List<PeerConnection.IceServer>) {
        val rtcConfig = PeerConnection.RTCConfiguration(iceServers)
        rtcConfig.sdpSemantics = PeerConnection.SdpSemantics.UNIFIED_PLAN
        
        peerConnection = peerConnectionFactory?.createPeerConnection(
            rtcConfig,
            object : PeerConnection.Observer {
                override fun onIceCandidate(candidate: IceCandidate) {
                    // Send ice candidate to server
                }
                
                override fun onAddStream(stream: MediaStream) {
                    onStreamReceived?.invoke(stream)
                }
                
                override fun onRemoveStream(stream: MediaStream) {
                    // Handle stream removal
                }
                
                override fun onDataChannel(dataChannel: DataChannel) {}
                override fun onIceConnectionChange(state: PeerConnection.IceConnectionState) {}
                override fun onIceConnectionReceivingChange(receiving: Boolean) {}
                override fun onIceGatheringChange(state: PeerConnection.IceGatheringState) {}
                override fun onSignalingChange(state: PeerConnection.SignalingState) {}
                override fun onRenegotiationNeeded() {}
            }
        )
    }
    
    fun addRemoteDescription(sdp: SessionDescription) {
        peerConnection?.setRemoteDescription(object : SdpObserver {
            override fun onCreateSuccess(sessionDescription: SessionDescription) {}
            override fun onSetSuccess() {}
            override fun onCreateFailure(error: String) {
                onError?.invoke("Failed to set remote description: $error")
            }
            override fun onSetFailure(error: String) {
                onError?.invoke("Failed to set remote description: $error")
            }
        }, sdp)
    }
    
    fun createAnswer(onAnswerCreated: (SessionDescription) -> Unit) {
        val constraints = MediaConstraints().apply {
            mandatory.add(MediaConstraints.KeyValuePair("OfferToReceiveAudio", "true"))
            mandatory.add(MediaConstraints.KeyValuePair("OfferToReceiveVideo", "true"))
        }
        
        peerConnection?.createAnswer(object : SdpObserver {
            override fun onCreateSuccess(sessionDescription: SessionDescription) {
                peerConnection?.setLocalDescription(object : SdpObserver {
                    override fun onCreateSuccess(p0: SessionDescription?) {}
                    override fun onSetSuccess() {
                        onAnswerCreated(sessionDescription)
                    }
                    override fun onCreateFailure(error: String) {
                        onError?.invoke("Failed to create answer: $error")
                    }
                    override fun onSetFailure(error: String) {
                        onError?.invoke("Failed to set local description: $error")
                    }
                }, sessionDescription)
            }
            
            override fun onSetSuccess() {}
            override fun onCreateFailure(error: String) {
                onError?.invoke("Failed to create answer: $error")
            }
            override fun onSetFailure(error: String) {}
        }, constraints)
    }
    
    fun cleanup() {
        videoTrack?.dispose()
        audioTrack?.dispose()
        peerConnection?.close()
        peerConnection = null
        peerConnectionFactory?.dispose()
        peerConnectionFactory = null
    }
}

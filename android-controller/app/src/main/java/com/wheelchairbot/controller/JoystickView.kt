package com.wheelchairbot.controller

import android.content.Context
import android.graphics.Canvas
import android.graphics.Paint
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.View
import kotlin.math.atan2
import kotlin.math.min
import kotlin.math.pow
import kotlin.math.sqrt

class JoystickView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0
) : View(context, attrs, defStyleAttr) {

    private var centerX = 0f
    private var centerY = 0f
    private var baseRadius = 0f
    private var hatRadius = 0f
    
    private var joystickX = 0f
    private var joystickY = 0f
    
    private val basePaint = Paint().apply {
        isAntiAlias = true
        color = context.getColor(R.color.gray)
        style = Paint.Style.FILL
    }
    
    private val hatPaint = Paint().apply {
        isAntiAlias = true
        color = context.getColor(R.color.purple_500)
        style = Paint.Style.FILL
    }
    
    private val borderPaint = Paint().apply {
        isAntiAlias = true
        color = context.getColor(R.color.light_gray)
        style = Paint.Style.STROKE
        strokeWidth = 4f
    }
    
    var onJoystickMoveListener: ((angle: Double, strength: Double) -> Unit)? = null
    
    override fun onSizeChanged(w: Int, h: Int, oldw: Int, oldh: Int) {
        super.onSizeChanged(w, h, oldw, oldh)
        centerX = w / 2f
        centerY = h / 2f
        baseRadius = min(w, h) / 2f * 0.8f
        hatRadius = baseRadius * 0.3f
        joystickX = centerX
        joystickY = centerY
    }
    
    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        
        // Draw base circle
        canvas.drawCircle(centerX, centerY, baseRadius, basePaint)
        canvas.drawCircle(centerX, centerY, baseRadius, borderPaint)
        
        // Draw joystick hat
        canvas.drawCircle(joystickX, joystickY, hatRadius, hatPaint)
        canvas.drawCircle(joystickX, joystickY, hatRadius, borderPaint)
    }
    
    override fun onTouchEvent(event: MotionEvent): Boolean {
        when (event.action) {
            MotionEvent.ACTION_DOWN,
            MotionEvent.ACTION_MOVE -> {
                val dx = event.x - centerX
                val dy = event.y - centerY
                val distance = sqrt(dx.pow(2) + dy.pow(2))
                
                if (distance < baseRadius) {
                    joystickX = event.x
                    joystickY = event.y
                } else {
                    val ratio = baseRadius / distance
                    joystickX = centerX + dx * ratio
                    joystickY = centerY + dy * ratio
                }
                
                // Calculate angle (0-360 degrees, 0 = right, increasing counterclockwise)
                val angle = Math.toDegrees(atan2(-dy.toDouble(), dx.toDouble()))
                val normalizedAngle = if (angle < 0) angle + 360 else angle
                
                // Calculate strength (0-100)
                val strength = min(distance / baseRadius * 100, 100.0)
                
                onJoystickMoveListener?.invoke(normalizedAngle, strength)
                invalidate()
                return true
            }
            
            MotionEvent.ACTION_UP,
            MotionEvent.ACTION_CANCEL -> {
                joystickX = centerX
                joystickY = centerY
                onJoystickMoveListener?.invoke(0.0, 0.0)
                invalidate()
                return true
            }
        }
        return super.onTouchEvent(event)
    }
}

import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStatus()
  }, [])

  const fetchStatus = async () => {
    try {
      const response = await fetch('/api/status')
      const data = await response.json()
      setStatus(data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching status:', error)
      setLoading(false)
    }
  }

  const sendCommand = async (direction, speed = 50) => {
    try {
      const response = await fetch(`/api/move?direction=${direction}&speed=${speed}`, {
        method: 'POST',
      })
      const data = await response.json()
      console.log('Command sent:', data)
      await fetchStatus()
    } catch (error) {
      console.error('Error sending command:', error)
    }
  }

  return (
    <div className="app">
      <header>
        <h1>🦽 Wheelchair Bot Controller</h1>
      </header>

      <main>
        <div className="status-panel">
          <h2>Status</h2>
          {loading ? (
            <p>Loading...</p>
          ) : status ? (
            <div className="status-info">
              <p><strong>Battery:</strong> {status.battery_level}%</p>
              <p><strong>Moving:</strong> {status.is_moving ? 'Yes' : 'No'}</p>
              <p><strong>Speed:</strong> {status.speed}</p>
              <p><strong>Direction:</strong> {status.direction || 'None'}</p>
            </div>
          ) : (
            <p>Unable to load status</p>
          )}
        </div>

        <div className="control-panel">
          <h2>Controls</h2>
          <div className="controls">
            <div className="control-row">
              <button onClick={() => sendCommand('forward')}>↑ Forward</button>
            </div>
            <div className="control-row">
              <button onClick={() => sendCommand('left')}>← Left</button>
              <button onClick={() => sendCommand('stop')} className="stop">⬛ Stop</button>
              <button onClick={() => sendCommand('right')}>→ Right</button>
            </div>
            <div className="control-row">
              <button onClick={() => sendCommand('backward')}>↓ Backward</button>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App

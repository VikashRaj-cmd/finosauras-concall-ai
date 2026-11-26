import { useEffect, useRef, useState } from "react"
import { WS_URL } from "../config"

export function useWebSocket(onMessage) {
  const [connected, setConnected] = useState(false)
  const ws = useRef(null)

  useEffect(() => {
    function connect() {
      ws.current = new WebSocket(WS_URL)
      ws.current.onopen = () => setConnected(true)
      ws.current.onmessage = (e) => {
        try { onMessage(JSON.parse(e.data)) } catch {}
      }
      ws.current.onclose = () => {
        setConnected(false)
        setTimeout(connect, 3000)
      }
      ws.current.onerror = () => ws.current.close()
    }
    connect()
    return () => ws.current?.close()
  }, [])

  return connected
}

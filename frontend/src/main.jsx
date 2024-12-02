import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'

newrelic.wrapLogger(console, 'info')
// from this point forward, every time `console.info` is invoked, it will save a log event

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

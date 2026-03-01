import { GoogleOAuthProvider } from '@react-oauth/google';
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import './global.css'
import App from './App.jsx'

const GOOGLE_CLIENT_ID = "376342460609-ofrk29a5ss5hrigdg58ae2cjj1mvaqhk.apps.googleusercontent.com";

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <App />
    </GoogleOAuthProvider>
  </StrictMode>,
)

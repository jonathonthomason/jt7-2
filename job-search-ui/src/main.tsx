import ReactDOM from 'react-dom/client'
import App from './App'

async function start() {
if (import.meta.env.VITE_ENABLE_MSW === 'true') {
const { worker } = await import('./mocks/browser')
await worker.start()
}

ReactDOM.createRoot(document.getElementById('root')!).render(<App />)
}

start()

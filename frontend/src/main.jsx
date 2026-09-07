import { createRoot } from 'react-dom/client'
import { RouterProvider } from 'react-router/dom'
import { ShoppingCartProvider } from './context/ShoppingCartContext.jsx'
import './index.css'
import router from './routes/routes.jsx'

createRoot(document.getElementById('root')).render(
    <ShoppingCartProvider>
        <RouterProvider router={router} />
    </ShoppingCartProvider>,
)

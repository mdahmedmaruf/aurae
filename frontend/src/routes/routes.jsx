import { createBrowserRouter } from 'react-router'
import App from '../App'
import Root from '../layouts/Root'
import CartPage from '../pages/CartPage'
import ProductList from '../pages/ProductList'

const router = createBrowserRouter([
    {
        path: '/',
        Component: Root,
        children: [
            { index: true, Component: App },
            { path: 'products', Component: ProductList },
            { path: 'cart', Component: CartPage },
        ],
    },
])

export default router

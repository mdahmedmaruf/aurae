import { createContext, useContext, useEffect, useState } from 'react'

const ShoppingCartContext = createContext(null)

export function ShoppingCartProvider({ children }) {
    const [cartItems, setCartItems] = useState(() => {
        const saveCart = localStorage.getItem('shopping_cart')
        return saveCart ? JSON.parse(saveCart) : []
    })
    const [toast, setToast] = useState(null)

    useEffect(() => {
        localStorage.setItem('shopping_cart', JSON.stringify(cartItems))
    }, [cartItems])

    const triggerToast = (message) => {
        setToast(message)

        const timer = setTimeout(() => setToast(null), 3000)
        return () => clearTimeout(timer)
    }

    const addToCart = (product) => {
        setCartItems((prevItems) => {
            const existingItems = prevItems.find(
                (item) => item.id === product.id,
            )
            if (existingItems) {
                return prevItems.map((item) =>
                    item.id === product.id
                        ? { ...item, quantity: item.quantity + 1 }
                        : item,
                )
            }
            return [...prevItems, { ...product, quantity: 1 }]
        })
        triggerToast(`Added ${product.title} to cart!`)
    }

    const removeFromCart = (id) => {
        const itemToRemove = cartItems.find((item) => item.id === id)
        setCartItems((prevItem) => prevItem.filter((item) => item.id !== id))

        if (itemToRemove) {
            triggerToast(`Removed ${itemToRemove.title} from cart.`)
        }
    }

    const updateCart = (id, delta) => {
        setCartItems((prevItems) =>
            prevItems
                .map((item) =>
                    item.id === id
                        ? { ...item, quantity: item.quantity + delta }
                        : item,
                )
                .filter((item) => item.quantity > 0),
        )
    }

    const clearCart = () => {
        setCartItems([])
        triggerToast('Remove All Items from Your Cart.')
    }

    const totalItems = cartItems.reduce((sum, item) => sum + item.quantity, 0)
    const totalPrice = cartItems.reduce(
        (sum, item) => sum + item.quantity * item.price,
        0,
    )

    const values = {
        cartItems,
        addToCart,
        removeFromCart,
        updateCart,
        clearCart,
        totalItems,
        totalPrice,
    }
    return (
        <ShoppingCartContext value={values}>
            {children}
            {toast && (
                <div className='absolute bottom-2 right-2 p-3 rounded-lg shadow-sm transition-transform delay-150 duration-200 ease-in-out'>
                    {toast}
                </div>
            )}
        </ShoppingCartContext>
    )
}

// eslint-disable-next-line react-refresh/only-export-components
export function useCart() {
    const context = useContext(ShoppingCartContext)

    if (!context)
        throw new Error('userCart must be used withing a CartProvider')

    return context
}

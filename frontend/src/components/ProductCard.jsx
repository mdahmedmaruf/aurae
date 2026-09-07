import { useCart } from '../context/ShoppingCartContext'

export default function ProductCard({ product }) {
    const { image_url, title, price } = product
    const { addToCart, cartItems } = useCart()

    console.log(cartItems)

    return (
        <div className='border border-gray-200 p-4'>
            <img
                src={image_url}
                alt={title}
                className='w-full h-96 object-contain'
            />
            {/* <p>{category}</p> */}
            <h2 className='text-base font-archivo uppercase truncate leading-6 text-gray-600 pt-2'>
                {title}
            </h2>
            <p className='text-base font-archivo uppercase leading-6 text-gray-500'>
                USD{price}
            </p>
            <button
                onClick={() => addToCart(product)}
                className='text-base font-archivo uppercase tracking-wide leading-6 text-gray-500 cursor-pointer'
            >
                Add to Cart
            </button>
        </div>
    )
}

import { Link } from 'react-router'
import { useCart } from '../context/ShoppingCartContext'

export default function Header() {
    const { cartItems } = useCart()

    return (
        <div className='flex items-center justify-items-center border-b border-gray-200 py-4 px-10 absolute left-0 w-full'>
            <div className='basis-1/5 flex justify-start'>
                <div className='font-archivo text-base uppercase tracking-wide leading-6 text-gray-500 flex gap-2'>
                    <Link to={`/`}>Home</Link>
                    <Link to={`/`}>About</Link>
                    <Link to={`/`}>Contact</Link>
                </div>
            </div>
            <div className='basis-full flex justify-center'>
                <h2 className='font-tensor font-bold uppercase text-3xl'>
                    <Link to={`/`}>aurae</Link>
                </h2>
            </div>
            <div className='basis-1/5 flex justify-end'>
                <div className='flex gap-2 text-gray-500'>
                    <span>
                        <svg
                            xmlns='http://www.w3.org/2000/svg'
                            viewBox='0 0 24 24'
                            width='24'
                            height='24'
                            color='currentColor'
                            fill='none'
                            stroke='currentColor'
                            strokeWidth='1.5'
                            strokeLinecap='round'
                            strokeLinejoin='round'
                        >
                            <circle cx='12' cy='7' r='4'></circle>
                            <path d='M12 14C7 14 4 16.5 4 19C4 20.1046 4.89543 21 6 21H18C19.1046 21 20 20.1046 20 19C20 16.5 17 14 12 14Z'></path>
                        </svg>
                    </span>
                    <span>
                        <svg
                            xmlns='http://www.w3.org/2000/svg'
                            viewBox='0 0 24 24'
                            width='24'
                            height='24'
                            color='currentColor'
                            fill='none'
                            stroke='currentColor'
                            strokeWidth='1.5'
                            strokeLinecap='round'
                            strokeLinejoin='round'
                        >
                            <path d='M10.4107 19.9677C7.58942 17.858 2 13.0348 2 8.69444C2 5.82563 4.10526 3.5 7 3.5C8.5 3.5 10 4 12 6C14 4 15.5 3.5 17 3.5C19.8947 3.5 22 5.82563 22 8.69444C22 13.0348 16.4106 17.858 13.5893 19.9677C12.6399 20.6776 11.3601 20.6776 10.4107 19.9677Z'></path>
                        </svg>
                    </span>
                    <span className='relative'>
                        {cartItems &&
                            cartItems.map((item) => (
                                <span className='absolute -right-3 -top-3 font-archivo text-xs bg-gray-700 text-white px-1.5 py-0.5 rounded-full'>
                                    {item.quantity}
                                </span>
                            ))}
                        <Link to={`/cart`}>
                            <svg
                                xmlns='http://www.w3.org/2000/svg'
                                viewBox='0 0 24 24'
                                width='24'
                                height='24'
                                color='currentColor'
                                fill='none'
                                stroke='currentColor'
                                strokeWidth='1.5'
                                strokeLinecap='round'
                                strokeLinejoin='round'
                            >
                                <path d='M8 7H16C17.8856 7 18.8284 7 19.4142 7.58579C20 8.17157 20 9.11438 20 11V15C20 18.2998 20 19.9497 18.9749 20.9749C17.9497 22 16.2998 22 13 22H11C7.70017 22 6.05025 22 5.02513 20.9749C4 19.9497 4 18.2998 4 15V11C4 9.11438 4 8.17157 4.58579 7.58579C5.17157 7 6.11438 7 8 7Z'></path>
                                <path d='M16 9.5C16 5.63401 14.2091 2 12 2C9.79086 2 8 5.63401 8 9.5'></path>
                            </svg>
                        </Link>
                    </span>
                </div>
            </div>
        </div>
    )
}

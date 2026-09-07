import { useEffect, useState } from 'react'

import API from '../api/client'
import ProductCard from '../components/ProductCard'

export default function ProductList() {
    const [products, setProducts] = useState([])
    const [loading, setLoading] = useState(true)

    const fetchProducts = async () => {
        try {
            const response = await API.get('/products')
            setProducts(response.data)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchProducts()
    }, [])

    if (loading)
        return (
            <div className='font-tensor text-lg uppercase text-gray-500 text-center p-8'>
                Loading products...
            </div>
        )

    return (
        <div className='max-w-6xl mx-auto p-6'>
            <h1 className='font-tensor uppercase text-3xl font-bold text-gray-700 mb-6'>
                Products
            </h1>
            <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6'>
                {products.map((product) => (
                    <ProductCard key={product.id} product={product} />
                ))}
            </div>
        </div>
    )
}

export default function HeroSection() {
    return (
        <div className='bg-[url("/hero-bg.png")] bg-no-repeat bg-cover bg-bottom-right bg-amber-200 h-screen w-full flex items-center'>
            <div>
                <h1 className='font-archivo text-6xl'>
                    Welcome to <strong>Aurae</strong> Clothing Store
                </h1>
                <div className='flex gap-3'>
                    <button className='font-archivo uppercase text-white bg-gray-800 py-2 px-6'>
                        Shop Now
                    </button>
                    <button className='font-archivo uppercase text-gray-800 border border-gray-800 bg-transparent py-2 px-6'>
                        Learn More
                    </button>
                </div>
            </div>
        </div>
    )
}

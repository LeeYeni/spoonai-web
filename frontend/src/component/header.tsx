import Image from "next/image";

export default function Header() {
    return (
        <header className="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur-md">
            <div className="container mx-auto px-4 h-16 flex items-center gap-3">
                <Image 
                    src="/logo.png" 
                    alt="Spoon AI Logo" 
                    width={36} 
                    height={36} 
                    className="rounded-md object-contain"
                />
                <span className="text-xl font-extrabold text-orange-500 tracking-tighter">
                    Spoon AI
                </span>
            </div>
        </header>
    );
}
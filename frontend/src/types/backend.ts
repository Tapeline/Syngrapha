export type Transaction = {
    id: string;
    merchant: string;
    time: string;
    cost: number;
    products: Product[];
}

export type Product = {
    id: string;
    transaction: string;
    time: string;
    merchant: string;
    name: string;
    quantity: number;
    price: number;
    cost: number;
    category: string | null;
}

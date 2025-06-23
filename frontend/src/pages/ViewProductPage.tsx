import {useMenu} from "../hooks/menu.ts";
import {useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import FillingPreloader from "../components/widgets/FillingPreloader.tsx";
import {MotionEffect} from "../components/animate-ui/effects/motion-effect.tsx";
import type {Product} from "../types/backend.ts";
import {getProduct} from "../api/transactions.ts";
import {useAuthStore} from "../hooks/auth.ts";
import {Table, TableBody, TableCell, TableRow} from "../components/ui/table.tsx";
import {EditIcon} from "lucide-react";
import {Button} from "../components/ui/button.tsx";

export default function ViewProductPage() {
    const {setPageTitle, setPageMenu} = useMenu();
    const {accessToken} = useAuthStore();
    const {transId, prodId} = useParams();
    const [isLoading, setIsLoading] = useState(true);
    const [product, setProduct] = useState<Product | null>(null);
    const [errorName, setErrorName] = useState<string | null>(null)
    useEffect(() => {
        setPageTitle([
            {title: "Transactions", href: "/transactions"},
            {
                title: transId?.toString().substring(0, 8) || "",
                href: `/transactions/${transId}`
            },
            {
                title: prodId?.toString().substring(0, 8) || "",
                href: `/transactions/${transId}/${prodId}`
            },
        ]);
        setPageMenu({
            title: "On this page",
            items: [
                {"title": "Back to list", "action": "/transactions"},
                {"title": "Back to transaction", "action": `/transactions/${transId}`}
            ],
        });
        getProduct(accessToken, transId||"", prodId||"").then(resp => {
            setErrorName(null)
            if (resp.status === 404) setErrorName("not_found");
            else if (resp.status === 200) setProduct(resp.data)
            else setErrorName("unknown");
            setIsLoading(false);
        })
    }, [transId])
    if (isLoading || !product)
        return <FillingPreloader/>;
    if (errorName === "not_found")
        return <MotionEffect slide><p>Not found</p></MotionEffect>;
    if (errorName === "unknown")
        return <MotionEffect slide><p>Unknown error</p></MotionEffect>;
    return <MotionEffect slide>
        <h2 className="text-4xl md:text-3xl">Product detail</h2>
        <small>{product.id}</small>
        <br/>
        <Table className="mt-3">
            <TableBody>
                <TableRow>
                    <TableCell>Name</TableCell>
                    <TableCell>{product.name}</TableCell>
                    <TableCell></TableCell>
                </TableRow>
                <TableRow>
                    <TableCell>Category</TableCell>
                    <TableCell>{product.category}</TableCell>
                    <TableCell>
                        <Button><EditIcon/></Button>
                    </TableCell>
                </TableRow>
                <TableRow>
                    <TableCell>Price</TableCell>
                    <TableCell>{product.price / 100}</TableCell>
                    <TableCell></TableCell>
                </TableRow>
                <TableRow>
                    <TableCell>Quantity</TableCell>
                    <TableCell>{product.quantity}</TableCell>
                    <TableCell></TableCell>
                </TableRow>
                <TableRow>
                    <TableCell>Cost</TableCell>
                    <TableCell>{product.cost / 100}</TableCell>
                    <TableCell></TableCell>
                </TableRow>
            </TableBody>
        </Table>
    </MotionEffect>
}

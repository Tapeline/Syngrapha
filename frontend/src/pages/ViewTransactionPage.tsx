import {useMenu} from "../hooks/menu.ts";
import {NavLink, useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import FillingPreloader from "../components/widgets/FillingPreloader.tsx";
import {MotionEffect} from "../components/animate-ui/effects/motion-effect.tsx";
import type {Transaction} from "../types/backend.ts";
import {getTransaction} from "../api/transactions.ts";
import {useAuthStore} from "../hooks/auth.ts";
import {Table, TableBody, TableCell, TableFooter, TableHeader, TableRow} from "../components/ui/table.tsx";
import {EyeIcon} from "lucide-react";
import {Button} from "../components/ui/button.tsx";

export default function ViewTransactionPage() {
    const {setPageTitle, setPageMenu} = useMenu();
    const {accessToken} = useAuthStore();
    const {transId} = useParams();
    const [isLoading, setIsLoading] = useState(true);
    const [transaction, setTransaction] = useState<Transaction | null>(null);
    const [errorName, setErrorName] = useState<string | null>(null)
    useEffect(() => {
        setPageTitle([
            {title: "Transactions", href: "/transactions"},
            {
                title: transId?.toString().substring(0, 8) || "",
                href: `/transactions/${transId}`
            },
        ]);
        setPageMenu({
            title: "On this page",
            items: [{"title": "Back", "action": "/transactions"}]
        });
        getTransaction(accessToken, transId||"").then(resp => {
            setErrorName(null)
            if (resp.status === 404) setErrorName("not_found");
            else if (resp.status === 200) setTransaction(resp.data)
            else setErrorName("unknown");
            setIsLoading(false);
        })
    }, [transId])
    if (isLoading || !transaction)
        return <FillingPreloader/>;
    if (errorName === "not_found")
        return <MotionEffect slide><p>Not found</p></MotionEffect>;
    if (errorName === "unknown")
        return <MotionEffect slide><p>Unknown error</p></MotionEffect>;
    return <MotionEffect slide>
        <h2 className="text-4xl md:text-3xl">Transaction detail</h2>
        <small>{transaction.id}</small>
        <br/>
        <Table className="mt-3">
            <TableBody>
                <TableRow>
                    <TableCell>Date</TableCell>
                    <TableCell>{transaction.time}</TableCell>
                </TableRow>
                <TableRow>
                    <TableCell>Merchant</TableCell>
                    <TableCell>{transaction.merchant}</TableCell>
                </TableRow>
            </TableBody>
        </Table>
        <h3 className="mt-3">Products</h3>
        <Table>
            <TableHeader>
                <TableRow>
                    <TableCell style={{width: "64px"}}>View</TableCell>
                    <TableCell>Name</TableCell>
                    <TableCell style={{width: "64px"}}>Category</TableCell>
                    <TableCell>Price</TableCell>
                    <TableCell>Qty</TableCell>
                    <TableCell>Cost</TableCell>
                </TableRow>
            </TableHeader>
            <TableBody>
                {transaction.products.map((prod) => (
                  <TableRow key={prod.id}>
                    <TableCell>
                        <Button variant="outline" asChild>
                            <NavLink to={
                                `/transactions/${transId}/${prod.id}`
                            }>
                                <EyeIcon/>
                            </NavLink>
                        </Button>
                    </TableCell>
                    <TableCell>{prod.name}</TableCell>
                    <TableCell>{prod.category}</TableCell>
                    <TableCell>{prod.price / 100}</TableCell>
                    <TableCell>{prod.quantity}</TableCell>
                    <TableCell>{prod.cost / 100}</TableCell>
                  </TableRow>
                ))}
            </TableBody>
            <TableFooter>
                <TableRow>
                    <TableCell colSpan={5}>Total</TableCell>
                    <TableCell>{transaction.cost / 100}</TableCell>
                </TableRow>
            </TableFooter>
        </Table>
    </MotionEffect>
}

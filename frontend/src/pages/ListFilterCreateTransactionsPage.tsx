"use client"

import {useMenu} from "../hooks/menu.ts";
import {useEffect, useState} from "react";
import FillingPreloader from "../components/widgets/FillingPreloader.tsx";
import {
    Tabs,
    TabsContent,
    TabsContents,
    TabsList,
    TabsTrigger
} from "../components/animate-ui/radix/tabs.tsx";
import {MotionEffect} from "../components/animate-ui/effects/motion-effect.tsx";
import {Button} from "../components/ui/button.tsx";
import {CheckIcon, EyeIcon, Loader2, ScanQrCodeIcon, TableCellsMergeIcon} from "lucide-react";
import {
    Dialog,
    DialogContent, DialogFooter,
    DialogHeader, DialogTitle,
    DialogTrigger
} from "../components/animate-ui/radix/dialog.tsx";
import {z} from "zod";
import {useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel, FormMessage
} from "../components/ui/form.tsx";
import {Input} from "../components/ui/input.tsx";
import type {Product, Transaction} from "../types/backend.ts";
import {createTransactionQR, getTransactions} from "../api/transactions.ts";
import {useAuthStore} from "../hooks/auth.ts";
import {useToaster} from "../hooks/toast.ts";
import { type ColumnDef } from "@tanstack/react-table";
import {DataTable} from "../components/widgets/DataTable.tsx";
import {createTransactionFromTable} from "../api/transactions.ts";
import {NavLink} from "react-router-dom";
import {DatePicker} from "../components/widgets/date-picker.tsx";
import BarcodeScanner from "react-qr-barcode-scanner";


const formSchema = z.object({
    table: z.instanceof(FileList)
        .refine(
            (file) =>
                file?.length == 1 && file?.item(0)?.name.endsWith(".csv"),
            "Exactly one .csv is required"
        )
})


function CreateDialog({token}) {
    const [isLoading, setIsLoading] = useState(false);
    const [isOpen, setIsOpen] = useState(false);
    const {toast} = useToaster();
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {},
    })
    const tableRef = form.register("table");
    const onSubmit = (values: z.infer<typeof formSchema>) => {
        setIsLoading(true);
        createTransactionFromTable(token, values.table).then(resp => {
            if (!resp.success || !resp.data) toast("Failed to create from table");
            setIsLoading(false);
            setIsOpen(false);
        })
    }
    return <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogTrigger asChild>
            <Button variant="outline" className="w-full my-3 lg:w-[128px]">
                <span><TableCellsMergeIcon className="inline"/> From table</span>
            </Button>
        </DialogTrigger>
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Import transactions from table</DialogTitle>
            </DialogHeader>
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                    <FormField
                        control={form.control}
                        name="table"
                        render={() => {
                            return (
                                <FormItem>
                                    <FormLabel>Table (.csv)</FormLabel>
                                    <FormControl>
                                        <Input
                                            type="file"
                                            placeholder="shadcn" {...tableRef}
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            );
                        }}
                    />
                    <DialogFooter>
                        <Button type="submit" disabled={isLoading}>
                            {isLoading && <Loader2 className="mr-2 h-5 w-5 animate-spin"/>}
                            Import
                        </Button>
                        <Button onClick={() => setIsOpen(false)} variant="outline">
                            Close
                        </Button>
                    </DialogFooter>
                </form>
            </Form>
        </DialogContent>
    </Dialog>
}

function CreateQRDialog({token, refreshList}) {
    const [isLoading, setIsLoading] = useState(false);
    const [isOpen, setIsOpen] = useState(false);
    const [scannedText, setScannedText] = useState<string | null>(null);
    const {toast} = useToaster();
    const onSubmit = (e) => {
        e.preventDefault()
        setIsLoading(true);
        createTransactionQR(token, scannedText).then(resp => {
            if (!resp.data) toast("Unknown error");
            else if (
                !resp.success && resp.data.code === "nalog_token_requires_re_auth"
            ) toast("You need to re-login at nalog.ru");
            setIsLoading(false);
            setIsOpen(false);
            setScannedText(null);
            refreshList();
        })
    }
    return <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogTrigger asChild>
            <Button className="w-full my-3 lg:w-[128px]">
                <span><ScanQrCodeIcon className="inline"/> From QR</span>
            </Button>
        </DialogTrigger>
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Import transactions from QR</DialogTitle>
            </DialogHeader>
            {isOpen && !scannedText &&
                <BarcodeScanner
                    width={500}
                    height={500}
                    onUpdate={(err, result) => {
                        if (result) setScannedText(result.text);
                    }}
                />
            }
            {scannedText &&
                <div className="flex items-center justify-center w-full h-full">
                    <CheckIcon/>
                </div>
            }
            <DialogFooter>
                <Button onClick={onSubmit} disabled={isLoading}>
                    {isLoading && <Loader2 className="mr-2 h-5 w-5 animate-spin"/>}
                    Import
                </Button>
                <Button onClick={() => setIsOpen(false)} variant="outline">
                    Close
                </Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
}

export const transactionColumns: ColumnDef<Transaction>[] = [
    {accessorKey: "id", enableHiding: true},
    {
        id: "view",
        cell: ({row}) => <Button variant="outline" asChild>
            <NavLink to={`/transactions/${row.getValue("id")}`}>
                <EyeIcon/>
            </NavLink>
        </Button>,
        maxSize: 64
    },
    {
        accessorKey: "time",
        header: "Date",
    },
    {
        accessorKey: "merchant",
        header: "Merchant",
    },
    {
        accessorKey: "cost",
        header: "Cost",
        cell: ({ row }) =>
            <div className="text-right font-medium">{
                row.getValue("cost") / 100
            }</div>,
    },
]
export const productColumns: ColumnDef<Product>[] = [
    {accessorKey: "id", enableHiding: true},
    {accessorKey: "transaction", enableHiding: true},
    {
        id: "view",
        cell: ({row}) => <Button variant="outline" asChild>
            <NavLink to={`/transactions/${row.getValue("transaction")}/${row.getValue("id")}`}>
                <EyeIcon/>
            </NavLink>
        </Button>,
        size: 64,
        minSize: 64,
        maxSize: 64
     },
    {
        accessorKey: "time",
        header: "Date",
    },
    {
        accessorKey: "category",
        header: "Category",
    },
    {
        accessorKey: "name",
        header: "Product",
    },
    {
        accessorKey: "cost",
        header: "Cost",
        cell: ({ row }) =>
            <div className="text-right font-medium">{
                row.getValue("cost") / 100
            }</div>,
    },
]

export default function ListFilterCreateTransactionsPage() {
    const {setPageTitle, setPageMenu} = useMenu();
    const {accessToken} = useAuthStore();
    const {toast} = useToaster();
    const [isLoading, setIsLoading] = useState(true);
    const [transactions, setTransactions] = useState<Array<Transaction> | null>(null);
    const [products, setProducts] = useState<Array<Product> | null>(null);
    const [filterBefore, setFilterBefore] = useState<Date | null>(null);
    const [filterSince, setFilterSince] = useState<Date | null>(null);
    const [listRefresher, setListRefresher] = useState(false);

    useEffect(() => {
        setPageTitle([{title: "Transactions", href: "/transactions"}]);
        setPageMenu(null);
        getTransactions(
            accessToken,
            filterSince?.toISOString(),
            filterBefore?.toISOString()
        ).then(resp => {
            if (!resp.success) toast("Cannot load transactions");
            else {
                setTransactions(resp.data);
                const prods: Product[] = [];
                for (const trans of resp.data)
                    for (const product of trans.products)
                        prods.push({
                            id: product.id,
                            transaction: trans.id,
                            merchant: trans.merchant,
                            time: trans.time,
                            name: product.name,
                            category: product.category,
                            quantity: product.quantity,
                            cost: product.cost,
                            price: product.price
                        })
                setProducts(prods)
            }
            setIsLoading(false);
        })
    }, [filterBefore, filterSince, listRefresher]);
    if (isLoading || !transactions || !products)
        return <FillingPreloader/>;

    return <MotionEffect slide>
        <h2 className="text-4xl md:text-3xl">Your expenses</h2>
        <br/>
        <div className="grid grid-cols-2 grid-rows-1 gap-4 md:flex">
            <CreateQRDialog token={accessToken} refreshList={() => {
                setListRefresher(!listRefresher);
            }}/>
            <CreateDialog token={accessToken}/>
        </div>
        <div className="grid grid-cols-2 grid-rows-1 gap-4 md:flex">
            <DatePicker label="From" initial={filterSince} onChange={setFilterSince}/>
            <DatePicker label="To" initial={filterBefore} onChange={setFilterBefore}/>
        </div>

        <Tabs defaultValue="transactions" className="w-full bg-muted rounded-lg mt-3">
            <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="transactions">Transactions</TabsTrigger>
                <TabsTrigger value="products">Products</TabsTrigger>
            </TabsList>

            <TabsContents className="mx-1 mb-1 -mt-2 rounded-sm h-full bg-background">
                <TabsContent value="transactions" className="space-y-6 p-3 md:p-6">
                    <DataTable
                        columns={transactionColumns}
                        data={transactions}/>
                </TabsContent>
                <TabsContent value="products" className="space-y-6 p-3 md:p-6">
                    <DataTable
                        columns={productColumns}
                        data={products}/>
                </TabsContent>
            </TabsContents>
        </Tabs>
    </MotionEffect>
}

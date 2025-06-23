import {useMenu} from "../hooks/menu.ts";
import {NavLink} from "react-router-dom";
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
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle
} from "../components/ui/card.tsx";
import {Button} from "../components/ui/button.tsx";
import {ArrowRight, Loader2} from "lucide-react";
import * as RandomImage from "../assets/huis.jpeg";
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
    FormDescription,
    FormField,
    FormItem,
    FormLabel, FormMessage
} from "../components/ui/form.tsx";
import {Input} from "../components/ui/input.tsx";
import {PlusIcon, CalendarIcon} from "lucide-react";
import {Popover, PopoverContent, PopoverTrigger} from "../components/ui/popover.tsx";
import {cn} from "../lib/utils.ts";
import {format} from "date-fns";
import {Textarea} from "../components/ui/textarea.tsx";


const formSchema = z.object({
    title: z.string()
        .min(2, {message: "title too short"})
        .max(50, {message: "title too long"}),
    text: z.string()
        .min(2, {message: "text too short"})
        .max(5000, {message: "text too long"}),
    dt: z.date(),
    num: z.number(),
    thumb: z.instanceof(FileList)
        .refine((file) => file?.length == 1, 'File is required.')
})


function CreateDialog() {
    const [isLoading, setIsLoading] = useState(false);
    const [isOpen, setIsOpen] = useState(false);
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            title: "",
            text: "",
            dt: new Date(),
            num: 0
        },
    })
    const thumbRef = form.register("thumb");
    const onSubmit = (values: z.infer<typeof formSchema>) => {
        setIsLoading(true);
        // This simulates a long-running web request
        setTimeout(() => {
            setIsLoading(false);
            setIsOpen(false);
        }, 1000);
    }
    return <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogTrigger asChild>
            <Button variant="outline" className="w-full my-3 lg:w-[192px]"
                    id="create-new-smth">
                <span><PlusIcon className="inline"/> New something</span>
            </Button>
        </DialogTrigger>
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Create something</DialogTitle>
            </DialogHeader>
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                    <FormField
                        control={form.control}
                        name="title"
                        render={({field}) => (
                            <FormItem>
                                <FormLabel>Title</FormLabel>
                                <FormControl>
                                    <Input placeholder="shadcn" {...field} />
                                </FormControl>
                                <FormDescription>
                                    This is your public title
                                </FormDescription>
                                <FormMessage/>
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="text"
                        render={({field}) => (
                            <FormItem>
                                <FormLabel>Text</FormLabel>
                                <FormControl>
                                    <Textarea
                                        placeholder="Tell us a little bit about yourself"
                                        className="resize-none"
                                        {...field}
                                    />
                                </FormControl>
                                <FormDescription>
                                    Text of your post
                                </FormDescription>
                                <FormMessage/>
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="dt"
                        render={({ field }) => (
                            <FormItem className="flex flex-col">
                                <FormLabel>Date of publication</FormLabel>
                                <Popover>
                                    <PopoverTrigger asChild>
                                        <FormControl>
                                            <Button
                                                variant={"outline"}
                                                className={cn(
                                                    "w-[240px] pl-3 text-left font-normal",
                                                    !field.value && "text-muted-foreground"
                                                )}
                                            >
                                                {field.value ? (
                                                    format(field.value, "PPP")
                                                ) : (
                                                    <span>Pick a date</span>
                                                )}
                                                <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                                            </Button>
                                        </FormControl>
                                    </PopoverTrigger>
                                    <PopoverContent className="w-auto p-0" align="start">
                                        <Calendar
                                            mode="single"
                                            selected={field.value}
                                            onSelect={field.onChange}
                                            disabled={(date) =>
                                                date > new Date() || date < new Date("1900-01-01")
                                            }
                                            initialFocus
                                        />
                                    </PopoverContent>
                                </Popover>
                                <FormDescription>
                                    Set publication date
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="num"
                        render={({field}) => (
                            <FormItem>
                                <FormLabel>Cost</FormLabel>
                                <FormControl>
                                    <Input {...field} />
                                </FormControl>
                                <FormDescription>
                                    Cost of a single view
                                </FormDescription>
                                <FormMessage/>
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="thumb"
                        render={() => {
                            return (
                                <FormItem>
                                    <FormLabel>Thumbnail</FormLabel>
                                    <FormControl>
                                        <Input
                                            type="file"
                                            placeholder="shadcn" {...thumbRef}

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
                        Create
                    </Button>
                        <Button onClick={() => setIsOpen(false)} variant="outline">
                            Close</Button>
                    </DialogFooter>
                </form>
            </Form>
        </DialogContent>
    </Dialog>
}


export default function ListFilterCreatePage() {
    const {setPageTitle, setPageMenu} = useMenu();
    const [isLoading, setIsLoading] = useState(true);
    const [objects, setObjects] = useState<Array<{
        title: string,
        description: string
    }> | null>(null);
    useEffect(() => {
        setPageTitle([{title: "Something", href: "/something"}]);
        setPageMenu(null);
        // TODO replace
        // This simulates a long-running web request
        setTimeout(() => {
            setObjects([
                {title: "Lorem ipsum", description: "Lorem ipsum dolor sit amet"},
                {title: "Lorem ipsum", description: "Lorem ipsum dolor sit amet"},
                {title: "Lorem ipsum", description: "Lorem ipsum dolor sit amet"},
            ])
            setIsLoading(false);
        }, 1000);
    }, []);
    if (isLoading || !objects)
        return <FillingPreloader/>;
    return <MotionEffect slide>
        <h2 className="text-4xl md:text-3xl">Something list</h2>
        <small>Here you can explore something or create new somethings</small>
        <br/>
        <CreateDialog/>

        <Tabs defaultValue="all" className="w-full bg-muted rounded-lg mt-3"
              id="something-list">
            <TabsList className="grid w-full grid-cols-2" id="something-list-selector">
                <TabsTrigger value="all">All somethings</TabsTrigger>
                <TabsTrigger value="my">My somethings</TabsTrigger>
            </TabsList>

            <TabsContents className="mx-1 mb-1 -mt-2 rounded-sm h-full bg-background">
                <TabsContent value="all" className="space-y-6 p-3 md:p-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {objects.map((obj, index) => (
                            <Card key={index}>
                                <CardHeader>
                                    <CardTitle>{obj.title}</CardTitle>
                                    <CardDescription>{obj.title}</CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <p>{obj.description}</p>
                                </CardContent>
                                <CardFooter>
                                    <Button asChild className="w-full">
                                        <NavLink to="/something/a">
                                            <ArrowRight/> Go to page
                                        </NavLink>
                                    </Button>
                                </CardFooter>
                            </Card>
                        ))}
                    </div>
                </TabsContent>
                <TabsContent value="my" className="space-y-6 p-3 md:p-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {objects.map((obj, index) => (
                            <Card key={index} className="pt-0">
                                <img className="shad-card-img" src={RandomImage.default}/>
                                <CardHeader>
                                    <CardTitle>{obj.title}</CardTitle>
                                    <CardDescription>{obj.title}</CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <p>{obj.description}</p>
                                </CardContent>
                                <CardFooter>
                                    <Button asChild className="w-full">
                                        <NavLink to="/something/a">
                                            <ArrowRight/> Go to page
                                        </NavLink>
                                    </Button>
                                </CardFooter>
                            </Card>
                        ))}
                    </div>
                </TabsContent>
            </TabsContents>
        </Tabs>
    </MotionEffect>
}

import {useMenu} from "../hooks/menu.ts";
import {useEffect, useState} from "react";
import FillingPreloader from "../components/widgets/FillingPreloader.tsx";
import {MotionEffect} from "../components/animate-ui/effects/motion-effect.tsx";
import {useAuthStore} from "../hooks/auth.ts";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "../components/ui/card.tsx";
import {Avatar, AvatarFallback, AvatarImage} from "../components/ui/avatar.tsx";
import {
    UserIcon,
    BarChartIcon,
    LogOutIcon,
    Loader2, KeyIcon
} from "lucide-react";
import {Button} from "../components/ui/button.tsx";
import {useToaster} from "../hooks/toast.ts";
import {
    Dialog,
    DialogContent, DialogDescription, DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger
} from "../components/animate-ui/radix/dialog.tsx";
import {checkNalogCode, requestNalogCode, submitNalogCode} from "../api/profile.ts";
import {InputOTP, InputOTPGroup, InputOTPSlot} from "../components/ui/input-otp.tsx";

function NalogDialog({token}) {
    const [isLoading, setIsLoading] = useState(false);
    const [isOpen, setIsOpen] = useState(false);
    const [smsCode, setSmsCode] = useState("");
    const {toast} = useToaster();
    const onSubmit = (e) => {
        e.preventDefault()
        setIsLoading(true);
        submitNalogCode(token, smsCode).then(resp => {
            if (
                !resp.success && resp.status === 401
            ) toast("Bad code");
            else if (!resp.data || !resp.success) toast("Unknown error");
            setIsLoading(false);
            setIsOpen(false);
            setSmsCode(null);
        })
    }
    const request = () => {
        requestNalogCode(token).then(resp => {
            if (!resp.success) toast("Error requesting code");
        })
    }
    return <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogTrigger asChild>
            <Button className="w-full my-3" onClick={request}>
                <span><KeyIcon className="inline"/> Login at nalog.ru</span>
            </Button>
        </DialogTrigger>
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Login at nalog.ru</DialogTitle>
                <DialogDescription>An authorization code has been sent to you</DialogDescription>
            </DialogHeader>
            <form onSubmit={onSubmit} className="space-y-8">
                <InputOTP maxLength={4} onChange={setSmsCode}>
                    <InputOTPGroup>
                        <InputOTPSlot index={0}/>
                        <InputOTPSlot index={1}/>
                        <InputOTPSlot index={2}/>
                        <InputOTPSlot index={3}/>
                    </InputOTPGroup>
                </InputOTP>
                <DialogFooter>
                    <Button type="submit" disabled={isLoading}>
                        {isLoading && <Loader2 className="mr-2 h-5 w-5 animate-spin"/>}
                        Authorize
                    </Button>
                    <Button onClick={() => setIsOpen(false)} variant="outline">
                        Close
                    </Button>
                </DialogFooter>
            </form>
        </DialogContent>
    </Dialog>
}

function CheckNalogAuthButton({token}) {
    const [isValid, setIsValid] = useState<boolean | null>(null);
    return <>
        <Button className="w-full my-3" onClick={() => {
            checkNalogCode(token).then(resp => {
                setIsValid(resp?.data?.is_valid)
            })
        }} variant={
            isValid === null
                ? "default"
                : (isValid
                    ? "outline"
                    : "destructive")
        }>
            {isValid === null && "Check nalog.ru authorization"}
            {isValid === true && "Authorized"}
            {isValid === false && "Not authorized"}
        </Button>
    </>
}

export default function ViewAccountPage() {
    const {setPageTitle, setPageMenu} = useMenu();
    const {userData, logout, accessToken} = useAuthStore();
    const [isLoading, setIsLoading] = useState(true);
    useEffect(() => {
        setPageTitle([{title: "Account"}, {title: "My"},]);
        setPageMenu(null)
        setIsLoading(false);
    }, [])
    if (isLoading)
        return <FillingPreloader/>;
    return <MotionEffect slide>
        <Card className="w-full">
            <CardContent>
                <div className="flex justify-between flex-row">
                    <div className="flex gap-3 items-center mb-2">
                        <Avatar className="h-8 w-8 rounded-lg">
                            <AvatarImage src={userData?.avatar} alt={userData?.username}/>
                            <AvatarFallback className="rounded-lg">
                                <UserIcon/>
                            </AvatarFallback>
                        </Avatar>
                        <div className="flex flex-col">
                            <b>{userData?.username}</b>
                            <span>{userData?.email}</span>
                        </div>
                    </div>
                    <Button variant="destructive" onClick={() => {
                        logout()
                        window.location.href = "/auth/login";
                    }} className="text-white">
                        <LogOutIcon className="inline"/>
                    </Button>
                </div>
                {/*<div className="grid grid-cols-1 md:grid-cols-2 gap-4">*/}
                {/*    <NalogDialog token={accessToken}/>*/}
                {/*    <CheckNalogAuthButton token={accessToken}/>*/}
                {/*</div>*/}
                <h6 className="mt-[32px]"><b>Bio</b></h6>
                <p>Lorem ipsum dolor sit amet </p>
                <h6 className="mt-[32px]"><b>Stats</b></h6>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <Card className="m-2">
                        <CardHeader>
                            <CardTitle><BarChartIcon className="inline"/> Some stat</CardTitle>
                            <CardDescription>Means something.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <span className="text-2xl">99</span>
                        </CardContent>
                    </Card>
                    <Card className="m-2">
                        <CardHeader>
                            <CardTitle><BarChartIcon className="inline"/> Some stat</CardTitle>
                            <CardDescription>Means something.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <span className="text-2xl">99</span>
                        </CardContent>
                    </Card>
                    <Card className="m-2">
                        <CardHeader>
                            <CardTitle><BarChartIcon className="inline"/> Some stat</CardTitle>
                            <CardDescription>Means something.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <span className="text-2xl">99</span>
                        </CardContent>
                    </Card>
                </div>
            </CardContent>
        </Card>
    </MotionEffect>
}

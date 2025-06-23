import {useMenu} from "../hooks/menu.ts";
import {useEffect, useState} from "react";
import FillingPreloader from "../components/widgets/FillingPreloader.tsx";
import {MotionEffect} from "../components/animate-ui/effects/motion-effect.tsx";
import {useAuthStore} from "../hooks/auth.ts";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "../components/ui/card.tsx";
import {Avatar, AvatarFallback, AvatarImage} from "../components/ui/avatar.tsx";
import {UserIcon, BarChartIcon, LogOutIcon} from "lucide-react";
import {Button} from "../components/ui/button.tsx";
import {strings} from "../i18n.ts";

export default function ViewAccountPage() {
    const {setPageTitle, setPageMenu} = useMenu();
    const {userData, logout} = useAuthStore();
    const [isLoading, setIsLoading] = useState(true);
    useEffect(() => {
        setPageTitle([{title: "Account"}, {title: "My"},]);
        setPageMenu(null)
        // TODO replace
        // This simulates a long-running web request
        setTimeout(() => {
            setIsLoading(false);
        }, 2000);
    }, [])
    if (isLoading)
        return <FillingPreloader/>;
    return <MotionEffect slide>
        <Card className="w-full">
            <CardContent>
                <div className="flex justify-between flex-col md:flex-row">
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
                        <LogOutIcon className="inline"/> {strings.logoutAction}
                    </Button>
                </div>
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

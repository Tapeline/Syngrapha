import {useMenu} from "../hooks/menu.ts";
import {useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import FillingPreloader from "../components/widgets/FillingPreloader.tsx";
import {MotionEffect} from "../components/animate-ui/effects/motion-effect.tsx";

export default function ViewSomethingPage() {
    const {setPageTitle, setPageMenu} = useMenu();
    const {someId} = useParams();
    const [isLoading, setIsLoading] = useState(true);
    useEffect(() => {
        setPageTitle([
            {title: "Something", href: "/something"},
            {title: someId?.toString() || ""},
        ]);
        setPageMenu({
            title: "On this page",
            items: [{"title": "Info", "action": () => alert("Info!")}]
        });
        // TODO replace
        // This simulates a long-running web request
        setTimeout(() => {
            setIsLoading(false);
        }, 2000);
    }, [])
    if (isLoading)
        return <FillingPreloader/>;
    return <MotionEffect slide>
        <p>Some content loaded</p>
    </MotionEffect>
}

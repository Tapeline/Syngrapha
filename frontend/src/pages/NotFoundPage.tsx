import {RollingText} from "../components/animate-ui/text/rolling.tsx";
import {Button} from "../components/ui/button.tsx";
import {NavLink} from "react-router-dom";
import {strings} from "../i18n.ts";

export default function NotFoundPage() {
    return <div className="flex min-h-svh flex-col 
    items-center justify-center bg-muted p-6 md:p-10">
        <RollingText className="text-6xl m-5" text="404" transition={
            {
                duration: 2, delay: 0.3, ease: 'easeInOut',
                repeat: Infinity,
                repeatType: "loop" as const
            }
        }/>
        <p>{strings.page404}</p>
        <Button className="m-2" asChild>
            <NavLink to="/">{strings.goHome}</NavLink>
        </Button>
    </div>
}

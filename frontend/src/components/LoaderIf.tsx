import {Loader2} from "lucide-react";

export default function LoaderIf({src}: {src: boolean}) {
    if (!src) return null;
    return <Loader2 className="mr-2 h-5 w-5 animate-spin"/>
}

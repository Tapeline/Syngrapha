import {Spinner} from "../ui/spinner.tsx";

export default function FillingPreloader(props: {isLoading?: boolean}) {
    const {isLoading = true} = props;
    let cname = "flex h-full flex-col items-center justify-center p-6 md:p-10 shad-preloader";
    if (!isLoading) cname += " shad-preloader-fade";
    return <div className={cname}>
        <div className="w-full max-w-sm md:max-w-3xl">
            <Spinner/>
        </div>
    </div>
}

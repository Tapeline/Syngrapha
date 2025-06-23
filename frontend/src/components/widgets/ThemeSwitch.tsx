import {useTheme} from "../animate-ui/components/theme-provider.tsx";
import {Label} from "../ui/label.tsx";
import {Switch} from "../ui/switch.tsx";
import {strings} from "../../i18n.ts";

export default function ThemeSwitch() {
    const {theme, setTheme} = useTheme();
    return <div className="flex items-center space-x-2 px-2">
        <Switch
            checked={theme === "dark"}
            onCheckedChange={(isChecked) => {
                setTheme(isChecked? "dark" : "light");
            }}
            id="theme-change-switch"
        />
        <Label htmlFor="theme-change-switch">{strings.themeLabel}</Label>
    </div>
}

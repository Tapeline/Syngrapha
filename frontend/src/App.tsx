import './App.css'
import {Outlet} from "react-router-dom";
import {useAuthStore} from "./hooks/auth.ts";
import {Toaster} from "sonner";
import {ThemeProvider} from "./components/animate-ui/components/theme-provider.tsx";
import {useLanguage} from "./hooks/language.ts";
import {strings} from "./i18n.ts";

function App() {
    const auth = useAuthStore();
    const {language} = useLanguage();
    strings.setLanguage(language);

    if (location.pathname === "/" && auth.accessToken)
        window.location.href = "/profile"
    if (location.pathname === "/" && !auth.accessToken)
        window.location.href = "/welcome"

    return (
        <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
            <Outlet/>
            <Toaster/>
        </ThemeProvider>
    )
}

export default App

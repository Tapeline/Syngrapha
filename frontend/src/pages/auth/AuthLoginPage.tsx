import {useAuthStore} from "../../hooks/auth.ts";
import {useToaster} from "../../hooks/toast.ts";
import {useNavigate} from "react-router-dom";
import {authLogin} from "../../api/auth.ts";
import LoginForm from "../../components/login-form.tsx";
import {useState} from "react";
import {strings} from "../../i18n.ts";
import {MotionEffect} from "../../components/animate-ui/effects/motion-effect.tsx";

export default function AuthLoginPage() {
    const {setUserInfo, setLoggedIn} = useAuthStore();
    const {toast} = useToaster();
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(false);
    const onLogin = (username: string, password: string) => {
        setIsLoading(true);
        authLogin(username, password).then((result) => {
            setIsLoading(false);
            if (!result.success) {
                if (result.data.code === "authentication_failed")
                    toast(strings.noValidAccount);
                else
                    toast(strings.failedToLogin);
                return;
            }
            setLoggedIn(true);
            setUserInfo(result.data.token, result.data);
            navigate("/profile");
        });
    }
    return <div
            className="flex min-h-svh flex-col items-center justify-center bg-muted p-6 md:p-10">
        <div className="w-full max-w-sm">
            <MotionEffect slide>
                <LoginForm
                    onLogin={onLogin}
                    isLoading={isLoading}
                    isRegister={false}
                    builtins={[]}
                />
            </MotionEffect>
        </div>
    </div>
}

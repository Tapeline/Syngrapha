import {useAuthStore} from "../hooks/auth.ts";
import {useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import {authProbe} from "../api/auth.ts";

export default function RequireAuth<Children>(props: { children: Children }) {
    const {children} = props;
    const {accessToken, setLoggedIn, setUserInfo} = useAuthStore();
    const navigate = useNavigate();
    const [isProcessing, setIsProcessing] = useState(true);
    const [isOk, setIsOk] = useState(false);
    useEffect(() => {
        if (!accessToken) {
            setIsProcessing(false);
            navigate('/auth/login');
            return;
        }
        authProbe(accessToken).then((result) => {
            setIsProcessing(false);
            if (!result.success) {
                navigate("/auth/login");
                return;
            }
            setIsOk(true);
            setLoggedIn(true);
            setUserInfo(accessToken, result.data);
        });
    }, []);
    if (!isProcessing && isOk && accessToken) return children;
    else return <></>
}

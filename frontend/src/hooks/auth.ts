// TODO change
const accessTokenKey = "myapp-accessToken";
const userDataKey = "myapp-userData";
const loggedCheckKey = "myapp-loggedIn";

type AuthStore<UserT> = {
    accessToken: string | null
    userData: UserT | null,
    setUserInfo: (token: string, userData: UserT) => void,
    isLoggedIn: boolean,
    setLoggedIn: (loggedCheck: boolean) => void,
    logout: () => void,
}

/*export const _useAuthStore = create<AuthStore<any>>(
    (set) => {
        const userDataStr = localStorage.getItem(userDataKey);
        let userData: any | null = null;
        try {
            if (userDataStr) userData = JSON.parse(userDataStr);
        } catch {
            userData = null;
        }
        return {
            accessToken: localStorage.getItem(accessTokenKey),
            userData: userData,
            setUserInfo: (token: string, userInfo: any) => set(() => {
                localStorage.setItem(accessTokenKey, token)
                localStorage.setItem(userDataKey, JSON.stringify(userInfo))
                return {userData: userInfo, accessToken: token};
            }),
            loggedCheck: false,
            setLoggedCheck: (loggedCheck: boolean) => set({ loggedCheck: loggedCheck }),
            logout: () => {
                localStorage.removeItem(accessTokenKey);
                localStorage.removeItem(userDataKey);
                set({
                    loggedCheck: false,
                    userData: null,
                    accessToken: null
                })
            },
            refresh: () => {
                const userDataStr = localStorage.getItem(userDataKey);
                let userData: any | null = null;
                try {
                    if (userDataStr) userData = JSON.parse(userDataStr);
                } catch {
                    userData = null;
                }
                return {userData: userData, accessToken: localStorage.getItem(accessTokenKey)};
            }
        }
    }
)*/


export function useAuthStore(): AuthStore<any> {
    const accessToken = localStorage.getItem(accessTokenKey);
    const userDataStr = localStorage.getItem(userDataKey);
    const loggedCheck = (
        localStorage.getItem(loggedCheckKey) === "true"
    );
    let userData: any | null = null;
    try {
        if (userDataStr) userData = JSON.parse(userDataStr);
    } catch {
        userData = null;
    }
    const setUserInfo = (
        token: string, userData: object
    ) => {
        localStorage.setItem(accessTokenKey, token)
        localStorage.setItem(userDataKey, JSON.stringify(userData))
    }
    const setLoggedCheck = (isLoggedIn: boolean) => {
        localStorage.setItem(loggedCheckKey, isLoggedIn? "true" : "false")
    }
    const logout = () => {
        localStorage.removeItem(accessTokenKey)
        localStorage.removeItem(userDataKey)
        localStorage.removeItem(loggedCheckKey)
    }
    if (!accessToken || !userData) return {
        accessToken: null,
        userData: null,
        setUserInfo: setUserInfo,
        isLoggedIn: loggedCheck,
        setLoggedIn: setLoggedCheck,
        logout: logout
    }
    return {
        accessToken: accessToken,
        userData: userData,
        setUserInfo: setUserInfo,
        isLoggedIn: loggedCheck,
        setLoggedIn: setLoggedCheck,
        logout: logout
    }
}

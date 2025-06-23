import {apiUrl, sendAuthRequest, sendRequest} from "./common.ts";

export function authLogin(username: string, password: string) {
    return sendRequest(
        "POST", apiUrl("auth/login"), {},
        {username: username, password: password},
    )
}

export function authRegister(username: string, password: string) {
    return sendRequest(
        "POST", apiUrl("auth/register"), {},
        {username: username, password: password},
    )
}

export function authProbe(token: string) {
    return sendAuthRequest(
        "GET", apiUrl("auth/profile"), token
    )
}

import {apiUrl, sendAuthRequest} from "./common.ts";


export function getMyProfile(token: string) {
    return sendAuthRequest(
        "GET", apiUrl("profile"), token
    )
}

export function requestNalogCode(token: string) {
    return sendAuthRequest(
        "POST", apiUrl("auth-nalog/request"), token
    )
}

export function submitNalogCode(token: string, code: string) {
    return sendAuthRequest(
        "POST", apiUrl("auth-nalog/submit"), token,
        {"code": code}
    )
}

export function checkNalogCode(
    token: string | null
) {
    return sendAuthRequest(
        "GET", apiUrl("auth-nalog/check"), token
    )
}
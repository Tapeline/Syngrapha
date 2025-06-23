import {apiUrl, sendAuthRequest} from "./common.ts";

export function getTransactions(
    token: string | null, fromDate?: string | undefined, toDate?: string | undefined
) {
    const params = {}
    if (fromDate !== undefined) params["since"] = fromDate;
    if (toDate !== undefined) params["before"] = toDate;
    console.log(fromDate, toDate, params)
    return sendAuthRequest(
        "GET", apiUrl(`transactions/my/`), token,
        null, params
    )
}

export function createTransactionFromTable(
    token: string | null, file: any
) {
    return sendAuthRequest(
        "GET", apiUrl(`transactions/my/`), token,
        null,
    )
}

export function createTransactionQR(
    token: string | null, qr: string
) {
    return sendAuthRequest(
        "POST", apiUrl(`transactions/import-qr/`), token,
        {"code": qr},
    )
}

export function getTransaction(
    token: string | null, transId: string
) {
    return sendAuthRequest(
        "GET", apiUrl(`transactions/${transId}`), token
    )
}

export function getProduct(
    token: string | null, transId: string, prodId: string
) {
    return sendAuthRequest(
        "GET", apiUrl(`transactions/${transId}/${prodId}`), token
    )
}

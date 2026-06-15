const API_BASE_URL =
    "http://127.0.0.1:8000/api";

function getToken() {

    return localStorage.getItem(
        "access_token"
    );
}

function getAuthHeaders() {

    return {
        Authorization:
            `Bearer ${getToken()}`
    };
}
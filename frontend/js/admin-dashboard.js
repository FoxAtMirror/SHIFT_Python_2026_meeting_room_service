document.addEventListener(
    "DOMContentLoaded",
    async () => {

        await initializeNavbar();

        await verifyAdmin();
    }
);

async function verifyAdmin() {

    const response =
        await fetch(
            `${API_BASE_URL}/auth/me`,
            {
                headers:
                    getAuthHeaders()
            }
        );

    if (!response.ok) {

        window.location.href =
            "login.html";

        return;
    }

    const user =
        await response.json();

    if (user.role !== "admin") {

        alert(
            "Доступ запрещён"
        );

        window.location.href =
            "rooms-list.html";
    }
}
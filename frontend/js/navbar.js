async function initializeNavbar() {

    await showAdminLink();

    initializeLogoutButton();
}

async function showAdminLink() {

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/auth/me`,
                {
                    headers:
                        getAuthHeaders()
                }
            );

        if (!response.ok) {
            return;
        }

        const user =
            await response.json();

        if (user.role === "admin") {

            document
                .getElementById(
                    "admin-link"
                )
                .style.display =
                    "inline";
        }

    } catch (error) {

        console.error(error);
    }
}

function initializeLogoutButton() {

    const button =
        document.getElementById(
            "logout-btn"
        );

    if (!button) {
        return;
    }

    button.addEventListener(
        "click",
        () => {

            localStorage.removeItem(
                "access_token"
            );

            window.location.href =
                "login.html";
        }
    );
}
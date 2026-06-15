document.addEventListener(
    "DOMContentLoaded",
    async () => {

        await initializeNavbar();

        const token =
            getToken();

        if (!token) {

            window.location.href =
                "login.html";

            return;
        }

        try {

            await loadCurrentUser();

            await loadRooms();

        } catch (error) {

            console.error(error);

            localStorage.removeItem(
                "access_token"
            );

            window.location.href =
                "login.html";
        }
    }
);

async function loadCurrentUser() {

    const response =
        await fetch(
            `${API_BASE_URL}/auth/me`,
            {
                headers:
                    getAuthHeaders()
            }
        );

    if (!response.ok) {

        throw new Error(
            "Unauthorized"
        );
    }

    const user =
        await response.json();

    document.getElementById(
        "user-info"
    ).textContent =
        `Привет, ${user.login} (${user.role})`;
}

async function loadRooms() {

    const response =
        await fetch(
            `${API_BASE_URL}/rooms`
        );

    const rooms =
        await response.json();

    console.log(rooms);

    const container =
        document.getElementById(
            "rooms-container"
        );

    container.innerHTML = "";

    rooms.forEach(room => {

        const roomElement =
            document.createElement("div");

        roomElement.innerHTML = `
            <a href="room-details.html?id=${room.id}">
                ${room.name}
            </a>
        `;

        container.appendChild(
            roomElement
        );
    });
}

document
    .getElementById(
        "logout-btn"
    )
    .addEventListener(
        "click",
        () => {

            localStorage.removeItem(
                "access_token"
            );

            window.location.href =
                "login.html";
        }
    );
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
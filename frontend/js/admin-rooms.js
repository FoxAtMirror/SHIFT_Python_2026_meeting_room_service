document.addEventListener(
    "DOMContentLoaded",
    async () => {

        await initializeNavbar();

        await verifyAdmin();

        await loadRooms();

        initializeCreateRoomButton();
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

    const user =
        await response.json();

    if (user.role !== "admin") {

        window.location.href =
            "rooms-list.html";
    }
}

async function loadRooms() {

    const response =
        await fetch(
            `${API_BASE_URL}/rooms`
        );

    const rooms =
        await response.json();

    const container =
        document.getElementById(
            "rooms-container"
        );

    container.innerHTML = "";

    rooms.forEach(room => {

        const roomElement =
            document.createElement("div");

        roomElement.innerHTML = `
            ${room.id}
            -
            ${room.name}
        `;

        container.appendChild(
            roomElement
        );
    });
}

function initializeCreateRoomButton() {

    document
        .getElementById(
            "create-room-btn"
        )
        .addEventListener(
            "click",
            createRoom
        );
}

async function createRoom() {

    const roomName =
        document.getElementById(
            "room-name"
        ).value;

    if (!roomName) {

        alert(
            "Введите название комнаты"
        );

        return;
    }

    const response =
        await fetch(
            `${API_BASE_URL}/rooms`,
            {
                method: "POST",
                headers: {
                    ...getAuthHeaders(),
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    name: roomName
                })
            }
        );

    if (!response.ok) {

        alert(
            "Ошибка создания комнаты"
        );

        return;
    }

    document.getElementById(
        "room-name"
    ).value = "";

    await loadRooms();
}
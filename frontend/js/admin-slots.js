document.addEventListener(
    "DOMContentLoaded",
    async () => {

        await initializeNavbar();

        await verifyAdmin();

        await loadRooms();

        await loadSlots();

        document
            .getElementById(
                "room-select"
            )
            .addEventListener(
                "change",
                loadSlots
            );

        document
            .getElementById(
                "create-slot-btn"
            )
            .addEventListener(
                "click",
                createSlot
            );
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

    const select =
        document.getElementById(
            "room-select"
        );

    select.innerHTML = "";

    rooms.forEach(room => {

        const option =
            document.createElement(
                "option"
            );

        option.value =
            room.id;

        option.textContent =
            room.name;

        select.appendChild(
            option
        );
    });
}

async function loadSlots() {

    const roomId =
        document.getElementById(
            "room-select"
        ).value;

    if (!roomId) {
        return;
    }

    const response =
        await fetch(
            `${API_BASE_URL}/slots/room/${roomId}`
        );

    const slots =
        await response.json();

    const container =
        document.getElementById(
            "slots-container"
        );

    container.innerHTML = "";

    if (slots.length === 0) {

        container.innerHTML =
            "<p>Слотов пока нет</p>";

        return;
    }

    slots.forEach(slot => {

        const slotElement =
            document.createElement(
                "div"
            );

        slotElement.innerHTML = `
            ${slot.start_time}
            -
            ${slot.end_time}
        `;

        container.appendChild(
            slotElement
        );
    });
}

async function createSlot() {

    const roomId =
        Number(
            document.getElementById(
                "room-select"
            ).value
        );

    const startTime =
        document.getElementById(
            "start-time"
        ).value;

    const endTime =
        document.getElementById(
            "end-time"
        ).value;

    if (
        !startTime ||
        !endTime
    ) {

        alert(
            "Заполните время"
        );

        return;
    }

    const response =
        await fetch(
            `${API_BASE_URL}/slots`,
            {
                method: "POST",
                headers: {
                    ...getAuthHeaders(),
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    room_id: roomId,
                    start_time: startTime,
                    end_time: endTime
                })
            }
        );

    const data =
        await response.json();

    if (!response.ok) {

        alert(
            data.detail ||
            "Ошибка создания"
        );

        return;
    }

    alert(
        "Слот создан"
    );

    document.getElementById(
        "start-time"
    ).value = "";

    document.getElementById(
        "end-time"
    ).value = "";

    await loadSlots();
}
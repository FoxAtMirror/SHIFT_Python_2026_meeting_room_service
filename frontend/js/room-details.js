document.addEventListener(
    "DOMContentLoaded",
    async () => {

        await initializeNavbar();
    }
);

const params =
    new URLSearchParams(
        window.location.search
    );

const roomId =
    params.get("id");

document.getElementById(
    "room-id"
).textContent =
    `Комната #${roomId}`;

document
    .getElementById(
        "load-slots-btn"
    )
    .addEventListener(
        "click",
        loadSlots
    );

async function loadSlots() {

    const date =
        document.getElementById(
            "booking-date"
        ).value;

    if (!date) {

        alert(
            "Выберите дату"
        );

        return;
    }

    const response =
        await fetch(
            `${API_BASE_URL}/rooms/${roomId}/availability?booking_date=${date}`
        );

    const slots =
        await response.json();

    const container =
        document.getElementById(
            "slots-container"
        );

    container.innerHTML = "";

    slots.forEach(slot => {

        const slotElement =
            document.createElement("div");

        if (!slot.available) {

            slotElement.innerHTML = `
                ${slot.start_time}
                -
                ${slot.end_time}
                (занято)
            `;

            container.appendChild(
                slotElement
            );

            return;
        }

        slotElement.innerHTML = `
            ${slot.start_time}
            -
            ${slot.end_time}

            <button
                onclick="bookSlot(
                    ${slot.slot_id}
                )">
                Забронировать
            </button>
        `;

        container.appendChild(
            slotElement
        );
    });
}

async function bookSlot(
    slotId
) {

    const date =
        document.getElementById(
            "booking-date"
        ).value;

    const response =
        await fetch(
            `${API_BASE_URL}/bookings`,
            {
                method: "POST",
                headers: {
                    ...getAuthHeaders(),
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    room_id:
                        Number(roomId),
                    slot_id:
                        slotId,
                    date:
                        date
                })
            }
        );

    const data =
        await response.json();

    if (!response.ok) {

        alert(
            data.detail
        );

        return;
    }

    alert(
        "Бронирование создано"
    );

    loadSlots();
}
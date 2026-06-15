 document.addEventListener(
    "DOMContentLoaded",
    async () => {

        await initializeNavbar();

        await verifyAdmin();

        await loadBookings();
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
            "Доступ запрещен"
        );

        window.location.href =
            "rooms-list.html";
    }
}

async function loadBookings() {

    const response =
        await fetch(
            `${API_BASE_URL}/bookings/`,
            {
                headers:
                    getAuthHeaders()
            }
        );

    const bookings =
        await response.json();

    const container =
        document.getElementById(
            "bookings-container"
        );

    container.innerHTML = "";

    bookings.forEach(booking => {

        const bookingElement =
            document.createElement(
                "div"
            );

        bookingElement.innerHTML = `
            <p>
                Бронирование #${booking.id}
                |
                Пользователь: ${booking.user_login}
                |
                Комната: ${booking.room_name}
                |
                Время: ${booking.slot_time}
                |
                Дата: ${booking.date}
            </p>

            <button
                onclick="deleteBooking(${booking.id})">
                Удалить
            </button>

            <hr>
        `;

        container.appendChild(
            bookingElement
        );
    });
}

async function deleteBooking(
    bookingId
) {

    if (
        !confirm(
            "Удалить бронирование?"
        )
    ) {
        return;
    }

    const response =
        await fetch(
            `${API_BASE_URL}/bookings/${bookingId}`,
            {
                method: "DELETE",
                headers:
                    getAuthHeaders()
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

    await loadBookings();
}
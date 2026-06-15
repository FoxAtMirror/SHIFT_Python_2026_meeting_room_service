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

        await loadBookings();
    }
);

async function loadBookings() {

    const response =
        await fetch(
            `${API_BASE_URL}/bookings/my`,
            {
                headers:
                    getAuthHeaders()
            }
        );

    if (!response.ok) {

        alert(
            "Не удалось загрузить бронирования"
        );

        return;
    }

    const bookings =
        await response.json();

    const container =
        document.getElementById(
            "bookings-container"
        );

    container.innerHTML = "";

    if (bookings.length === 0) {

        container.innerHTML =
            "<p>У вас пока нет бронирований</p>";

        return;
    }

    bookings.forEach(booking => {

        const bookingElement =
            document.createElement("div");

        bookingElement.innerHTML = `
        <p>
            Бронирование #${booking.id}
            |
            Комната: ${booking.room_name}
            |
            Время: ${booking.slot_time}
            |
            Дата: ${booking.date}
        </p>

        <button
            onclick="deleteBooking(${booking.id})">
            Отменить
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
            "Отменить бронирование?"
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

    if (!response.ok) {

        alert(
            "Ошибка удаления"
        );

        return;
    }

    await loadBookings();
}
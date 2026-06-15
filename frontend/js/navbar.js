async function initializeNavbar() {

    renderNavbar();

    await showUserInfo();

    await showAdminLink();

    initializeLogoutButton();
}

function renderNavbar() {

    const navbar =
        document.getElementById(
            "navbar"
        );

    if (!navbar) {
        return;
    }

    navbar.innerHTML = `
        <nav>

            <a href="rooms-list.html">
                Комнаты
            </a>

            |

            <a href="my-bookings.html">
                Мои бронирования
            </a>

            |

            <a
                id="admin-link"
                href="admin-dashboard.html"
                style="display:none"
            >
                Админ
            </a>

            |

            <span id="user-info">

            </span>

            |

            <button id="logout-btn">
                Выйти
            </button>

        </nav>

        <hr>
    `;
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

async function showUserInfo() {

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

        document.getElementById(
            "user-info"
        ).textContent =
            `${user.login} (${user.role})`;

    } catch (error) {

        console.error(error);
    }
}
const registerForm =
    document.getElementById(
        "register-form"
    );

registerForm.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();

        const login =
            document.getElementById(
                "login"
            ).value;

        const password =
            document.getElementById(
                "password"
            ).value;

        try {

            const response =
                await fetch(
                    `${API_BASE_URL}/auth/register`,
                    {
                        method: "POST",
                        headers: {
                            "Content-Type":
                                "application/json"
                        },
                        body: JSON.stringify({
                            login,
                            password
                        })
                    }
                );

            const data =
                await response.json();

            if (!response.ok) {

                throw new Error(
                    data.detail
                );
            }

            const loginResponse =
                await fetch(
                    `${API_BASE_URL}/auth/login`,
                    {
                        method: "POST",
                        headers: {
                            "Content-Type":
                                "application/x-www-form-urlencoded"
                        },
                        body:
                            `username=${encodeURIComponent(login)}`
                            +
                            `&password=${encodeURIComponent(password)}`
                    }
                );

            const loginData =
                await loginResponse.json();

            if (!loginResponse.ok) {

                throw new Error(
                    "Ошибка автоматического входа"
                );
            }    

            localStorage.setItem(
                "access_token",
                loginData.access_token
            );

            window.location.href =
                "rooms-list.html";

        } catch (error) {

            document.getElementById(
                "error-message"
            ).textContent =
                error.message;
        }
    }
);
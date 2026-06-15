const loginForm =
    document.getElementById("login-form");

loginForm.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();

        const login =
            document.getElementById("login").value;

        const password =
            document.getElementById("password").value;

        try {

            const formData =
                new URLSearchParams();

            formData.append(
                "username",
                login
            );

            formData.append(
                "password",
                password
            );

            const response =
                await fetch(
                    `${API_BASE_URL}/auth/login`,
                    {
                        method: "POST",
                        headers: {
                            "Content-Type":
                                "application/x-www-form-urlencoded"
                        },
                        body: formData
                    }
                );

            const data =
                await response.json();

            if (!response.ok) {

                throw new Error(
                    data.detail
                );
            }

            localStorage.setItem(
                "access_token",
                data.access_token
            );

            window.location.href = "rooms-list.html";

            console.log(
                "JWT:",
                data.access_token
            );

        } catch (error) {

            document.getElementById(
                "error-message"
            ).textContent =
                error.message;
        }
    }
);
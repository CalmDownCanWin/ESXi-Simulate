
const loginButton = document.getElementById("loginStatus");
const progressBar = document.getElementById("progressBar");
const welcomeMessage = document.getElementById("welcomeMessage");
const usernameInput = document.getElementById("usernameInput");
const passwordInput = document.getElementById("passwordInput");

let isFirstClick = true;

function validateInputs() {
    return usernameInput.value.trim() !== "";
}

function checkInputs() {
        if (usernameInput.value.trim() === "" ) {
            loginButton.disabled = true;
        } else {
            loginButton.disabled = false;
        }
    }

usernameInput.addEventListener("input", checkInputs);
passwordInput.addEventListener("input", checkInputs);

loginButton.addEventListener("click", function () {
    
    welcomeMessage.style.display = "block";
    welcomeMessage.style.color = "#FFA500";
    welcomeMessage.textContent = "Logging in to ESXi host...";

    if (validateInputs()) {
        progressBar.style.display = "block";
        loginButton.disabled = true;

        setTimeout(() => {
            progressBar.style.display = "none";
            loginButton.disabled = false;

            const correctUsername = "123"; // Replace with your actual username
            const correctPassword = "123"; // Replace with your actual password

            if (usernameInput.value === correctUsername && passwordInput.value === correctPassword) {
                welcomeMessage.style.display = "block";
                welcomeMessage.textContent = "Login ERROR!"   ;
                welcomeMessage.style.color = "#FFA500";
            } else {
                welcomeMessage.style.display = "block";
                welcomeMessage.style.color = "#FFA500";
                welcomeMessage.textContent = "Cannot complete login due to an incorrect user name or password.";
                usernameInput.style.borderColor = "red"
                passwordInput.style.borderColor = "red"
            }

            
        }, 5000); // Simulate a 3-second login process
    } else {
        progressBar.style.display = "block";

        setTimeout(() => {
            progressBar.style.display = "none";
            welcomeMessage.style.display = "block";
            welcomeMessage.style.color = "#FFA500";
            welcomeMessage.textContent = "Cannot complete login due to missing username or password.";
        }, 5000); // Simulate a 3-second process
    }
});

loginButton.disabled = true;
// nếu nhập sai hoặc nhập thiếu thì thời gian chạy khoảng 5s
// nếu nhập đúng thì thời gian chạy từ 13-18s hiển thị "Conection Timeout" hoặc "Kết nối bị gián đoạn"
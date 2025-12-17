window.onload = function () {
    eel.is_session_registered()(function (registered) {
        let page = window.location.pathname;

        if (!registered && page.includes("index.html")) {
            window.location.href = "user.html";
        }
    });
};

function saveUser() {
    let name = document.getElementById("name").value;
    let mobile = document.getElementById("mobile").value;

    eel.save_user(name, mobile)(function (response) {
        if (response === "SUCCESS") {
            window.location.href = "index.html";
        } else {
            document.getElementById("msg").innerText = response;
        }
    });
}

function runCode() {
    let code = document.getElementById("code").value;
    eel.run_code(code)(function (result) {
        document.getElementById("output").innerText = result;
    }); 
}

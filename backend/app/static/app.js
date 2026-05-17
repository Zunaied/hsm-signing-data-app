console.log("APP JS LOADED");

/*
========================================
WAIT FOR DOM (CRITICAL FIX)
========================================
*/
document.addEventListener("DOMContentLoaded", () => {

    console.log("DOM READY - ATTACHING EVENTS");

    const signBtn = document.getElementById("signBtn");
    const verifyBtn = document.getElementById("verifyBtn");
    const statusBox = document.getElementById("statusBox");

    // Safety check (VERY IMPORTANT)
    if (!signBtn || !verifyBtn || !statusBox) {
        console.error("UI ELEMENTS NOT FOUND IN DOM");
        return;
    }

    console.log("BUTTONS FOUND:", signBtn, verifyBtn);

    /*
    ========================================
    STATUS HANDLER
    ========================================
    */
    function setStatus(message, success = true) {

        console.log("STATUS:", message);

        statusBox.innerText = message;

        statusBox.style.color = success ? "#22c55e" : "#ef4444";
        statusBox.style.fontWeight = "bold";
    }

    /*
    ========================================
    SIGN REQUEST
    ========================================
    */
    signBtn.addEventListener("click", async () => {

        console.log("SIGN BUTTON CLICKED");

        try {

            const name = document.getElementById("name").value.trim();
            const email = document.getElementById("email").value.trim();

            if (!name || !email) {
                setStatus("Name and Email required", false);
                return;
            }

            setStatus("Signing data...");

            const response = await fetch("/sign", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ name, email })
            });

            console.log("SIGN RESPONSE STATUS:", response.status);

            const data = await response.json();

            console.log("SIGN RESPONSE DATA:", data);

            if (data.signature) {
                document.getElementById("signature").value = data.signature;
            }

            setStatus(data.message || "Signed", data.status === "success");

        } catch (err) {

            console.error("SIGN ERROR:", err);
            setStatus("Sign request failed", false);
        }
    });

    /*
    ========================================
    VERIFY REQUEST
    ========================================
    */
    verifyBtn.addEventListener("click", async () => {

        console.log("VERIFY BUTTON CLICKED");

        try {

            const name = document.getElementById("name").value.trim();
            const email = document.getElementById("email").value.trim();
            const signature = document.getElementById("signature").value.trim();

            if (!name || !email || !signature) {
                setStatus("All fields required for verify", false);
                return;
            }

            setStatus("Verifying signature...");

            const response = await fetch("/verify", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name,
                    email,
                    signature
                })
            });

            console.log("VERIFY RESPONSE STATUS:", response.status);

            const data = await response.json();

            console.log("VERIFY RESPONSE DATA:", data);

            if (data.status === "success") {
                setStatus("SIGNATURE VALID ✅", true);
            } else {
                setStatus(data.message || "INVALID SIGNATURE ❌", false);
            }

        } catch (err) {

            console.error("VERIFY ERROR:", err);
            setStatus("Verify request failed", false);
        }
    });

});
console.log("APP JS LOADED");

const statusBox = document.getElementById("statusBox");

function setStatus(msg, ok = true) {
    console.log("STATUS:", msg);

    statusBox.innerText = msg;

    statusBox.style.border = ok ? "1px solid green" : "1px solid red";
}


/*
========================
SIGN
========================
*/
async function signData() {

    console.log("SIGN CLICKED");

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;

    const res = await fetch("/sign", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, email})
    });

    const data = await res.json();

    console.log("SIGN RESPONSE:", data);

    if (data.signature) {
        document.getElementById("signature").value = data.signature;
        setStatus("SIGNED SUCCESS");
    } else {
        setStatus("SIGN FAILED", false);
    }
}


/*
========================
VERIFY
========================
*/
async function verifyData() {

    console.log("VERIFY CLICKED");

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const signature = document.getElementById("signature").value;

    const res = await fetch("/verify", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, email, signature})
    });

    const data = await res.json();

    console.log("VERIFY RESPONSE:", data);

    if (data.status === "success") {
        setStatus("VALID SIGNATURE");
    } else {
        setStatus("INVALID SIGNATURE", false);
    }
}

window.signData = signData;
window.verifyData = verifyData;
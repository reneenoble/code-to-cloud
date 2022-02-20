async function sendRsvp(eventId) {
    but = document.getElementById("rsvp-button")
    but.disabled = true;

    rsvpheader = document.getElementById("see-you-there")
    rsvpheader.hidden = false;

    data = JSON.stringify({"ID": eventId})

    const respone = await fetch("/rsvp", {
        method: 'POST',
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
            },
        body: data // body data type must match "Content-Type" header
    })};

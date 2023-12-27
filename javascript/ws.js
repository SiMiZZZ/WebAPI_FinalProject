function appendMessage(msg) {
    let messages = document.getElementById('messages')
    let message = document.createElement('li')
    let content = document.createTextNode(msg)
    message.appendChild(content)
    messages.appendChild(message)
}
let client_id = Math.floor(Math.random() * 1000) + 1
document.querySelector("#ws-id").textContent = client_id;
let ws = new WebSocket(`{{ ws_protocol }}://{{ server_urn }}/ws/${client_id}`);

ws.onmessage = function(event) {
    appendMessage(event.data)
};

function sendMessage(event) {
    let input = document.getElementById("messageText")
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}
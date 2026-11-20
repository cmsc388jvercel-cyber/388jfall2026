// chat.js -- Week 11: the browser half of the chat.
const socket = io();                       // open the WebSocket (same host as the page)
const log = document.getElementById("log");

function addLine(node) {
  log.appendChild(node);
  log.scrollTop = log.scrollHeight;
}

function line(text, cssClass) {
  const p = document.createElement("p");
  p.textContent = text;                    // textContent, NOT innerHTML: text stays text
  if (cssClass) p.className = cssClass;
  return p;
}

socket.on("connect", () => {
  const name = prompt("Pick a username") || "anonymous";
  socket.emit("join", { username: name });
});

socket.on("user_joined", (d) => {
  document.getElementById("count").textContent = "(" + d.online + " online)";
  addLine(line(d.username + " joined", "system"));
});

socket.on("user_left", (d) => {
  document.getElementById("count").textContent = "(" + d.online + " online)";
  addLine(line(d.username + " left", "system"));
});

socket.on("chat_message", (m) => addLine(line(m.username + ": " + m.text)));
socket.on("announcement", (m) => addLine(line("ANNOUNCEMENT: " + m.text, "announce")));

document.getElementById("form").addEventListener("submit", (e) => {
  e.preventDefault();
  const box = document.getElementById("text");
  socket.emit("chat_message", { text: box.value });
  box.value = "";
});

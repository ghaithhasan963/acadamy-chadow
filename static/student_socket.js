const socket = io();

socket.on("show_message", (data) => {
  alert("📢 رسالة من المعلم:\n" + data.message);
});

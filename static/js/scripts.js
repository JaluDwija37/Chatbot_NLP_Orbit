const msgerForm = document.querySelector(".msger-inputarea");
const msgerInput = document.querySelector(".msger-input");
const msgerChat = document.querySelector(".msger-chat");

// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "/static/assets/images/kadekbot.png";
const PERSON_IMG = "/static/assets/images/user.png";
const BOT_NAME = "Orbit Care";
const PERSON_NAME = "Kamu";

msgerForm.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = msgerInput.value;
  if (!msgText) return;

  // Display the user's message
  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";

  // Send data via AJAX
  $.ajax({
    type: "POST",
    url: "/ask",
    data: { user_question: msgText },
    success: function (data) {
      // Extract the response message from the JSON data
      const response = data.response;

      // Display the bot's response
      appendMessage(BOT_NAME, BOT_IMG, "left", response);

      // Scroll to the bottom of the chat
      msgerChat.scrollTop = msgerChat.scrollHeight;
    },
    error: function (xhr, status, error) {
      // Handle errors if any
      console.error("Error: " + error);
    }
  });
});

function appendMessage(name, img, side, text) {
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop = msgerChat.scrollHeight;
}

// Utils
function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}

$(document).ready(function () {
  // Use event delegation to handle the modal event
  $(document).on('show.bs.modal', '#updateModal', function (event) {
    var button = $(event.relatedTarget);;
    var tag = button.data('tag');
    var pattern = button.data('pattern');
    var responses = button.data('responses');

    // Use console.log instead of alert
    console.log(button, id, tag);

    // Set the form fields with the data from the selected intent
    $('#update_id').val(id);
    $('#update_tag').val(tag);
    $('#update_pattern').val(pattern);
    $('#update_responses').val(responses);
  });
});

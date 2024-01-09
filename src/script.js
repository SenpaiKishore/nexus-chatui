document.addEventListener("DOMContentLoaded", function() {
  var textarea = document.getElementById("query");
  textarea.focus();
});

function sendMessage(){
  const queryInput = document.getElementById('query');
  const resultContainer = document.getElementById('result');
  const query = queryInput.value;

  queryInput.value = '';

  var messagePara = document.createElement('p');
  messagePara.innerHTML = query;
  var messageDiv = document.createElement('div');
  messageDiv.className = 'message';
  messageDiv.appendChild(messagePara);
  var messageContainerDiv = document.createElement('div');
  messageContainerDiv.className = 'message-container user';
  messageContainerDiv.appendChild(messageDiv);
  document.getElementById("chat-messages").appendChild(messageContainerDiv);

  // Make a POST request to the Flask API
  fetch('http://localhost:8080/api/query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      "query": query,
    }),
  })
  .then(response => response.json())
  .then(data => {
    var messagePara = document.createElement('p');
    messagePara.innerHTML = data.result;
    var messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    messageDiv.appendChild(messagePara);
    var messageContainerDiv = document.createElement('div');
    messageContainerDiv.className = 'message-container system';
    messageContainerDiv.appendChild(messageDiv);
    document.getElementById("chat-messages").appendChild(messageContainerDiv);
  })
  .catch(error => {
    console.error('Error:', error);
  });

}
function autoResize() {
  var textarea = document.getElementById('query');
  var container = document.getElementById('user-input');

  // Set a threshold to trigger scrolling (e.g., 80% of the max height)
  var maxHeight = parseFloat(getComputedStyle(container).maxHeight);
  
  textarea.style.height = '20px';
  
  if (textarea.scrollHeight > '60'){
    textarea.style.height = textarea.scrollHeight -50 + 'px';
  }

  // If the textarea height exceeds the threshold, scroll to the bottom
  if (textarea.scrollHeight > maxHeight) {
    container.scrollTop = container.scrollHeight;
  }
}

function handleKeyPress(event) {
  if (event.key === "Enter") {
      event.preventDefault();
      sendMessage();
      console.log("sending message")
  }
}
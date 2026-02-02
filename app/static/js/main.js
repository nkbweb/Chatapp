// app/static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Search functionality
    const searchInput = document.getElementById('search-chats');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const chatItems = document.querySelectorAll('.chat-item');
            
            chatItems.forEach(function(item) {
                const chatName = item.querySelector('.chat-name').textContent.toLowerCase();
                const lastMessage = item.querySelector('.chat-last-message').textContent.toLowerCase();
                
                if (chatName.includes(searchTerm) || lastMessage.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
    
    // Auto-focus message input in chat
    const messageInput = document.getElementById('message-content');
    if (messageInput) {
        messageInput.focus();
    }
});
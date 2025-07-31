jQuery(document).ready(function($) {
    'use strict';
    
    // Chat widget elements
    const chatIcon = $('#truelearn-chat-icon');
    const chatWindow = $('#truelearn-chat-window');
    const chatClose = $('#truelearn-chat-close');
    const chatMessages = $('#truelearn-chat-messages');
    const chatInput = $('#truelearn-chat-input');
    const chatSend = $('#truelearn-chat-send');
    const quickReplies = $('.truelearn-quick-reply');
    
    // Chat state
    let isChatOpen = false;
    let isTyping = false;
    
    // Toggle chat window
    chatIcon.on('click', function() {
        toggleChat();
    });
    
    chatClose.on('click', function() {
        closeChat();
    });
    
    // Close chat when clicking outside
    $(document).on('click', function(e) {
        if (!$(e.target).closest('.truelearn-chat-widget').length && isChatOpen) {
            closeChat();
        }
    });
    
    // Send message on Enter key
    chatInput.on('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Auto-resize textarea
    chatInput.on('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 100) + 'px';
    });
    
    // Send message button
    chatSend.on('click', function() {
        sendMessage();
    });
    
    // Quick reply buttons
    quickReplies.on('click', function() {
        const message = $(this).data('message');
        addMessage(message, 'user');
        sendMessageToAPI(message);
    });
    
    // Functions
    function toggleChat() {
        if (isChatOpen) {
            closeChat();
        } else {
            openChat();
        }
    }
    
    function openChat() {
        chatWindow.addClass('active');
        isChatOpen = true;
        chatInput.focus();
        scrollToBottom();
    }
    
    function closeChat() {
        chatWindow.removeClass('active');
        isChatOpen = false;
    }
    
    function addMessage(content, sender) {
        const messageDiv = $('<div>').addClass('truelearn-message').addClass('truelearn-' + sender);
        
        const avatar = $('<div>').addClass('truelearn-message-avatar');
        const icon = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        avatar.html(icon);
        
        const messageContent = $('<div>').addClass('truelearn-message-content');
        
        // Format content with line breaks and bullet points
        const formattedContent = content
            .replace(/\n/g, '<br>')
            .replace(/•/g, '• ');
        
        messageContent.html(formattedContent);
        
        messageDiv.append(avatar).append(messageContent);
        chatMessages.append(messageDiv);
        
        scrollToBottom();
    }
    
    function showTypingIndicator() {
        if ($('.truelearn-typing-indicator').length === 0) {
            const typingDiv = $(`
                <div class="truelearn-typing-indicator">
                    <div class="truelearn-typing-dots">
                        <div class="truelearn-typing-dot"></div>
                        <div class="truelearn-typing-dot"></div>
                        <div class="truelearn-typing-dot"></div>
                    </div>
                </div>
            `);
            chatMessages.append(typingDiv);
        }
        $('.truelearn-typing-indicator').show();
        scrollToBottom();
    }
    
    function hideTypingIndicator() {
        $('.truelearn-typing-indicator').hide();
    }
    
    function scrollToBottom() {
        chatMessages.scrollTop(chatMessages[0].scrollHeight);
    }
    
    function sendMessage() {
        const message = chatInput.val().trim();
        if (message && !isTyping) {
            addMessage(message, 'user');
            sendMessageToAPI(message);
            chatInput.val('');
            chatInput.css('height', 'auto');
        }
    }
    
    function sendMessageToAPI(message) {
        isTyping = true;
        chatSend.prop('disabled', true);
        showTypingIndicator();
        
        $.ajax({
            url: truelearn_ajax.ajax_url,
            type: 'POST',
            data: {
                action: 'chat_message',
                message: message,
                nonce: truelearn_ajax.nonce
            },
            success: function(response) {
                hideTypingIndicator();
                
                if (response.success && response.data.status === 'success') {
                    addMessage(response.data.response, 'bot');
                } else {
                    addMessage('Sorry, I encountered an error. Please try again.', 'bot');
                }
            },
            error: function(xhr, status, error) {
                hideTypingIndicator();
                addMessage('Sorry, I\'m having trouble connecting. Please check your internet connection.', 'bot');
                console.error('Chat API Error:', error);
            },
            complete: function() {
                isTyping = false;
                chatSend.prop('disabled', false);
            }
        });
    }
    
    // Add typing indicator to DOM
    const typingIndicator = $(`
        <div class="truelearn-typing-indicator" style="display: none;">
            <div class="truelearn-typing-dots">
                <div class="truelearn-typing-dot"></div>
                <div class="truelearn-typing-dot"></div>
                <div class="truelearn-typing-dot"></div>
            </div>
        </div>
    `);
    chatMessages.append(typingIndicator);
    
    // Initialize chat
    console.log('TrueLearn Academy Chatbot Widget initialized');
}); 
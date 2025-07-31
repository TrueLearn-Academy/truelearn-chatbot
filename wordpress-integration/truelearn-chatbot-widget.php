<?php
/**
 * Plugin Name: TrueLearn Academy Chatbot Widget
 * Plugin URI: https://truelearnacademy.com
 * Description: Adds a floating chat widget for TrueLearn Academy with AI-powered responses
 * Version: 1.0.0
 * Author: TrueLearn Academy
 * Author URI: https://truelearnacademy.com
 * License: GPL v2 or later
 * Text Domain: truelearn-chatbot
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class TrueLearnChatbotWidget {
    
    public function __construct() {
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_action('wp_footer', array($this, 'render_chat_widget'));
        add_action('wp_ajax_chat_message', array($this, 'handle_chat_message'));
        add_action('wp_ajax_nopriv_chat_message', array($this, 'handle_chat_message'));
    }
    
    public function enqueue_scripts() {
        // Enqueue CSS
        wp_enqueue_style(
            'truelearn-chatbot-style',
            plugin_dir_url(__FILE__) . 'assets/chatbot-widget.css',
            array(),
            '1.0.0'
        );
        
        // Enqueue JavaScript
        wp_enqueue_script(
            'truelearn-chatbot-script',
            plugin_dir_url(__FILE__) . 'assets/chatbot-widget.js',
            array('jquery'),
            '1.0.0',
            true
        );
        
        // Localize script with AJAX URL
        wp_localize_script('truelearn-chatbot-script', 'truelearn_ajax', array(
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('truelearn_chat_nonce')
        ));
    }
    
    public function render_chat_widget() {
        ?>
        <!-- TrueLearn Academy Chatbot Widget -->
        <div id="truelearn-chat-widget" class="truelearn-chat-widget">
            <!-- Chat Icon -->
            <div id="truelearn-chat-icon" class="truelearn-chat-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/>
                </svg>
                <span class="truelearn-chat-label">Chat with us</span>
            </div>
            
            <!-- Chat Window -->
            <div id="truelearn-chat-window" class="truelearn-chat-window">
                <div class="truelearn-chat-header">
                    <div class="truelearn-chat-title">
                        <i class="fas fa-graduation-cap"></i>
                        TrueLearn Academy
                    </div>
                    <div class="truelearn-chat-subtitle">AI Learning Assistant</div>
                    <button id="truelearn-chat-close" class="truelearn-chat-close">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                        </svg>
                    </button>
                </div>
                
                <div class="truelearn-chat-messages" id="truelearn-chat-messages">
                    <div class="truelearn-welcome-message">
                        Welcome to TrueLearn Academy! How can I help you today?
                    </div>
                    
                    <div class="truelearn-message truelearn-bot">
                        <div class="truelearn-message-avatar">
                            <i class="fas fa-robot"></i>
                        </div>
                        <div class="truelearn-message-content">
                            Hello! I'm your AI learning assistant at TrueLearn Academy. I can help you with:
                            <br><br>
                            📚 Course information and enrollment<br>
                            🎯 Learning path recommendations<br>
                            💰 Pricing and payment options<br>
                            📞 Technical support<br>
                            🏆 Certificates and career guidance
                            <br><br>
                            What would you like to know about?
                        </div>
                    </div>
                    
                    <div class="truelearn-quick-replies">
                        <div class="truelearn-quick-reply" data-message="What courses do you offer?">Available Courses</div>
                        <div class="truelearn-quick-reply" data-message="How much do courses cost?">Pricing</div>
                        <div class="truelearn-quick-reply" data-message="How do I enroll?">Enrollment</div>
                        <div class="truelearn-quick-reply" data-message="Contact information">Contact Us</div>
                    </div>
                </div>
                
                <div class="truelearn-chat-input-container">
                    <div class="truelearn-chat-input-wrapper">
                        <textarea 
                            id="truelearn-chat-input" 
                            class="truelearn-chat-input" 
                            placeholder="Type your message here..."
                            rows="1"
                        ></textarea>
                        <button id="truelearn-chat-send" class="truelearn-chat-send">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Font Awesome for icons -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <?php
    }
    
    public function handle_chat_message() {
        // Verify nonce
        if (!wp_verify_nonce($_POST['nonce'], 'truelearn_chat_nonce')) {
            wp_die('Security check failed');
        }
        
        $message = sanitize_text_field($_POST['message']);
        
        if (empty($message)) {
            wp_send_json_error('No message provided');
        }
        
        // Call your Flask API
        $api_url = 'https://your-app-name.onrender.com/api/chat'; // Replace with your actual URL
        
        $response = wp_remote_post($api_url, array(
            'headers' => array(
                'Content-Type' => 'application/json',
            ),
            'body' => json_encode(array(
                'message' => $message
            )),
            'timeout' => 30
        ));
        
        if (is_wp_error($response)) {
            wp_send_json_error('Failed to connect to chatbot service');
        }
        
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        
        if ($data && isset($data['response'])) {
            wp_send_json_success(array(
                'response' => $data['response'],
                'status' => $data['status']
            ));
        } else {
            wp_send_json_error('Invalid response from chatbot service');
        }
    }
}

// Initialize the plugin
new TrueLearnChatbotWidget(); 
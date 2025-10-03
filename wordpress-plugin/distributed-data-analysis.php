<?php
/**
 * Plugin Name: Distributed Data Analysis
 * Plugin URI: https://github.com/arwankhoiruddin/DistributedAI
 * Description: Dashboard untuk sistem analisis data terdistribusi dengan API Server dan Runner
 * Version: 1.0.0
 * Author: Arwan Khoiruddin
 * License: MIT
 */

// Exit if accessed directly
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('DDA_VERSION', '1.0.0');
define('DDA_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('DDA_PLUGIN_URL', plugin_dir_url(__FILE__));

/**
 * Main Plugin Class
 */
class Distributed_Data_Analysis {
    
    private static $instance = null;
    
    public static function instance() {
        if (is_null(self::$instance)) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    private function __construct() {
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('admin_init', array($this, 'register_settings'));
        add_action('admin_enqueue_scripts', array($this, 'enqueue_admin_scripts'));
    }
    
    /**
     * Add admin menu
     */
    public function add_admin_menu() {
        add_menu_page(
            'Data Analysis',
            'Data Analysis',
            'manage_options',
            'distributed-data-analysis',
            array($this, 'render_tasks_page'),
            'dashicons-chart-area',
            30
        );
        
        add_submenu_page(
            'distributed-data-analysis',
            'Tasks',
            'Tasks',
            'manage_options',
            'distributed-data-analysis',
            array($this, 'render_tasks_page')
        );
        
        add_submenu_page(
            'distributed-data-analysis',
            'Settings',
            'Settings',
            'manage_options',
            'dda-settings',
            array($this, 'render_settings_page')
        );
    }
    
    /**
     * Register settings
     */
    public function register_settings() {
        register_setting('dda_settings', 'dda_api_url');
        register_setting('dda_settings', 'dda_api_key');
        
        add_settings_section(
            'dda_api_settings',
            'API Server Configuration',
            array($this, 'settings_section_callback'),
            'dda-settings'
        );
        
        add_settings_field(
            'dda_api_url',
            'API Server URL',
            array($this, 'api_url_field_callback'),
            'dda-settings',
            'dda_api_settings'
        );
        
        add_settings_field(
            'dda_api_key',
            'API Key',
            array($this, 'api_key_field_callback'),
            'dda-settings',
            'dda_api_settings'
        );
    }
    
    /**
     * Settings section callback
     */
    public function settings_section_callback() {
        echo '<p>Configure the API server connection settings.</p>';
    }
    
    /**
     * API URL field callback
     */
    public function api_url_field_callback() {
        $value = get_option('dda_api_url', 'http://localhost:8000');
        echo '<input type="text" name="dda_api_url" value="' . esc_attr($value) . '" class="regular-text" placeholder="http://localhost:8000">';
        echo '<p class="description">URL of the API server (e.g., http://localhost:8000)</p>';
    }
    
    /**
     * API Key field callback
     */
    public function api_key_field_callback() {
        $value = get_option('dda_api_key', '');
        echo '<input type="text" name="dda_api_key" value="' . esc_attr($value) . '" class="regular-text" placeholder="Optional API Key">';
        echo '<p class="description">Optional API key for authentication</p>';
    }
    
    /**
     * Render settings page
     */
    public function render_settings_page() {
        if (!current_user_can('manage_options')) {
            return;
        }
        
        if (isset($_GET['settings-updated'])) {
            add_settings_error('dda_messages', 'dda_message', 'Settings Saved', 'updated');
        }
        
        settings_errors('dda_messages');
        ?>
        <div class="wrap">
            <h1><?php echo esc_html(get_admin_page_title()); ?></h1>
            <form action="options.php" method="post">
                <?php
                settings_fields('dda_settings');
                do_settings_sections('dda-settings');
                submit_button('Save Settings');
                ?>
            </form>
        </div>
        <?php
    }
    
    /**
     * Render tasks page
     */
    public function render_tasks_page() {
        if (!current_user_can('manage_options')) {
            return;
        }
        
        // Handle form submission
        if (isset($_POST['dda_create_task']) && check_admin_referer('dda_create_task_action', 'dda_create_task_nonce')) {
            $this->handle_create_task();
        }
        
        ?>
        <div class="wrap">
            <h1>Data Analysis Tasks</h1>
            
            <!-- Create Task Form -->
            <div class="dda-create-task">
                <h2>Create New Task</h2>
                <form method="post" action="">
                    <?php wp_nonce_field('dda_create_task_action', 'dda_create_task_nonce'); ?>
                    
                    <table class="form-table">
                        <tr>
                            <th scope="row">
                                <label for="operation_code">Operation Code</label>
                            </th>
                            <td>
                                <select name="operation_code" id="operation_code" required>
                                    <option value="">Select Operation</option>
                                    <option value="100">100 - Fetch Raw Data</option>
                                    <option value="200">200 - Filter Data</option>
                                    <option value="300">300 - ML Model Analysis</option>
                                    <option value="400">400 - Export Report</option>
                                </select>
                                <p class="description">Select the type of operation to perform</p>
                            </td>
                        </tr>
                        <tr>
                            <th scope="row">
                                <label for="params">Parameters (JSON)</label>
                            </th>
                            <td>
                                <textarea name="params" id="params" rows="4" class="large-text" placeholder='{"key": "value"}'>{}</textarea>
                                <p class="description">Enter task parameters as JSON object</p>
                            </td>
                        </tr>
                    </table>
                    
                    <?php submit_button('Create Task', 'primary', 'dda_create_task'); ?>
                </form>
            </div>
            
            <hr>
            
            <!-- Tasks List -->
            <div class="dda-tasks-list">
                <h2>Task List</h2>
                <?php $this->render_tasks_table(); ?>
            </div>
        </div>
        <?php
    }
    
    /**
     * Handle create task form submission
     */
    private function handle_create_task() {
        $operation_code = intval($_POST['operation_code']);
        $params_json = stripslashes($_POST['params']);
        
        // Validate JSON
        $params = json_decode($params_json, true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            add_settings_error('dda_messages', 'dda_message', 'Invalid JSON in parameters', 'error');
            return;
        }
        
        // Get API settings
        $api_url = get_option('dda_api_url', 'http://localhost:8000');
        $api_key = get_option('dda_api_key', '');
        
        // Create task via API
        $response = wp_remote_post($api_url . '/task', array(
            'headers' => array(
                'Content-Type' => 'application/json',
            ),
            'body' => json_encode(array(
                'operation_code' => $operation_code,
                'params' => $params,
                'api_key' => $api_key
            )),
            'timeout' => 15
        ));
        
        if (is_wp_error($response)) {
            add_settings_error('dda_messages', 'dda_message', 'Error: ' . $response->get_error_message(), 'error');
        } else {
            $body = wp_remote_retrieve_body($response);
            $data = json_decode($body, true);
            
            if (isset($data['task_id'])) {
                add_settings_error('dda_messages', 'dda_message', 'Task created successfully! Task ID: ' . $data['task_id'], 'updated');
            } else {
                add_settings_error('dda_messages', 'dda_message', 'Failed to create task', 'error');
            }
        }
        
        settings_errors('dda_messages');
    }
    
    /**
     * Render tasks table
     */
    private function render_tasks_table() {
        $api_url = get_option('dda_api_url', 'http://localhost:8000');
        
        // Get all tasks from API
        $response = wp_remote_get($api_url . '/tasks/all', array(
            'timeout' => 15
        ));
        
        if (is_wp_error($response)) {
            echo '<p>Error loading tasks: ' . $response->get_error_message() . '</p>';
            return;
        }
        
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        
        if (!isset($data['tasks']) || empty($data['tasks'])) {
            echo '<p>No tasks found. Create your first task above!</p>';
            return;
        }
        
        $tasks = $data['tasks'];
        ?>
        <table class="wp-list-table widefat fixed striped">
            <thead>
                <tr>
                    <th>Task ID</th>
                    <th>Operation Code</th>
                    <th>Status</th>
                    <th>Created At</th>
                    <th>Assigned To</th>
                    <th>Result</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($tasks as $task): ?>
                    <tr>
                        <td><?php echo esc_html(substr($task['task_id'], 0, 8)); ?>...</td>
                        <td><?php echo esc_html($task['operation_code']); ?></td>
                        <td>
                            <span class="dda-status dda-status-<?php echo esc_attr($task['status']); ?>">
                                <?php echo esc_html(ucfirst($task['status'])); ?>
                            </span>
                        </td>
                        <td><?php echo esc_html($task['created_at']); ?></td>
                        <td><?php echo $task['assigned_to'] ? esc_html(substr($task['assigned_to'], 0, 8)) . '...' : '-'; ?></td>
                        <td>
                            <?php if ($task['status'] === 'completed'): ?>
                                <a href="#" class="button button-small dda-view-result" data-task-id="<?php echo esc_attr($task['task_id']); ?>">View Result</a>
                            <?php else: ?>
                                -
                            <?php endif; ?>
                        </td>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
        
        <!-- Result Modal -->
        <div id="dda-result-modal" style="display:none;">
            <div class="dda-result-content">
                <h3>Task Result</h3>
                <div id="dda-result-data"></div>
            </div>
        </div>
        <?php
    }
    
    /**
     * Enqueue admin scripts
     */
    public function enqueue_admin_scripts($hook) {
        if (strpos($hook, 'distributed-data-analysis') === false && $hook !== 'toplevel_page_distributed-data-analysis') {
            return;
        }
        
        wp_enqueue_style('dda-admin', DDA_PLUGIN_URL . 'css/admin.css', array(), DDA_VERSION);
        wp_enqueue_script('dda-admin', DDA_PLUGIN_URL . 'js/admin.js', array('jquery'), DDA_VERSION, true);
        wp_localize_script('dda-admin', 'ddaData', array(
            'apiUrl' => get_option('dda_api_url', 'http://localhost:8000'),
            'nonce' => wp_create_nonce('dda_ajax_nonce')
        ));
    }
}

// Initialize the plugin
function dda_init() {
    return Distributed_Data_Analysis::instance();
}

add_action('plugins_loaded', 'dda_init');

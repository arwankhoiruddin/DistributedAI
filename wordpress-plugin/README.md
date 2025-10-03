# WordPress Plugin - Distributed Data Analysis

WordPress plugin for managing distributed data analysis tasks.

## Installation

1. Copy the `wordpress-plugin` folder to your WordPress installation's `wp-content/plugins/` directory
2. Rename the folder to `distributed-data-analysis` if needed
3. Activate the plugin through the WordPress Admin > Plugins menu
4. Configure the API server settings in WordPress Admin > Data Analysis > Settings

## Configuration

After activating the plugin, go to **Data Analysis > Settings** and configure:

- **API Server URL**: The URL of your API server (e.g., `http://localhost:8000`)
- **API Key**: Optional API key for authentication

## Usage

### Creating Tasks

1. Go to **Data Analysis > Tasks** in the WordPress admin menu
2. Fill in the "Create New Task" form:
   - Select an operation code (100-400)
   - Enter parameters as JSON (default: `{}`)
3. Click "Create Task"

### Viewing Tasks

The tasks table shows:
- Task ID (shortened)
- Operation Code
- Status (pending, assigned, completed)
- Created timestamp
- Assigned runner ID
- View Result button (for completed tasks)

### Operation Codes

- **100**: Fetch Raw Data
- **200**: Filter Data
- **300**: ML Model Analysis
- **400**: Export Report

## Features

- Simple admin interface for task management
- Real-time task status updates
- View task results in a modal dialog
- Auto-refresh tasks table every 10 seconds
- WordPress Settings API integration

## Requirements

- WordPress 5.0 or higher
- PHP 7.0 or higher
- Access to an API server

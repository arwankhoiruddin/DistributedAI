/* Distributed Data Analysis - Admin JavaScript */

(function($) {
    'use strict';
    
    $(document).ready(function() {
        
        // Handle view result button click
        $('.dda-view-result').on('click', function(e) {
            e.preventDefault();
            
            var taskId = $(this).data('task-id');
            var apiUrl = ddaData.apiUrl;
            
            // Fetch result from API
            $.ajax({
                url: apiUrl + '/result/' + taskId,
                method: 'GET',
                dataType: 'json',
                success: function(response) {
                    var resultHtml = '<strong>Task ID:</strong> ' + response.task_id + '<br>';
                    resultHtml += '<strong>Status:</strong> ' + response.status + '<br>';
                    resultHtml += '<strong>Runner ID:</strong> ' + response.runner_id + '<br>';
                    resultHtml += '<strong>Result Data:</strong><br>' + response.result_data;
                    
                    $('#dda-result-data').html(resultHtml);
                    $('#dda-result-modal').fadeIn();
                },
                error: function(xhr, status, error) {
                    alert('Error fetching result: ' + error);
                }
            });
        });
        
        // Close modal when clicking outside
        $(window).on('click', function(e) {
            if (e.target.id === 'dda-result-modal') {
                $('#dda-result-modal').fadeOut();
            }
        });
        
        // Close modal with Escape key
        $(document).on('keydown', function(e) {
            if (e.key === 'Escape') {
                $('#dda-result-modal').fadeOut();
            }
        });
        
        // Auto-refresh tasks table every 10 seconds
        if ($('.dda-tasks-list').length > 0) {
            setInterval(function() {
                location.reload();
            }, 10000);
        }
    });
    
})(jQuery);

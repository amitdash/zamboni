(function(exports) {
    "use strict";

    exports.houdini = function() {
        // Initialize magic labels.
        $(document).delegate('.houdini.ready', 'click', _pd(function(e) {
            var $label = $(this);
            $label.addClass('fading');
            setTimeout(function() {
                $label.removeClass('ready').addClass('active');
            }, 500);
        })).delegate('.houdini.active .done', 'click', _pd(function(e) {
            var $label = $(this).closest('.houdini');
            $label.removeClass('active').addClass('ready');
            // Replace text with new value.
            $label.find('.output').text($label.find('input').val());
        }));
    };

    // Handle Name and Slug.
    exports.nameHoudini = function() {
        var $ctx = $('#general-details');
    };

    exports.privacy = function() {
        // Privacy Policy is required. Maybe I can reuse this elsewhere.
        var $ctx = $('#show-privacy');
        // When the checkbox is clicked ...
        $ctx.delegate('input[type=checkbox]', 'click', function() {
            // Hide the label ...
            $ctx.find('label.checkbox').slideUp(function() {
                // And show the Privacy Policy field ...
                $ctx.find('.brform').slideDown(function() {
                    $ctx.addClass('active');
                });
            });
        })
    }

})(typeof exports === 'undefined' ? (this.submit_details = {}) : exports);


$(document).ready(function() {
    // Icon previews.
    imageStatus.start(true, false);
    $('#submit-media').bind('click', function() {
        imageStatus.cancel();
    });

    submit_details.houdini();
    $('#submit-details').exists(function () {
        //submit_details.general();
        //submit_details.privacy();
        initCatFields();
        initCharCount();
        initSubmit();
        initTruncateSummary();
    });
    submit_details.houdini();
});

var edx = edx || {};

(function($) {
    'use strict';

    edx.student = edx.student || {};
    edx.student.account = edx.student.account || {};

    edx.student.account.EmailOptInInterface = {

        urls: {
            emailOptInUrl: '/user_api/v1/preferences/email_opt_in/'
        },

        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },

        /**
         * Set the email opt in setting for the organization associated
         * with this course.
         * @param  {string} courseKey  Slash-separated course key.
         * @param {string} optIn The preference to opt in or out of organization emails.
         */
        setPreference: function( courseKey, optIn, context ) {
            return $.ajax({
                url: this.urls.emailOptInUrl,
                type: 'POST',
                data: {course_id: courseKey, optIn: optIn},
                headers: this.headers,
                context: context
            });
        }
    };
})(jQuery);

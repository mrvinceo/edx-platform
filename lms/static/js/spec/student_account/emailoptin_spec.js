define(['js/common_helpers/ajax_helpers', 'js/student_account/emailoptin'],
    function( AjaxHelpers, EmailOptInInterface ) {
        'use strict';

        describe( 'edx.student.account.EmailOptInInterface', function() {

            var COURSE_KEY = 'edX/DemoX/Fall',
                OPT_IN = 'True',
                EMAIL_OPT_IN_URL = '/user_api/v1/email_opt_in/';

            it('Opts in for organization emails', function() {
                // Spy on Ajax requests
                var requests = AjaxHelpers.requests( this );

                // Attempt to enroll the user
                EmailOptInInterface.setPreference( COURSE_KEY, OPT_IN );

                // Expect that the correct request was made to the server
                AjaxHelpers.expectRequest( requests, 'POST', EMAIL_OPT_IN_URL );

                // Simulate a successful response from the server
                AjaxHelpers.respondWithJson(requests, {});
            });
        });
    }
);

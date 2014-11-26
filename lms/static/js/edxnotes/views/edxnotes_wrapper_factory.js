;(function (define, undefined) {
    'use strict';
    define(['jquery', 'underscore', 'js/edxnotes/views/notes'], function($, _, Notes) {
        return function (elementId, params, visibility, visibilityUrl) {
            var element = document.getElementById(elementId),
                checkbox = $('a.action-toggle-notes'),
                checkboxIcon = checkbox.children('i');

            console.log('Initial visibility: ' + visibility);
            toggleAnnotator();

            checkbox.on('click', function(event) {
                visibility = !visibility;
                toggleCheckbox();

                $.ajax({
                    type: 'PUT',
                    url: window.location.origin + visibilityUrl,
                    contentType: 'application/json',
                    dataType: 'json',
                    data: JSON.stringify({'visibility': visibility}),
                    success: function(response) {
                        console.log('PUT Success.');
                        toggleAnnotator();
                    },
                    error: function(response) {console.log('PUT Error.');}
                });
                event.preventDefault();
            });

            function toggleCheckbox() {
                checkboxIcon.removeClass('icon-check icon-check-empty');
                checkboxIcon.addClass(visibility ? 'icon-check' : 'icon-check-empty');
            }

            function toggleAnnotator() {
                if (visibility) {
                    createAnnotator();
                } else {
                    destroyAnnotator();
                }
            }

            function createAnnotator() {
                console.time(element);
                Notes.factory(element, params);
                console.timeEnd(element);
            }

            function destroyAnnotator() {
                if (Annotator) {
                    _.each(Annotator._instances, function(instance) {
                        instance.destroy();
                    });
                    console.log('Destroyed Annotator.');
                } else{
                    console.log('No Annotator to destroy.');
                }
            }
        };
    });
}).call(this, define || RequireJS.define);

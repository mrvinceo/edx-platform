define([
    'jquery', 'underscore', 'js/common_helpers/template_helpers',
    'js/common_helpers/ajax_helpers', 'js/edxnotes/views/page_factory'
], function($, _, TemplateHelpers, AjaxHelpers, NotesFactory) {
    'use strict';
    describe('EdxNotes NotesPage', function() {
        var notes = [
            {
                created: 'December 11, 2014 at 11:12AM',
                updated: 'December 11, 2014 at 11:12AM',
                text: 'First added model',
                quote: 'Should be listed third'
            },
            {
                created: 'December 11, 2014 at 11:11AM',
                updated: 'December 11, 2014 at 11:11AM',
                text: 'Third added model',
                quote: 'Should be listed second'
            },
            {
                created: 'December 11, 2014 at 11:10AM',
                updated: 'December 11, 2014 at 11:10AM',
                text: 'Second added model',
                quote: 'Should be listed first'
            }
        ];

        beforeEach(function() {
            this.addMatchers({
                toContainText: function (text) {
                    var trimmedText = $.trim($(this.actual).text());

                    if (text && $.isFunction(text.test)) {
                      return text.test(trimmedText);
                    } else {
                      return trimmedText.indexOf(text) !== -1;
                    }
                }
            });
            loadFixtures('js/fixtures/edxnotes/edxnotes.html');
            TemplateHelpers.installTemplates([
                'templates/edxnotes/note-item',
                'templates/edxnotes/note-item'
            ]);
            this.view = new NotesFactory({notesList: notes});
        });


        it('should be displayed properly', function() {
            var requests = AjaxHelpers.requests(this);

            expect(this.view.$('.tab-search-results')).not.toExist();
            expect(this.view.$('.tab-recent-activity.is-active')).toExist();
            expect(this.view.$('.edx-notes-page-items-list')).toExist();

            this.view.$('.search-box input').val('test_query');
            this.view.$('.search-box button[type=submit]').click();
            AjaxHelpers.respondWithJson(requests, {
                total: 0,
                rows: []
            });
            expect(this.view.$('.tab-search-results.is-active')).toExist();
            expect(this.view.$('.tab-recent-activity')).toExist();
        });

        it('should display update value and accompanying text', function() {
            _.each($('.edxnotes-page-item'), function(element, index) {
                expect($('dl > dt', element).last()).toContainText('Last Edited:');
                expect($('dl > dd', element).last()).toContainText(notes[index].updated);
            });
        });
    });
});

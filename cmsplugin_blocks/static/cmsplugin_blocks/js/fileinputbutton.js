/*
 *
 * Script to enable some visual customization on file input.
 *
 * It require a label element next to the input and related to the input
 * with the "for" attribute. Then the label element text is updated
 * when a file is selected. Finally the input require a class
 * "fileinputbutton__input".
 *
 * A related stylesheet is expected to hide the browser input and customize
 * the label layout to look alike a button.
 *
 * Multiple files:
 *
 * If input have attribute "multiple", the label content will be filled with
 * a string to display a counter about selected files. Default string is
 * "{count} files" where "{count}" is replaced with counter value.
 *
 * You can customize this string in input attribute "data-multiple-caption"
 * with something like "{count} files selected".
 *
 * States:
 *
 * - When input is focused, a classname "has-focus" is added;
 * - When one or more files are selected, a classname "has-selection" is added;
 *
 * Credits:
 *
 * This version of the original script is included in Jquery way to do a
 * "on ready" since medias from a form are always loaded in the header
 * so we need to prevent executing this code before the DOM is ready,
 * hopefully Jquery is alread loaded from Django admin.
 *
 * Original credits:
 *
 * By Osvaldas Valutis, www.osvaldas.info
 * Available for use under the MIT License
 *
 * From: https://tympanus.net/codrops/2015/09/15/styling-customizing-file-inputs-smart-way/
*/

$(function($) {
    var inputs = document.querySelectorAll('.fileinputbutton__input');
    Array.prototype.forEach.call(inputs, function(input) {
        var label = input.nextElementSibling,
            labelVal = label.innerHTML;

        input.addEventListener('change', function(e) {
            var fileName = '';
            if(this.files && this.files.length > 1) {
                fileName = (this.getAttribute('data-multiple-caption') || '{count} files').replace('{count}', this.files.length);
            } else {
                fileName = e.target.value.split('\\').pop();
            }

            if(fileName) {
                label.querySelector('span').innerHTML = fileName;
                input.classList.add('has-selection');
            } else {
                label.innerHTML = labelVal;
                input.classList.remove('has-selection');
            }
        });

        // Firefox bug fix
        input.addEventListener('focus', function() {
            input.classList.add('has-focus');
        });
        input.addEventListener('blur', function() {
            input.classList.remove('has-focus');
        });
    });
});

(function(ns) {
    var INPUT = 'hk',
        KEY_SPACE = 32,
        KEY_BACKSPACE = 8;

    // True iff the string ends in a Devanagari character.
    function endsInDevanagari(data) {
        var mark = data.charCodeAt(data.length - 1);
        // Devanagari [0x0900 - 0x097F]
        return (mark >= 0x0900 && mark <= 0x097F);
    }

    // Binds a textarea to some useful helper functions.
    ns.Textarea = Backbone.View.extend({

        events: {
            'keydown': 'transHelper'
        },

        // Get the caret position inside `el`.
        getCaretPosition: function() {
            var el = this.el;

            // Normal browsers
            if (el.selectionStart !== undefined) {
                return el.selectionStart;
            }

            // IE
            else if (document.selection) {
                el.focus();
                var range = document.selection.createRange();
                range.moveStart('character', -el.value.length);
                return range.text.length;
            }

            else {
                console.log('getCaretPosition: no support for browser');
            }

            return -1;
        },

        // Set the caret position.
        setCaretPosition: function(pos) {
            var el = this.el;

            // Normal browsers
            if (el.setSelectionRange !== undefined) {
                el.focus();
                el.setSelectionRange(pos, pos);
            }

            // IE
            else if (el.createTextRange) {
                var range = el.createTextRange();
                range.move('character', pos);
                range.select();
            }

            else {
                console.log('setCaretPosition: no support for browser');
            }

            return this;
        },

        // Get content before caret. If `replacement` is defined, replace
        // the content with `replacement`.
        beforeCaret: function(replacement) {
            var content = this.el.value,
                pos = this.getCaretPosition();
            if (replacement !== undefined) {
                this.el.value = replacement + content.substr(pos);
                this.setCaretPosition(replacement.length);
                return this;
            } else {
                return content.substring(0, pos);
            }
        },

        transHelper: function(e) {
            var keyCode = e.keyCode;
            // Space and backspace
            if (keyCode === KEY_SPACE || keyCode === KEY_BACKSPACE) {
                var before = this.beforeCaret(),
                    tokens = before.split(' ');

                if (tokens.length) {
                    var last = tokens[tokens.length - 1],
                        changed = false;

                    // Space
                    if (keyCode == KEY_SPACE && last.length > 1) {
                        var index = last.indexOf('#');
                        if (index != -1) {
                            last = last.slice(0, index) + Sanscript.t(last.slice(index+1), INPUT, 'devanagari');
                            changed = true;
                        } else {
                            index = last.indexOf('@');
                            if (index != -1) {
                                var trans = Sanscript.t(last.slice(index+1), INPUT, 'iast');
                                last = last.slice(0, index) + '[sa: ' + trans + ']';
                                changed = true;
                            }
                        }
                    }

                    // Backspace
                    else if (keyCode == KEY_BACKSPACE && endsInDevanagari(last)) {
                        e.preventDefault();
                        var prefix = '',
                            regexp = /(\s)(\S*)$/,
                            match = regexp.exec(last);
                        if (match) {
                            prefix = last.substring(0, match.index) + match[1];
                            last = match[2];
                        }
                        last = prefix + '#' + Sanscript.t(last, 'devanagari', INPUT);
                        changed = true;
                    }

                    if (changed) {
                        tokens[tokens.length - 1] = last;
                        this.beforeCaret(tokens.join(' '));
                    }
                }
            }
        }
    });

})(window.Ambuda = window.Ambuda || {});


$(function() {
    new Ambuda.Textarea({ el: $('#text-input') });
});
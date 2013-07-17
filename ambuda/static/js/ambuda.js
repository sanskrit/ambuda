(function(ns) {
    var INPUT = 'hk',
        KEY_SPACE = 32,
        KEY_BACKSPACE = 8;

    function hasDevanagari(data) {
        var mark = data.charCodeAt(data.length - 1);
        return (mark >= 0x0900 && mark <= 0x097F);
    }

    function getCaretPosition(el) {
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
    }

    function setCaretPosition(el, pos) {
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
    }

    $.fn.beforeCaret = function(replacement) {
        var el = $(this).get(0),
            content = el.value,
            pos = getCaretPosition(el);
        if (replacement !== undefined) {
            el.value = replacement + content.substr(pos);
            setCaretPosition(el, replacement.length);
            return this;
        } else {
            return content.substring(0, pos);
        }
    };

    ns.smartKeydown = function(e) {
        var keyCode = e.keyCode;
        // Space and backspace
        if (keyCode === KEY_SPACE || keyCode === KEY_BACKSPACE) {
            var $this = $(this),
                before = $this.beforeCaret(),
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
                else if (hasDevanagari(last)) {
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
                    $this.beforeCaret(tokens.join(' '));
                }
            }
        }
    };

})(window.Ambuda = window.Ambuda || {});


$(function() {
    $('#text-input').keydown(Ambuda.smartKeydown);
});
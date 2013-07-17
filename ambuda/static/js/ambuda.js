(function(ns) {
    var INPUT = 'hk';

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
        if (keyCode === 32 || keyCode === 8) {
            var $this = $(this),
                before = $this.beforeCaret(),
                tokens = before.split(' ');

            if (tokens.length) {
                var last = tokens[tokens.length - 1],
                    changed = false;

                // Space
                if (keyCode == 32 && last.length > 1) {
                    var mark = last.charAt(0);
                    if (mark == '#') {
                        last = Sanscript.t(last.substr(1), INPUT, 'devanagari');
                        changed = true;
                    } else if (mark == '@') {
                        last = Sanscript.t(last.substr(1), INPUT, 'iast');
                        last = '[sa: ' + last + ']';
                        changed = true;
                    }
                }

                // Backspace
                else if (hasDevanagari(last)) {
                    e.preventDefault();
                    last = '#' + Sanscript.t(last, 'devanagari', INPUT);
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
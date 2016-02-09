// -------------------------------------------------------------------
// markItUp!
// -------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// -------------------------------------------------------------------
// MarkDown tags example
// http://en.wikipedia.org/wiki/Markdown
// http://daringfireball.net/projects/markdown/
// -------------------------------------------------------------------
// Feel free to add more tags
// -------------------------------------------------------------------
mySettings = {
    onShiftEnter: {
        keepDefault: false,
        openWith: '\n\n'
    },
    markupSet: [{
        name: '一级标题',
        key: '1',
        placeHolder: '输入标题...',
        closeWith: function(markItUp) {
            return miu.markdownTitle(markItUp, '=')
        }
    }, {
        name: '二级标题',
        key: '2',
        placeHolder: '输入标题...',
        closeWith: function(markItUp) {
            return miu.markdownTitle(markItUp, '-')
        }
    }, {
        name: '三级标题',
        key: '3',
        openWith: '### ',
        placeHolder: '输入标题...'
    }, {
        name: '四级标题',
        key: '4',
        openWith: '#### ',
        placeHolder: '输入标题...'
    }, {
        name: '五级标题',
        key: '5',
        openWith: '##### ',
        placeHolder: '输入标题...'
    }, {
        name: '六级标题',
        key: '6',
        openWith: '###### ',
        placeHolder: '输入标题...'
    }, {
        separator: '---------------'
    }, {
        name: '粗体',
        key: 'B',
        openWith: '**',
        closeWith: '**'
    }, {
        name: '斜体',
        key: 'I',
        openWith: '_',
        closeWith: '_'
    }, {
        separator: '---------------'
    }, {
        name: '项目列表',
        openWith: '- '
    }, {
        name: '数字列表',
        openWith: function(markItUp) {
            return markItUp.line + '. ';
        }
    }, {
        separator: '---------------'
    }, {
        name: '图片',
        key: 'P',
        replaceWith: '![[![Alternative text]!]]([![Url:!:http://]!] "[![Title]!]")'
    }, {
        name: '链接',
        key: 'L',
        openWith: '[',
        closeWith: ']([![Url:!:http://]!] "[![Title]!]")',
        placeHolder: 'Your text to link here...'
    }, {
        separator: '---------------'
    }, {
        name: '引用',
        openWith: '> '
    }, {
        name: '代码',
        openWith: '(!(\t|!|`)!)',
        closeWith: '(!(`)!)'
    }, {
        separator: '---------------'
    }, {
        name: '预览',
        call: 'preview',
        className: "preview"
    }]
}

// mIu nameSpace to avoid conflict.
miu = {
    markdownTitle: function(markItUp, char) {
        heading = '';
        n = $.trim(markItUp.selection || markItUp.placeHolder).length;
        // work around bug in python-markdown where header underlines must be at least 3 chars
        if (n < 3) {
            n = 3;
        }
        for (i = 0; i < n; i++) {
            heading += char;
        }
        return '\n' + heading;
    }
}

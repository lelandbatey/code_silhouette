#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Create a page listing the 'silhouettes' of several different programming
languages. To create the html file, run like so:

    python make_page.py > silhouettes.html

The code used as the basis for the silhouettes is just the largest files in
popular projects for each respective language on github.
'''

from __future__ import print_function
import io

import requests

import silhouette

code_sources = [
    ("java", "https://raw.githubusercontent.com/spring-projects/spring-boot/master/spring-boot/src/main/java/org/springframework/boot/web/embedded/undertow/UndertowServletWebServerFactory.java"),
    ("rust", "https://raw.githubusercontent.com/BurntSushi/ripgrep/master/ignore/src/walk.rs"),
    ("js", "https://code.jquery.com/jquery-2.2.4.js"),
    ("go", "https://raw.githubusercontent.com/gohugoio/hugo/master/hugolib/site.go"),
    ("python", "https://raw.githubusercontent.com/warner/magic-wormhole/master/src/wormhole/transit.py"),
    ("c", "https://raw.githubusercontent.com/antirez/redis/unstable/src/cluster.c"),
    ("php", "https://raw.githubusercontent.com/symfony/symfony/master/src/Symfony/Component/HttpFoundation/Request.php")
]

code_sources.sort(key=lambda x: x[0])

CSS = '''
body {
    font-family: helvetica, arial, freesans, clean, sans-serif;
    font-size: 18px;
    color: #222;
    background-color: lightgrey;
}
.lfbtable {
    display: flex;
    flex-direction: row;
    flex-wrap: no-wrap;
    align-items: center;
    justify-content: flex-start;
}
.cell {
    align-self: flex-start;
    max-width: 24.9%;
    max-height: 24.9%;
    width: auto;
    height: auto;
    background-position: center center;
    background-repeat: no-repeat;
    background-size: cover;
    overflow: hidden;
    transition: .2s ease opacity;
}
pre {
    font-size: 2px;
    overflow: hidden;
    width: 120px;
    letter-spacing: -0.1px;
    padding-left: 5px;

    filter: blur(1px);
}
a {
filter: blur(0px);
}
'''
PAGE = """<!DOCTYPE html>
<html>
<style type="text/css">
{}
</style>
<body>
<button onclick="toggleBlur();">Toggle blur</button>
<a href="https://github.com/lelandbatey/code_silhouette">Source for generating this document.</a>
<div class='copy'>
{}
</div>
{}
</body>
<script>
{}
</script>
</html>"""

JAVASCRIPT = '''
var bluron = true;
function toggleBlur() {
    bluron = !bluron;
    var pres = document.getElementsByTagName('pre');
    for (var i = 0; i < pres.length; i++) {
        var amount = 0;
        if (bluron) {
            amount = 1;
        }
        pres[i].style.filter = 'blur('+amount+'px)';
    }
}
'''

def make_cell(data):
    tmpl = '<div class="cell"><a href="{}">{}</a><pre>{}</pre></div>'
    return tmpl.format(*data)


def main():
    files = []
    for lang, addr in code_sources:
        data = requests.get(addr).text
        contents = io.StringIO("\n".join(data.split('\n')[:1000]))
        outline = ''.join(silhouette.silhouette(contents, " ", "<span style='background: black;'>", "</span>"))
        files.append((addr, lang, outline))

    cells = []
    for f in files:
        cells.append(make_cell(f))
    table = '<div class="lfbtable">{}\n</div>'
    table = table.format('\n'.join(cells))
    print(PAGE.format(CSS, table, "", JAVASCRIPT))

if __name__ == '__main__':
    main()

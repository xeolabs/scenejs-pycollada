"""
Generates sample code for outputing html with embeded models
"""

def generate_html_head(title):
    return \
"<!DOCTYPE HTML>\n\
<html>\n\
<!--\n\
      " + title + "\n\
-->\n\
<head>\n\
  <meta charset='utf-8' />\n\
  <title>"+ title + "</title>\n\
\n\
  <!-- Framework -->\n\
\n\
  <!--<script type='application/javascript' src='scenejs.min.js'></script>-->\n\
  <script type='application/javascript' src='scenejs.js'></script>\n\
\n\
  <!-- Resources -->\n\
\n"

def generate_html_body():
    return \
"</head>\n\
<body>\n\
    <div id='scenejsLog'></div>\n\
    <div id='content'>\n\
        <canvas id='sampleCanvas' width='1030' height='700'>\n\
            <p>This application requires a browser that supports the<a href='http://www.w3.org/html/wg/html5/'>HTML5</a>&lt;canvas&gt; feature.</p>\n\
        </canvas>\n\
    </div>\n\
</body>\n\
</html>"

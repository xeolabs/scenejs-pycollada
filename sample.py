"""
Generates sample code for outputing html with embeded models
"""

def generate_html_head(title, detailed=False):
    return \
"<!DOCTYPE HTML>\n\
<html>\n\
<!--\n\
      " + title + "\n\
-->\n\
<head>\n\
    <meta charset='utf-8'>\n" + ("\
    <!-- Use Chrome Frame in Internet Explorer if it is available (this functionality can be placed in the .htaccess file instead if desired) -->\n\
    <meta http-equiv='X-UA-Compatible' content='IE=edge,chrome=1'>\n" if detailed else "\n") + "\
\n\
    <title>"+ title + "</title>\n\
\n\
    <!-- Framework -->\n\
\n\
    <!--<script type='text/javascript' src='scenejs.min.js'></script>-->\n\
    <script type='text/javascript' src='scenejs.js'></script>\n\
\n\
</head>\n\
<body>\n\
    <div id='scenejsLog'></div>\n\
    <div id='content'>\n\
        <canvas id='scenejsCanvas' width='1030' height='700'>\n\
            <p>This application requires a browser that supports the<a href='http://www.w3.org/html/wg/html5/'>HTML5</a>&lt;canvas&gt; feature.</p>\n\
        </canvas>\n\
    </div>\n\
\n\
    <!-- Resources -->\n\
\n"

def generate_html_body(sceneId=None):
    return "\
    <script type='text/javascript'>\n" + ("\
        SceneJS.createNode({\n\
            type: 'scene',\n\
            id: 'sampleScene',\n\
            canvasId: 'scenejsCanvas',\n\
            loggingElementId: 'scenejsLog',\n\
            nodes: [\n\
                // Add your nodes here...\n\
            ]\n\
        });\n" if not sceneId else "") + "\
        SceneJS.withNode('" + (sceneId if sceneId else "sampleScene") + "').render();\n\
    </script>\n\
</body>\n\
</html>"

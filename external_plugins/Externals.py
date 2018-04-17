# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from branca.element import CssLink, Figure, JavascriptLink, MacroElement

from jinja2 import Template


class ScrollZoomToggler(MacroElement):
    """Creates a button for enabling/disabling scroll on the Map."""
    def __init__(self):
        super(ScrollZoomToggler, self).__init__()
        self._name = 'ScrollZoomTogglerv2'

        self._template = Template("""
            {% macro header(this,kwargs) %}
                <style>
                    #{{this.get_name()}} {
                        position:absolute;
                        width:35px;
                        bottom:10px;
                        height:35px;
                        left:10px;
                        background-color:#fff;
                        text-align:center;
                        line-height:35px;
                        vertical-align: middle;
                        }
                </style>
            {% endmacro %}

            {% macro html(this,kwargs) %}
				<img id="{{this.get_name()}}" alt="toggle scroll"
					 src="https://cdn2.iconfinder.com/data/icons/e-commerce-4/256/Searching-256.png"
					 style="z-index: 999999"
					 onclick="{{this._parent.get_name()}}.toggleScroll()"
					 title="Click to toggle scroll"/>
            {% endmacro %}

            {% macro script(this,kwargs) %}
                    {{this._parent.get_name()}}.scrollEnabled = true;

                    {{this._parent.get_name()}}.toggleScroll = function() {
                        if (this.scrollEnabled) {
                            this.scrollEnabled = false;
                            this.scrollWheelZoom.disable();
                            }
                        else {
                            this.scrollEnabled = true;
                            this.scrollWheelZoom.enable();
                            }
                        };

                    {{this._parent.get_name()}}.toggleScroll();
            {% endmacro %}
            """)
			
class Fullscreen(MacroElement):
    """
    Adds a fullscreen button to your map.

    Parameters
    ----------
    position : str
          change the position of the button can be:
          'topleft', 'topright', 'bottomright' or 'bottomleft'
          default: 'topleft'
    title : str
          change the title of the button,
          default: 'Full Screen'
    title_cancel : str
          change the title of the button when fullscreen is on,
          default: 'Exit Full Screen'
    force_separate_button : boolean
          force seperate button to detach from zoom buttons,
          default: False
    See https://github.com/brunob/leaflet.fullscreen for more information.

    """
    def __init__(self, position='topleft', title='Full Screen',
                 title_cancel='Exit Full Screen', force_separate_button=False):
        super(Fullscreen, self).__init__()
        self._name = 'Fullscreen'
        self.position = position
        self.title = title
        self.title_cancel = title_cancel
        self.force_separate_button = str(force_separate_button).lower()

        self._template = Template("""
        {% macro script(this, kwargs) %}
            L.control.fullscreen({
                position: '{{this.position}}',
                title: '{{this.title}}',
                titleCancel: '{{this.title_cancel}}',
                forceSeparateButton: {{this.force_separate_button}},
                }).addTo({{this._parent.get_name()}});
            {{this._parent.get_name()}}.on('enterFullscreen', function(){
                console.log('entered fullscreen');
            });

        {% endmacro %}
        """)  # noqa

    def render(self, **kwargs):
        super(Fullscreen, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/leaflet.fullscreen/1.4.2/Control.FullScreen.min.js'),  # noqa
            name='Control.Fullscreen.js'
        )

        figure.header.add_child(
            CssLink('https://cdnjs.cloudflare.com/ajax/libs/leaflet.fullscreen/1.4.2/Control.FullScreen.min.css'),  # noqa
            name='Control.FullScreen.css'
        )
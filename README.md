# Verna

<a href="https://pypi.org/project/verna"><img alt="PyPI" src="https://img.shields.io/pypi/v/verna"></a>
<img alt="Build Status" src="https://api.travis-ci.com/ju-sh/verna.svg?branch=master"></img>
<a href="https://github.com/ju-sh/verna/blob/master/LICENSE.md"><img alt="License: MIT" src="https://img.shields.io/pypi/l/verna"></a>

A simple module to handle colors

Only RGBA colors are supported at the moment.

---

<h2>Installation</h2>

You need Python>=3.6 to use Verna.

It can be installed from PyPI with pip using

    pip install verna

---

<h2>Usage</h2>

Colors are represented using objects of class `Color`.

The color value is essentially stored as an integer as the `integer` attribute.

The following properties can be used to access the different color components.

    color.alpha
    color.red
    color.green
    color.blue

where `color` is an instance of `Color`.

The different color components can be edited with one of the following values

 - a percentage in string form with a '%' at the end (eg: "20%")
 - an integer from 0 to 255 (eg: 0xff, 255)
 - a float from 0.0 to 1.0 (only for `alpha` property. eg: 0.4)

So, the following are valid:

    color = Color(0x00ffff)
    color.alpha = 0x80
    color.alpha = "50%"
    color.alpha = 0.5   # float values can be assigned
                        # only to alpha property

    color.red = 0xff    # Same as color.red = 255
    color.red = "100%"
    color.green = 217
    color.green = "85%"
    color.blue = 0xf5
    color.blue = "96%"

whereas the following will cause error:

    color = Color(0x00ffff)
    color.alpha = 0x1ff    # > 0xff
    color.alpha = -1       # < 0.0
    color.alpha = "120%"   # > 100%
    color.alpha = "120"    # No '%' at end
    color.alpha = 1.2      # > 1.0
    color.alpha = True     # Invalid type: bool
    color.red = 0.5        # float value accepted only for alpha

A `Color` object may be created in multiple ways.

By default, alpha value is `0`.

<h6>From integer color code</h6>

For example, cyan (solid), which has color code `0x00ffff` can be created like

    Color(0x00ffff)

which is same as

    Color(65535)

<h6>From color name</h6>

`Color.from_name()` can be used to create `Color` objects from a [CSS3 color name](https://www.w3.org/wiki/CSS3/Color/Extended_color_keywords).

For example, cyan can be created with

    Color.from_name('cyan')

<h6>From RGBA values</h6>

`Color.from_rgba()` can be used to create an instance of `Color` from RGBA values.

    Color.from_rgba(255, 255, 0)         # solid yellow
    Color.from_rgba(255, 255, 0, 0.5)    # translucent yellow


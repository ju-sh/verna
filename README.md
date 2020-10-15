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




You can create color object in multiple ways.

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

---

<h2>What does the name mean</h2>


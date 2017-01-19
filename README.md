# georand

Simple python program to generate a set of random points within a bounding box to test GIS-applications.

Run `python georand.py -h` and see example.sh for usage.

## Properties

Properties are a `|`-delimited string, each with the format of:
~~~
propertyname:definition
~~~
`definition` is either a range of integer (e.g. 1-10) or float values (e.g. 0.1-1.0) or a set of string values (e.g. low-medium-high).

Full example:
~~~
"num:1-10|cat:new-old-revised|magnitude:0.1-7.0"
~~~

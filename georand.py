
import argparse
import json
import random

try:
    import geojson
except:
    print("Missing dependency: geojson (pip install geojson)")

def parse_bbox_str(bbox_str):
    bbox = bbox_str.split(" ")
    bbox = [float(num) for num in bbox]
    return bbox

def parse_properties(prop_str):
    props = prop_str.split("|")
    props = [prop.split(":") for prop in props]
    out_props = []
    for prop_idx, prop in enumerate(props):
        ranges = prop[1].split("-")
        if len(ranges) == 2:
            if ranges[0].isdigit() and ranges[1].isdigit():
                ranges[0] = int(ranges[0])
                ranges[1] = int(ranges[1])
                prop_type = "int"
            else:
                try:
                    ranges[0] = float(ranges[0])
                    ranges[1] = float(ranges[1])
                    prop_type = "float"
                except:
                    prop_type = "str"
        else:
            prop_type = "str"
        out_props.append([prop[0], ranges, prop_type])
    return out_props

ap = argparse.ArgumentParser(description="Generate random points as geojson")
ap.add_argument("-b", "--bbox",
              dest="bbox",
              default="-179.9 -79.9 179.9 79.9",
              help="Bounding Box to generate random points (Lat/Lon, minx miny maxx maxy)")

ap.add_argument("-n", "--number-of-points",
              dest="points",
              type=int,
              default=100,
              help="Number of points to generate")

ap.add_argument("-o", "--output-file",
            dest="output_file",
            default="out.geojson",
            help="Geojson output file")

ap.add_argument("-p", "--properties",
            dest="properties",
            help="Properties for random selection, e.g. num:1-10|cat:new-old-revised|magnitude:0.1-7.0")

ap.add_argument("-i", "--indentation",
            dest="indentation",
            type=int,
            default=None,
            help="Indentation level for the geojson file")

ap.add_argument('outfile', nargs=argparse.REMAINDER)

args = ap.parse_args()

points = args.points
bbox = parse_bbox_str(args.bbox)
outfile = args.output_file
properties = parse_properties(args.properties)
indentation = args.indentation

if outfile == "out.geojson":
    outfile = args.outfile[0]

ogc_fid = 1

features = []

for i in range(0, points):
    x = random.uniform(bbox[0], bbox[2])
    y = random.uniform(bbox[1], bbox[3])

    point = geojson.Point((x, y))

    feature = geojson.Feature(geometry=point)
    feature["properties"]["ogc_fid"] = ogc_fid
    for prop in properties:
        if prop[2] == "str":
            feature["properties"][prop[0]] = random.choice(prop[1])
        elif prop[2] == "int":
            feature["properties"][prop[0]] = random.randint(prop[1][0], prop[1][1])
        elif prop[2] == "float":
            feature["properties"][prop[0]] = random.uniform(prop[1][0], prop[1][1])

    features.append(feature)

    ogc_fid += 1

fc = geojson.FeatureCollection(features)

fc["crs"] = {
    "type": "name",
    "properties": {
      "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
      }
    }

with open(outfile, "w+") as fh:
    json.dump(fc, fh, indent=indentation)

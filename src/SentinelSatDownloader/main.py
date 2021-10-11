from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt, make_path_filter
from flask import Flask, request
import numpy as np

from flask_restful import reqparse

app = Flask(__name__)
# http://localhost:105/persist?position=10 11&fromdate=YYYYMMDD&todate=YYYYMMDD
@app.route('/download', methods=['GET', 'POST'])
def download():
    parser = reqparse.RequestParser()
    parser.add_argument('position', type=str, help='a list of positions -> lat lon')
    parser.add_argument('fromdate', type=str, help="The earliest date to get map data from -> 'YYYYMMDD'")
    parser.add_argument('todate', type=str, help="The latest date to get map data from -> 'YYYYMMDD' or 'NOW' for current date")

    args = parser.parse_args()
    
    positions = args.position.split()
    args.position = [float(positions[0]), float(positions[1])]

    #Download satelite imagery of beach locations to sentinelsat/downloads
    user = "nikolai.damm"
    password = "fywfuP-qekfut-xomki3"

    # Creates a small rectangle boundary box around a position, where the position is at the center of the rectangle.
    latRectSize = 0.005
    longRectSize = 0.0025
    topLeftCorner = f"{args.position[0]-latRectSize} {args.position[1]+longRectSize}"
    bottomLeftCorner = f"{args.position[0]-latRectSize} {args.position[1]-longRectSize}"
    bottomRightCorner = f"{args.position[0]+latRectSize} {args.position[1]-longRectSize}"
    topRightCorner = f"{args.position[0]+latRectSize} {args.position[1]+longRectSize}"

    # Creates a GeoJSON rectangle query in the well known text (wtk) format that queries the sentinel satellite for maps that contain our rectangle query.
    rectangleQuery = f"POLYGON (({topLeftCorner}, {bottomLeftCorner}, {bottomRightCorner}, {topRightCorner}, {topLeftCorner}))"

    # Queries the sentinel satellite with predefined parameters
    api = SentinelAPI(user, password)
    623680114746094
    products = api.query(rectangleQuery,
                platformname = 'Sentinel-2',
                processinglevel = 'Level-2A',
                date = (args.fromdate, args.todate),
                cloudcoverpercentage=(0, 20))

    # Downloads selected data based on the query above
    nodefilter = make_path_filter("*/granule/*/img_data/r10m/*_tci_10m.jp2")
    api.download_all(products, "downloads", nodefilter=nodefilter)
    return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)


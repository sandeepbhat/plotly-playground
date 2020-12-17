import json
import plotly.express as plotlyex
import pandas
import geopandas
from shapely import wkt


def parse_config(config_path: str) -> dict:
    with open(config_path) as conf:
        return json.load(conf)


if __name__ == "__main__":
    config = parse_config("config.json")

    traffic_cameras = pandas.read_json(
        config["api_base"].format(config["app_id"], config["api_format"]))

    traffic_cameras["Geometry"] = [
        value["WGS84"] for _, value in traffic_cameras["Geometry"].items()]

    # Refer https://geopandas.readthedocs.io/en/latest/gallery/create_geopandas_from_pandas.html
    traffic_cameras["Geometry"] = traffic_cameras["Geometry"].apply(wkt.loads)

    geo_df = geopandas.GeoDataFrame(traffic_cameras, geometry="Geometry")

    plotlyex.set_mapbox_access_token(config["mapbox_token"])

    fig = plotlyex.scatter_mapbox(
        geo_df, lat=geo_df.geometry.y, lon=geo_df.geometry.x, hover_name="CameraImageUrl", zoom=1)

    fig.show()

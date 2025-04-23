Currently the GetRasterExecutor and GeoJsonExecutor are the only queries that are working

# Importing the executors:

For GetRasterExecutor:

  from iharp_query_executor.get_raster_api import GetRasterExecutor

For GeoJsonExecutor:

  from iharp_query_executor.get_geojson_executor import GeoJsonExecutor


# To use the executors:

  For GetRasterExecutor:

    raster = GetRasterExecutor(
      variable=variable,
      start_datetime=start_datetime,
      end_datetime=end_datetime,
      temporal_resolution=temporal_resolution,
      min_lat=min_lat,
      max_lat=max_lat,
      min_lon=min_lon,
      max_lon=max_lon,
      spatial_resolution=spatial_resolution,
      aggregation=aggregation,
  )

  For GeoJsonExecutor:

    geojson = GeoJsonExecutor(
      variable=variable,
      start_datetime=start_datetime,
      end_datetime=end_datetime,
      temporal_resolution=temporal_resolution,
      min_lat=min_lat,
      max_lat=max_lat,
      min_lon=min_lon,
      max_lon=max_lon,
      spatial_resolution=spatial_resolution,
      aggregation=aggregation,
      geojson_file=geojson_file
  )
class GeoInterfaceMixin():
    """Implementation of __geo_interface__

    https://gist.github.com/sgillies/2217756

    """
    def __get_geo_interface_geodata__(self):
        """returns type and coordinates for __geo_interface__

        """

        if self.geom_type is "Point":
            return {'type': 'Point',
                    'coordinates': tuple(self.coords[0])
                    }
        elif self.geom_type in ['MultiPoint',]:
            return {'type': self.geom_type,
                    'coordinates': [geom.coords[0] for geom in self.geoms],
                    }
        elif self.geom_type in ['LineString', 'LinearRing']:
            return {'type': self.geom_type,
                    'coordinates': self.coords
                    }
        elif self.geom_type in ['MultiLineString',]:
            coords = []
            for geom in self.geoms:
                eachmulticoords = geom.coords
                coords.append(eachmulticoords)
            return {'type': self.geom_type,
                    'coordinates': coords
                    }
        elif self.geom_type in ['Polygon',]:
            coords = [self.exterior.coords]
            _holes = [hole.coords for hole in self.interiors]
            if _holes:
                coords.extend(_holes)
            return {'type': self.geom_type,
                    'coordinates': coords
                    }
        elif self.geom_type in ['MultiPolygon',]:
            coords = []
            for geom in self.geoms:
                eachmulticoords = [geom.exterior.coords]
                _holes = [hole.coords for hole in geom.interiors]
                if _holes:
                    eachmulticoords.extend(_holes)
                coords.append(eachmulticoords)
            return {'type': self.geom_type,
                    'coordinates': coords
                    }

    def __get_geo_interface_bbox__(self):
        """returns bbox for __geo_interface__

        Currently creates a bbox for points whereas __geo_interface__ implementation in pyshp doesn't, need
        to clarify what the proper behaviour should be for GeoJSON data and standardize.

        """
        return {'bbox': tuple(self.bounds)}

    def __get_geo_interface_properties__(self):
        """returns bbox for __geo_interface__"""
        return {'properties': self.properties}

    @property
    def __geo_interface__(self):
        geojson = {}
        geojson.update(self.__get_geo_interface_geodata__())
        geojson.update(self.__get_geo_interface_bbox__())
        if hasattr(self, 'properties'):
            geojson.update(self.__get_geo_interface_properties__())
        return geojson

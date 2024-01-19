import re
from qgis.core import QgsVectorLayer, QgsProject, QgsDataSourceUri, Qgis, QgsMapLayer




def create_layer(layer_name, typename):
    """Create a layer from WFS service."""

    testmiljo = True
    wfst = False
    username = 'kom201'
    password = '7w9w6DQm'

    # Get all layers
    layers = [layer.name() for layer in QgsProject.instance().mapLayers().values()]

    if layer_name not in layers:
        preferCoordinatesForWfsT11 = 'false'
        restrictToRequestBBOX = '1'
        srsname = 'EPSG:25832'

        if not testmiljo and not wfst:
            url = f'https://geofa.geodanmark.dk/ows/fkg/fkg'
            pagingEnabled = 'false'
        if not testmiljo and wfst:
            url = f'https://geofa.geodanmark.dk/wfs/{username}@fkg/fkg/25832'
            pagingEnabled = 'true'
        if testmiljo and not wfst:
            url = f'https://geofa-test.geodanmark.dk/ows/fkg/fkg'
            pagingEnabled = 'false'
        if testmiljo and wfst:
            url = f'https://geofa-test.geodanmark.dk/wfs/{username}@fkg/fkg/25832'
            pagingEnabled = 'true'
        version = 'auto'

        if wfst:
            # Create connection string
            connection_string = f"user={username}@fkg " \
                                f"password={password} " \
                                f"pagingEnabled={pagingEnabled} " \
                                f"preferCoordinatesForWfsT11={preferCoordinatesForWfsT11} " \
                                f"restrictToRequestBBOX={restrictToRequestBBOX} " \
                                f"srsname={srsname} " \
                                f"typename={typename} " \
                                f"url={url} " \
                                f"version={version}"

        if not wfst:
            connection_string = f"pagingEnabled={pagingEnabled} " \
                                f"preferCoordinatesForWfsT11={preferCoordinatesForWfsT11} " \
                                f"restrictToRequestBBOX={restrictToRequestBBOX} " \
                                f"srsname={srsname} " \
                                f"typename={typename.replace('fkg:','fkg:fkg.')} " \
                                f"url={url} " \
                                f"version={version}"

        # Create the QgsDataSourceUri object
        uri = QgsDataSourceUri(connection_string)

        # Add the vector layer
        layer = QgsVectorLayer(uri.uri(False), layer_name, "WFS")

        print(0)

create_layer("Skoledistrikter", "fkg:t_5710_born_skole_dis")

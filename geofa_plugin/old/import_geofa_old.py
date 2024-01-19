from qgis.core import QgsVectorLayer, QgsProject, QgsDataSourceUri, Qgis, QgsMapLayer, QgsSettings
import os
import os.path
from .config import Settings
class import_geofa:
    def generate_menu_items(self):
        """Generate the menu items as a function."""
        # to edit menu names edit the one to the right of the colon the left one is the key for the action and
        # should not be changed unless it's absolutely necessary
        menu_items = {
            "Administration": {
                "Skoledistrikter": "Skoledistrikter",
                "Andre distrikter": "Andre distrikter",
                "Pleje- og ældredistrikter": "Pleje- og ældredistrikter",
                "Prognose- og statistik distrikter": "Prognose- og statistik distrikter"
            },
            "Sport, fritid og friluftsliv": {
                "Friluftsliv faciliteter, punkter": "Friluftsliv faciliteter, punkter",
                "Friluftsliv faciliteter, flader": "Friluftsliv faciliteter, flader",
                "Friluftsliv faciliteter, linjer": "Friluftsliv faciliteter, linjer"
            },
            "Vej og trafik": {
                "Ladefaciliteter": "Ladefaciliteter"
            },
        }
        return menu_items

    def run_action(self, submenu, plugin_path, update=False):
        """Perform work based on the action name."""

        # Get menu items
        menu_items = import_geofa.generate_menu_items(self)

        # Run actions
        if submenu == menu_items["Administration"]["Skoledistrikter"]:
            import_geofa.create_geofa_layer(self, submenu, "fkg:t_5710_born_skole_dis", plugin_path, update=update)
        elif submenu == menu_items["Administration"]["Andre distrikter"]:
            import_geofa.create_geofa_layer(self, submenu, "fkg:t_5711_and_dis", plugin_path, update=update)
        elif submenu == menu_items["Administration"]["Pleje- og ældredistrikter"]:
            import_geofa.create_geofa_layer(self, submenu, "fkg:t_5712_plej_aeldr_dis", plugin_path, update=update)
        elif submenu == menu_items["Administration"]["Prognose- og statistik distrikter"]:
            import_geofa.create_geofa_layer(self, submenu, "fkg:t_5713_prog_stat_dis", plugin_path, update=update)

        elif submenu == menu_items["Sport, fritid og friluftsliv"]["Friluftsliv faciliteter, punkter"]:
            import_geofa.create_geofa_layer(self, submenu, "fkg:t_5800_fac_pkt", plugin_path, update=update)
        elif submenu == menu_items["Sport, fritid og friluftsliv"]["Friluftsliv faciliteter, flader"]:
            import_geofa.create_geofa_layer(self, submenu, "fkg:t_5801_fac_fl", plugin_path, update=update)
        elif submenu == menu_items["Sport, fritid og friluftsliv"]["Friluftsliv faciliteter, linjer"]:
            import_geofa.create_geofa_layer(self, submenu, "fkg:t_5802_fac_li", plugin_path, update=update)

        elif submenu == menu_items["Vej og trafik"]["Ladefaciliteter"]:
            import_geofa.create_geofa_layer(self, submenu, "fkg:t_5607_ladefacilitet", plugin_path, update=update)

    def d_tables(self, update=False):

        # Read config
        import_geofa.readconfig(self)

        # Lists of all d_tables
        d_tables = ["d_5607_ladefacilitet_type",
                    "d_5607_tilgaengelighed_type",
                    "d_5607_effekt_type",
                    "d_5710_udd_distrikt_type",
                    "d_5711_an_distrikt_type",
                    "d_5712_plej_distrikt_type",
                    "d_5713_prog_distrikt_type",
                    "d_5800_facilitet",
                    "d_5800_saeson",
                    "d_5800_kvalitet",
                    "d_5802_certifi",
                    "d_5802_svaerhed",
                    "d_5802_rutetype",
                    "d_5802_rute_uty",
                    "d_5802_kategori",
                    "d_5802_hierarki",
                    "d_basis_trin",
                    "d_basis_handicapegnet",
                    "d_basis_ansvarlig_myndighed",
                    "d_basis_ja_nej",
                    "d_basis_oprindelse",
                    "d_basis_status",
                    "d_basis_offentlig",
                    "d_basis_belaegning",
                    "d_basis_planstatus",
                    "d_basis_ansva_v"]

        # Get all layers
        layers = [layer.name() for layer in QgsProject.instance().mapLayers().values()]

        # Add missing layers
        for d_table in d_tables:
            if d_table not in layers or update:

                if not self.testmiljo:
                    url = f"https://geofa.geodanmark.dk/api/v2/sql/fkg?q=SELECT%20*%20FROM%20fkg.{d_table}"
                if self.testmiljo:
                    # virker ikke med test lige pt. ændre når det gør
                    url = f"https://geofa.geodanmark.dk/api/v2/sql/fkg?q=SELECT%20*%20FROM%20fkg.{d_table}"

                if update:
                    layer = QgsProject.instance().mapLayersByName(d_table)[0]
                    layer.setDataSource(url, d_table, "ogr")
                    layer.reload()
                else:
                    dlayer = QgsVectorLayer(url, d_table, "ogr")

                    # Set layer properties
                    # https://gis.stackexchange.com/questions/318506/setting-layer-identifiable-seachable-and-removable-with-python-in-qgis-3
                    dlayer.setFlags(
                    QgsMapLayer.LayerFlag(QgsMapLayer.Private + QgsMapLayer.Removable + QgsMapLayer.Searchable))

                    # Check if the layer was loaded successfully
                    if dlayer.isValid():
                        QgsProject.instance().addMapLayer(dlayer)
                    else:
                        self.iface.messageBar().pushMessage("Error", f'{dlayer.name()} could not be loaded.',
                                                        level=Qgis.Critical)

    def create_geofa_layer(self, layer_name, typename, plugin_path, update=False, ):
        """Create a layer from WFS service."""

        # Get plugin path
        plugin_path = plugin_path

        # Read config
        import_geofa.readconfig(self)

        # Add d_tables to project
        import_geofa.d_tables(self)

        # Get all layers
        layers = [layer.name() for layer in QgsProject.instance().mapLayers().values()]

        if layer_name not in layers or update:
            preferCoordinatesForWfsT11 = 'false'
            restrictToRequestBBOX = '1'
            srsname = 'EPSG:25832'

            if not self.testmiljo and not self.wfst:
                url = f'https://geofa.geodanmark.dk/ows/fkg/fkg'
                pagingEnabled = 'false'
            if not self.testmiljo and self.wfst:
                url = f'https://geofa.geodanmark.dk/wfs/{self.username}@fkg/fkg/25832'
                pagingEnabled = 'true'
            if self.testmiljo and not self.wfst:
                url = f'https://geofa-test.geodanmark.dk/ows/fkg/fkg'
                pagingEnabled = 'false'
            if self.testmiljo and self.wfst:
                url = f'https://geofa-test.geodanmark.dk/wfs/{self.username}@fkg/fkg/25832'
                pagingEnabled = 'true'

            version = 'auto'

            # Create connection string
            if self.wfst:

                connection_string = f"user={self.username}@fkg " \
                                    f"password={self.password} " \
                                    f"pagingEnabled={pagingEnabled} " \
                                    f"preferCoordinatesForWfsT11={preferCoordinatesForWfsT11} " \
                                    f"restrictToRequestBBOX={restrictToRequestBBOX} " \
                                    f"srsname={srsname} " \
                                    f"typename={typename} " \
                                    f"url={url} " \
                                    f"version={version}"

            if not self.wfst:
                connection_string = f"pagingEnabled={pagingEnabled} " \
                                    f"preferCoordinatesForWfsT11={preferCoordinatesForWfsT11} " \
                                    f"restrictToRequestBBOX={restrictToRequestBBOX} " \
                                    f"srsname={srsname} " \
                                    f"typename={typename.replace('fkg:','fkg:fkg.')} " \
                                    f"url={url} " \
                                    f"version={version}"

            # Create the QgsDataSourceUri object
            uri = QgsDataSourceUri(connection_string)

            # Add svg path, so it can find symbols used in the styles
            # https://gis.stackexchange.com/questions/281698/relative-path-to-the-plugin-folder-for-svg-file-in-qgis3-sld-file
            svg_paths = QgsSettings().value('svg/searchPathsForSVG')
            if plugin_path not in svg_paths:
                QgsSettings().setValue('svg/searchPathsForSVG', svg_paths + [plugin_path+"/geofa_symboler"])

            if update:
                layer = QgsProject.instance().mapLayersByName(layer_name)[0]
                layer.setDataSource(uri.uri(False), layer_name, "WFS")
                layer.triggerRepaint()

            else:
                layer = QgsVectorLayer(uri.uri(False), layer_name, "WFS")

                # Load style
                style = os.path.join(os.path.dirname(__file__), f'qml/{layer_name}.qml')
                layer.loadNamedStyle(style)

                # Check if the layer was loaded successfully
                if layer.isValid():
                    QgsProject.instance().addMapLayer(layer)
                else:
                    self.iface.messageBar().pushMessage("Error", f'{layer_name} could not be loaded.',level=Qgis.Critical)
        else:
            self.iface.messageBar().pushMessage("Error", f'{layer_name} already exists.', level=Qgis.Info, duration=5)

    def readconfig(self):
        settings = Settings()  # new config
        self.username = settings.value('username')
        self.password = settings.value('password')
        self.wfst = settings.value('wfst')
        self.testmiljo = settings.value('testmiljo')
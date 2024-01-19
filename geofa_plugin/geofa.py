# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoFA
                                 A QGIS plugin
 GeoFA
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-07-18
        git sha              : $Format:%H$
        copyright            : (C) 2023 by geofa
        email                : geofa
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu
import os
import os.path
from .config import Settings, OptionsFactory
from PyQt5.QtGui import QDesktopServices
from qgis.PyQt.QtCore import QUrl
from .layerlocatorfilter import LayerLocatorFilter
from .import_geofa import import_geofa
import webbrowser
from qgis.core import QgsProject, QgsExpressionContextUtils

OM_GEOFA_URL = (
        "https://www.geodanmark.dk/home/vejledninger/geofa/"
)

class GeoFA:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GeoFA_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # new config method
        self.settings = Settings()
        self.options_factory = OptionsFactory(self.settings)
        self.options_factory.setTitle('GeoFA')
        iface.registerOptionsWidgetFactory(self.options_factory)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&GeoFA')

        self.layer_locator_filter = LayerLocatorFilter()
        self.iface.registerLocatorFilter(self.layer_locator_filter)

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GeoFA', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.menu = QMenu("&GeoFA", self.iface.mainWindow().menuBar())
        actions = self.iface.mainWindow().menuBar().actions()
        self.iface.mainWindow().menuBar().insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.menu)

        menu_items = import_geofa.generate_menu_items()
        searchable_layers = []
        for main_menu, submenus in menu_items.items():
            menu = self.menu.addMenu(main_menu)
            for submenu in submenus:
                q_action = menu.addAction(submenu, lambda submenu=submenu: self.run_action(submenu, self.plugin_dir))
                searchable_layers.append(
                    {
                        "title": submenu,
                        "category": main_menu,
                        "action": q_action,
                    })

        self.menu.addSeparator()
        self.layer_locator_filter.set_searchable_layers(searchable_layers)

        # Add about
        icon_path_info = os.path.join(os.path.dirname(__file__), "icon_about.png")
        self.about_menu = QAction(QIcon(icon_path_info), self.tr("Om pluginet") + "...", self.iface.mainWindow(),)
        self.about_menu.setObjectName(self.tr("Om pluginet"))
        self.about_menu.triggered.connect(self.about_dialog)
        self.menu.addAction(self.about_menu)

        # Add manual link
        icon_path_manual = os.path.join(os.path.dirname(__file__), "manual_icon.png")
        self.manual_menu = QAction(QIcon(icon_path_manual), self.tr("Vejledning"), self.iface.mainWindow(),)
        self.manual_menu.setObjectName(self.tr("Vejledning"))
        self.manual_menu.triggered.connect(self.open_pdf_manual)
        self.menu.addAction(self.manual_menu)

    def run_action(self, submenu, plugin_path):
        self.readconfig()
        import_geofa.run_action(self, submenu, plugin_path)

    def about_dialog(self):
        QDesktopServices.openUrl(QUrl(OM_GEOFA_URL))

    def open_pdf_manual(self):
        # Open pdf manual
        webbrowser.open_new(os.path.join(self.plugin_dir, "GeoFA_plugin_vejledning.pdf"))

    def readconfig(self):
        settings = Settings()  # new config
        self.username = settings.value('username')
        self.password = settings.value('password')
        self.wfst = settings.value('wfst')
        self.testmiljo = settings.value('testmiljo')

        # Set project variables
        QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(), 'geofa_bruger_id', self.username)

    def unload(self):
        self.menu.deleteLater()
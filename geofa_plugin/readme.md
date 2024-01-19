# QGIS GeoFA Plugin

The QGIS GeoFA plugin allows you to load WFS data from GeoFA and import it directly into your QGIS project. Additionally, you have the option to input user credentials if you need access to WFS-T, enabling you to modify the data.

## Prerequisites

Before using the plugin, you must have QGIS installed with OSGeo4W. If you haven't installed it yet, visit https://qgis.org to get the latest version.

## Setting up PyCharm with QGIS Libraries

To work with the GeoFA plugin in PyCharm, follow these steps to make PyCharm aware of QGIS libraries:

1. Open C:\OSGeo4W\ folder and create a batch file named `qgis_env.bat` with the following content:

```Batch 
@echo off
SET OSGEO4W_ROOT=C:\OSGeo4W
call "%OSGEO4W_ROOT%"\bin\o4w_env.bat

@echo off
path %PATH%;%OSGEO4W_ROOT%\apps\qgis-ltr\bin
path %PATH%;%OSGEO4W_ROOT%\apps\grass\grass78\lib
path %PATH%;C:\OSGeo4W\apps\Qt5\bin
path %PATH%;C:\OSGeo4W\apps\Python39\Scripts

set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis-ltr\python
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python39

start "PyCharm aware of QGIS" /B "C:\Users\hbl\AppData\Local\JetBrains\PyCharm 2023.1.1\bin\pycharm64.exe" %*
```

2. Run the `qgis_env.bat` batch file to start PyCharm with QGIS libraries.


## Deploying the Plugin

In the plugin folder there is a file **pyQGIS.bat**. This file makes us capable to use all the libris included with QGIS.

Check the content of the file and make sure you do have the correct folders and that the paths fits your system. Especially the python path may change depending on which version of python that comes along with your QGIS installation. Notice also that you need to have 7-zip installed and add the correct path to this, if anything is different please make a new file and end it with your initials.

To deploy the plugin to QGIS and create the ZIP file, you can use `pb_tool`, which is a handy tool for QGIS plugin development. To install pb_tool in the CMD run:

```
python -m pip install pb_tool
```

Now we can deploy the QGIS plugin, run the **pyQGIS.bat** and run the following:

```
pb_tool deploy
```
write "y" for yes and pb_tool will deploy the plugin to the QGIS plugin directory.

If you open QGIS now and go to "Plugins > Manage and Install Plugins..." you can find the plugin in the in the installed tab and you can activate it.

If this does not work, you may need to tell pb_tool where the plugins needs to be deployed to, **pb_tool.cfg** file and go to this location:

```
# Full path to where you want your plugin directory copied. If empty,
# the QGIS default path will be used. Don't include the plugin name in
# the path.
plugin_path: 
```

And add the path so it looks for example like this:

```
plugin_path: C:\Users\hbl\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins
```

Save the file afterwards.

## Notes
The main logic of the plugin resides in the `import_geofa.py` module. This module handles the import of individual WFS layers and domain value tables from the GeoFA SQL API.

## Future Improvements
In the future, the plugin can be enhanced with the following features:

1. Handling the layers using QLR files saved in the GeoFA database, thus avoiding hardcoded WFS layers.

## Contributing

If you want to contribute to the development of the QGIS GeoFA plugin, please follow the standard guidelines for contributing to open-source projects. Fork the repository, make your changes, and submit a pull request.

## License

The QGIS GeoFA plugin is licensed under the GNU General Public License v2.0 (GPL-2.0). You can find the full license text in the [LICENSE](LICENSE) file.

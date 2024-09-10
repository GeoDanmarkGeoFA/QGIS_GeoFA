@echo off
SET OSGEO4W_ROOT=C:\OSGeo4W
call "%OSGEO4W_ROOT%"\bin\o4w_env.bat

@echo off
path %PATH%;%OSGEO4W_ROOT%\apps\qgis-ltr\bin
path %PATH%;%OSGEO4W_ROOT%\apps\grass\grass83\lib
path %PATH%;C:\OSGeo4W\apps\Qt5\bin
path %PATH%;C:\OSGeo4W\apps\Python39\Scripts

set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis-ltr\python
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python312
set PATH=%PATH%;C:\Program Files\7-Zip\

cd /d %~dp0

cmd.exe
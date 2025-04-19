import json
import os
import sys
from pathlib import Path

import pynmea2
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QSize, QUrl, QObject, pyqtSlot, QEventLoop
from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal, QEventLoop
from PyQt6.QtNetwork import QNetworkAccessManager
from gprlibpy.widgets.map_viewer.map_elements import Marker, Circle, Polyline, Polygon, Rectangle, BaseModel



class MapViewerFrontendEventHandler(QObject):
    """
    Handle events from the frontend
    """
    mapClicked = pyqtSignal(float, float)  # Signal emitted when a map click occurs
    mapReady = pyqtSignal()  # Signal emitted when the map is ready

    def __init__(self, map_viewer: "MapViewer", api_key: str):
        super(MapViewerFrontendEventHandler, self).__init__()
        self.map_viewer = map_viewer
        self.api_key = api_key

    @pyqtSlot()
    def getApiKey(self):
        """
        Sends the API key to the web page when requested.
        """
        script = f"loadGoogleMaps('{self.api_key}');"
        self.map_viewer.page().runJavaScript(script)

    @pyqtSlot()
    def on_map_ready(self):
        """Handles event when the map is ready to receive elements."""
        print("Map is fully initialized and ready for interactions.")
        self.mapReady.emit()

    @pyqtSlot(str)
    def log(self, msg):
        """
        Print a message
        """
        print(f"Log from JS: {msg}")



class MapViewer(QWebEngineView):
    """
    A simple map viewer that can display a map and add markers, polylines, and polygons.
    """

    def __init__(self, api_key: str, provider="gmap", *args, **kwargs):
        super(MapViewer, self).__init__(*args, **kwargs)

        # Initialize the map viewer
        self.initialized = False
        self.channel = QWebChannel()
        self.web_page = self.page()
        self.web_page.setWebChannel(self.channel)
        self.map_handler = MapViewerFrontendEventHandler(self, api_key)
        # Register the map handler object with the channel
        self.channel.registerObject("qtMapViewer", self.map_handler)

        # Allow local content to access remote URLs (e.g., Google Maps API)
        settings = self.page().settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        # Load the HTML file
        file_path = Path(__file__).parent.joinpath("gmap_index.html")
        local_url = QUrl.fromLocalFile(str(file_path))
        self.load(local_url)

    def wait_for_map_ready(self):
        """Blocks execution until the map is fully loaded."""
        loop = QEventLoop()
        self.map_handler.mapReady.connect(loop.quit)
        print("Waiting for the map to be ready...")
        loop.exec()  # This will block execution until mapReady signal is emitted
        print("Map is now ready! Proceeding...")

    def run_script(self, script, callback=None):
        """
        Run a script on the page
        """
        if callback is None:
            self.page().runJavaScript(script)
        else:
            self.page().runJavaScript(script, callback)


    def set_zoom(self, zoom):
        """
        Set the zoom level of the map
        """
        self.run_script(f"gmap_setZoom({zoom})")

    def add_marker(self, marker: Marker, center_to=False):
        """
        Add a marker to the map
        """
        center_to = "true" if center_to else "false"
        json_object = marker.model_dump_json(exclude_none=True)
        code = f'gmap_addMarker({json_object}, {center_to});'
        self.run_script(code)

    def add_polyline(self, polyline: Polyline, center_to=False):
        """
        Add a polyline to the map
        """
        center_to = "true" if center_to else "false"
        json_object = polyline.model_dump_json(exclude_none=True)
        code = f'gmap_addPolyline({json_object}, {center_to});'
        self.run_script(code)

if __name__ == "__main__":
    from gprlibpy.widgets import Marker, Point, Polyline
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-logging --log-level=3"
    API_KEY = "AIzaSyACzppF9Mx55S3QgRXE25fkz1rztNJVBEw"  # Replace with your actual API key
    app = QApplication(sys.argv)
    gmap = MapViewer(api_key=API_KEY, provider="gmap")
    gmap.resize(QSize(800, 600))
    gmap.show()
    gmap.wait_for_map_ready()
    gmap.set_zoom(30)
    point = Point(lat=3.4417785092678557, lng=-76.49386837070928)
    marker = Marker(
        position=point,
        title="San Francisco",
        draggable=False
    )
    #gmap.add_marker(marker, center_to=True)
    points = [
        Point(lat=3.4417785092678557, lng=-76.49386837070928),
        Point(lat=3.4417785092678557, lng=-76.49386837070928),
        Point(lat=3.4417785092678557, lng=-76.49386837070928),
        Point(lat=3.4417785092678557, lng=-76.49386837070928),
    ]
    gmap.add_polyline(Polyline(path=points, geodesic=True, strokeColor="red", strokeOpacity=0.8, strokeWeight=2), center_to=True)
    print("Map is ready!")
    sys.exit(app.exec())

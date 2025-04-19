from pydantic import BaseModel, create_model
from typing import Optional, Type

def partial_model(model: Type[BaseModel]):
    """
    Converts all fields in a Pydantic model to Optional (nullable) types with default None.
    """
    fields = {}
    for field_name, field_type in model.__annotations__.items():
        fields[field_name] = (Optional[field_type], None)  # Make fields optional with default None
    return create_model(
        f'Partial{model.__name__}',
        __base__=model,
        __module__=model.__module__,
        **fields
    )


@partial_model
class Point(BaseModel):
    lat: float
    lng: float

@partial_model
class Marker(BaseModel):
    position: Point
    title: str
    draggable: bool

@partial_model
class Polyline(BaseModel):
    path: list[Point]
    geodesic: bool
    strokeColor: str
    strokeOpacity: float
    strokeWeight: int

@partial_model
class Polygon(BaseModel):
    paths: list[Point]
    strokeColor: str
    strokeOpacity: float
    strokeWeight: int
    fillColor: str
    fillOpacity: float

@partial_model
class Circle(BaseModel):
    center: Point
    radius: float
    strokeColor: str
    strokeOpacity: float
    strokeWeight: int
    fillColor: str
    fillOpacity: float

@partial_model
class RectangleBounds(BaseModel):
    north: float
    south: float
    east: float
    west: float

@partial_model
class Rectangle(BaseModel):
    bounds: RectangleBounds
    strokeColor: str
    strokeOpacity: float
    strokeWeight: int
    fillColor: str
    fillOpacity: float
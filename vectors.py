import math
import utils


class Scalar:
    def __init__(self, value: float, measurement_unit: str = None) -> None:
        self.value = value
        self.measurement_unit = measurement_unit


class Vector:
    def __init__(self, magnitude: float, angle: float, start: list|tuple|set, measurement_unit: str, id: str, origins = None) -> None:
        self.magnitude = magnitude
        self.angle = angle
        self.start = start
        self.id = id
        self.x = self.magnitude * math.cos(math.radians(self.angle)) if self.angle not in [90, 270] else 0
        self.y = self.magnitude * math.sin(math.radians(self.angle))
        self.origins = origins
        self.measurement_unit = measurement_unit # TODO: implement measurement units 
    
    def update(self):
        self.x = self.magnitude * math.cos(math.radians(self.angle)) if self.angle not in [90, 270] else 0
        self.y = self.magnitude * math.sin(math.radians(self.angle))
    
    def inspect(self):
        insp = f"{'_'*30}\nVector {self.id} properties:\nMAGNITUDE: {self.magnitude} {self.measurement_unit}\nANGLE: {self.angle}°\nSTART: {self.start}\nX: {self.x}\nY: {self.y}"
        if self.origins:
            insp += '\n' + f"{'FROM VECTORS: ' + self.origins}"
        return f"{insp}\n{'_'*30}\n"


class VectorOperations:
    def find_quadrant(self, components: list|tuple|set) -> int:
        x, y = components
        if x>=0 and y>=0:
            return 0
        elif (x<0 and y>0) or (x<0 and y<0):
            return 180
        elif x>0 and y<0:
            return 360
    
    def elaborate_coords(self, vector_coords: list|tuple|set) -> float:
        """Given x and y coordinates, this function returns magnitude and angle of the result vector"""
        #magnitude
        magnitude = math.sqrt(vector_coords[0]**2 + vector_coords[1]**2)
        #vector
        if vector_coords[0]==0: #I manually specified the results for angle 90 an 270 (quick answer: because in those cases result.x is 0 and it is not possible to divide by 0 any number but I had to in line 38)
            if vector_coords[1]>0:
                angle = 90
            else:
                angle = 270
        else:
            angle = math.degrees(math.atan(vector_coords[1]/vector_coords[0])) + self.find_quadrant((vector_coords[0], vector_coords[1]))
        return magnitude, angle
        
    def sum(self, vectors: list|tuple|set) -> Vector:
        result = Vector(0, 0, id="x", start=((vectors[0].start[0]+vectors[1].start[0])/2, (vectors[0].start[1]+vectors[1].start[1])/2), measurement_unit = vectors[0].measurement_unit)
        result.x = vectors[0].x + vectors[1].x
        result.y = vectors[0].y + vectors[1].y
        result.magnitude, result.angle = self.elaborate_coords((result.x, result.y))
        result.origins = f"{vectors[0].id}+{vectors[1].id}"
        return result
    
    def subtraction(self, vectors: list|tuple|set) -> Vector:
        result = Vector(0, 0, id="s", start=((vectors[0].start[0]+vectors[1].start[0])/2, (vectors[0].start[1]+vectors[1].start[1])/2), measurement_unit = vectors[0].measurement_unit)
        result.x = vectors[0].x - vectors[1].x
        result.y = vectors[0].y - vectors[1].y
        result.magnitude, result.angle = self.elaborate_coords((result.x, result.y))
        result.origins = f"{vectors[0].id}-{vectors[1].id}"
        return result
    
    def cross_product(self, vectors: list|tuple|set, id: str) -> float: #this function should return a vector but since the vector is perpendicular to the cartesian plane it's non representable in 2d, so this function only returns its magnitude
        angle_in_vectors = math.degrees(math.acos(self.dot_product(vectors).value/(vectors[0].magnitude*vectors[1].magnitude)))
        #print("aiv: ", angle_in_vectors)
        vector_magnitude = vectors[0].magnitude * vectors[1].magnitude * math.sin(angle_in_vectors)
        vector_measrement_unit = utils.rewrite_measurement_unit(vectors[0].measurement_unit, vectors[1].measurement_unit, "*")
        inspect = f"{'_'*30}\nCross product {id} properties:\nMAGNITUDE: {vector_magnitude} {vector_measrement_unit}\nFROM VECTORS: {vectors[0].id}×{vectors[1].id}\n{'_'*30}"

        return vectors, vector_magnitude, id, inspect
    
    def dot_product(self, vectors: list|tuple|set) -> float:
        return Scalar(vectors[0].x*vectors[1].x + vectors[0].y*vectors[1].y, measurement_unit=utils.rewrite_measurement_unit(vectors[0].measurement_unit, vectors[1].measurement_unit, "*"))
    
    def product(self, vector: Vector, scalar: Scalar) -> Vector:
        result = Vector(0, 0, id="p", start=vector.start, measurement_unit=utils.rewrite_measurement_unit(vector.measurement_unit, scalar.measurement_unit, "*"))
        result.x = vector.x*scalar.value
        result.y = vector.y*scalar.value
        result.magnitude, result.angle = self.elaborate_coords((result.x, result.y))
        result.origins = f"{vector.id}*{scalar.value}{scalar.measurement_unit}"
        return result
    
    def division(self, vector: Vector, scalar: Scalar) -> Vector:
        result = Vector(0, 0, id="p", start=vector.start, measurement_unit=utils.rewrite_measurement_unit(vector.measurement_unit, scalar.measurement_unit, "/"))
        result.x = vector.x/scalar.value
        result.y = vector.y/scalar.value
        result.magnitude, result.angle = self.elaborate_coords((result.x, result.y))
        result.origins = f"{vector.id}/{scalar.value}{scalar.measurement_unit}"
        return result

#TODO
#RigidBody, Force(Vector)



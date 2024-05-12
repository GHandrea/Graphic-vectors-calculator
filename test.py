from vectors import Scalar, Vector, VectorOperations
import graphics

Vo = VectorOperations()

displacement = Vector(10, 0, (0,0), "m", "Δs")
time_interval = Scalar(5, "s")

velocity = Vo.division(displacement, time_interval)
velocity.id = "Δv"

accelleration = Vo.division(velocity, time_interval)
accelleration.id = "a"

mass = Scalar(3, "kg")
force = Vo.product(accelleration, mass)
force.id = "F"

#print(velocity.inspect(), accelleration.inspect(), force.inspect())

#graphics.represent_vector(displacement)
graphics.show()
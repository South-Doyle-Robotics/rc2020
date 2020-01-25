

class Trait:
    '''
    The base class used for traits
    '''
    def __init__(self):
        raise Exception("Traits may not be instantiated! Use an object that implements this trait instead")


def implements(*traits):
    '''
    This decorator is used to implement a trait for a new class.
    Example usage:

    ```
    class Printable(Trait):
        def printme(self): pass

    @implements(Printable)
    class Robot:
        # if printme is not defined for Robot,
        # an exception will be thrown!
        def printme(self): print("Robot!")


    robot = Robot()
    if robot.implements(Printable):
        robot.printme()
    ```
    '''
    def result(class_definition):
        # For every trait that the class implements,
        # confirm the class implements all of the trait's methods
        for trait in traits:
            for method in dir(trait):
                if not method in dir(class_definition) and method[0] != "_":
                    raise Exception(class_definition.__name__ + " does not implement method `" + method + "` from trait `" + trait.__name__ + "`")
        # Add a method to the class that allows us to check which traits the class implements
        class_definition.implements = lambda self, trait: trait in traits
        return class_definition
    return result
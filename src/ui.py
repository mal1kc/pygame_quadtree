# a simple ui to create a quadtree flags to test it on run
# a textbox and reflesh button would be ideal
#  a text data [1,0,[1,0,0,0],0] this would be
from quadtree import QuadtreeFlag


examplequadtreeFlag = QuadtreeFlag(
    (
        QuadtreeFlag((None, None, None, None)),
        None,
        QuadtreeFlag((QuadtreeFlag((None, None, None, None)), None, None, None)),
        None,
    )
)

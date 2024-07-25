from renderer import Renderer
from functions_v7 import *

session = createSess(Roi="SI")
renderer = Renderer(session)
renderer.startRender()
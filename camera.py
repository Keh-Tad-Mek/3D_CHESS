import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

def setup_camera(window):
    glMatrixMode(GL_PROJECTION) # turns 3d into a 2d image for the screen
    glLoadIdentity() # clears all previous camera calculations to start fresh 

    width, height = glfw.get_window_size(window)

    aspect_ratio = width / height

    gluPerspective(
        30,  # field of view
        aspect_ratio, # aspect ratio
        0.1, # near clipping not to show anything that close to the camera
        100.0 # far clipping not to show anything further than that 
    )

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt( # where exactly the camera is setup
        0, 10, -15, # x, y, z coordinates of where the camera is setup
        0, 0, 0, # tels the camera to point at the middle of the chess board
        0, 1, 0 # 
    )

    glLightfv(GL_LIGHT0, GL_POSITION, [5, 10, 5, 1]) 
    
    # Ambient: Background light that fills shadows (0.0 to 1.0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1]) 
    
    # Diffuse: The direct light hitting surfaces
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])
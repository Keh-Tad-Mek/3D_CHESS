import glfw # graphics library framework
from OpenGL.GL import * # handles the 3d art
from OpenGL.GLU import * # utility for the GL that provides camera options and whatnot
from camera import setup_camera
from draw_pieces import init_pieces, draw_all_pieces, pieces, get_piece_at, move_piece_location, is_move_valid

cursor_x = 3 
cursor_y = 1 # cursors x and y define the position of the pointer
selected_piece_pos = None # remembers the chosen chess piece
current_turn = "white" # handles turns 

def main():
    if not glfw.init():
        print("Failed to initialize GLFW.")
        return


    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3) 
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE) # use the beginner friendly tools
    glfw.window_hint(glfw.RESIZABLE, False)
    glfw.window_hint(glfw.VISIBLE, True)

    window = glfw.create_window(1920, 1080, "3D Chess", None, None)

    if not window:
        print("Failed to create GLFW window.")
        glfw.terminate()
        return
    

    glfw.make_context_current(window) # tells the OS to draw everything on this window

    glfw.set_key_callback(window, key_callback) # loads the function that handles key presses

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glViewport(0, 0, 1920, 1080)

    init_pieces() # orders the pieces to start a game

    while not glfw.window_should_close(window): 
        # this loop makes sure that the window stays open until explicitly closed
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        setup_camera(window) # sets up the camera positions and angles
        
        draw_chess_board() # renders the chess board for the pieces to move on
        
        draw_highlights() # renders the position pointer based on where we move

        draw_all_pieces()

        glfw.swap_buffers(window) # hides the rendering and just shows the final image
        glfw.poll_events() # load all event handlers

    glfw.terminate()
    print("Window closed.")


def key_callback(window, key, scancode, action, mods):
    """
    Handles single key presses (debounce logic provided by GLFW callback)
    """
    global cursor_x, cursor_y, selected_piece_pos

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_RIGHT:
            cursor_x = max(0, cursor_x - 1)

        elif key == glfw.KEY_LEFT:
            cursor_x = min(7, cursor_x + 1)

        elif key == glfw.KEY_UP:
            cursor_y = min(7, cursor_y + 1)

        elif key == glfw.KEY_DOWN:
            cursor_y = max(0, cursor_y - 1)
        
        elif key == glfw.KEY_ENTER:
            handle_enter_key()
            
        elif key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)


def handle_enter_key():
    global selected_piece_pos, cursor_x, cursor_y, current_turn

    # --- STATE 1: SELECTION PHASE ---
    if selected_piece_pos is None:
        piece = get_piece_at(cursor_x, cursor_y) # returns info about piece at that position
        
        if piece:
            # RULE 1: Check Turn
            if piece[3] != current_turn:
                print(f"Invalid selection: It is {current_turn}'s turn!")
                return

            selected_piece_pos = (cursor_x, cursor_y)
            print(f"Selected {piece[3]} {piece[0]} at {cursor_x}, {cursor_y}")
        else:
            print("No piece at this location.")

    # --- STATE 2: MOVEMENT PHASE ---
    else:
        # Deselect if clicking same spot
        if selected_piece_pos == (cursor_x, cursor_y):
            selected_piece_pos = None
            print("Deselected.")
            return

        sx, sy = selected_piece_pos
        
        # RULE 2: Friendly Fire (Cannot capture own color)
        target_piece = get_piece_at(cursor_x, cursor_y)
        if target_piece and target_piece[3] == current_turn:
            print(f"Invalid Move: Cannot capture your own {target_piece[0]}!")
            return

        # RULE 3: Move Validation (Geometry & Path)
        valid, reason = is_move_valid(sx, sy, cursor_x, cursor_y)
        
        if valid:
            move_piece_location(sx, sy, cursor_x, cursor_y)
            selected_piece_pos = None # Reset selection
            
            # Switch Turn
            current_turn = 'black' if current_turn == 'white' else 'white'
            print(f"Move successful ({reason}). Now {current_turn}'s turn.")
        else:
            print(f"Invalid Move: {reason}")


def draw_highlights():
    """Draws the cursor (Green) and the selected tile (Red)"""
    global cursor_x, cursor_y, selected_piece_pos
    
    # 1. Draw Selected Piece Highlight (Red)
    if selected_piece_pos:
        sx, sy = selected_piece_pos
        draw_tile_highlight(sx, sy, (1.0, 0.0, 0.0)) # Red
        
    # 2. Draw Current Cursor Highlight (Green)
    draw_tile_highlight(cursor_x, cursor_y, (0.0, 1.0, 0.0)) # Green


def draw_tile_highlight(x_coord, z_coord, color):
    """Draws a solid flat square on the tile"""
    x = x_coord - 3.5
    z = z_coord - 3.5
    
    glDisable(GL_LIGHTING) 
    glColor3f(*color)
    
    # Use a tiny offset (0.02) so it sits just above the board surface
    y_surface = 0.001

    glBegin(GL_QUADS)
    glVertex3f(x, y_surface, z)
    glVertex3f(x + 1, y_surface, z)
    glVertex3f(x + 1, y_surface, z + 1)
    glVertex3f(x, y_surface, z + 1)
    glEnd()

    glEnable(GL_LIGHTING)


def draw_chess_board():
    glEnable(GL_COLOR_MATERIAL) # Ensure material colors work
    for row in range(8):
        for col in range(8):

            x = col - 3.5
            z = row - 3.5

            if (row + col) % 2 == 0: # color the board tiles white and black turn by turn
                glColor3f(0, 0, 0)
            else:
                glColor3f(1, 1, 1) 

            glBegin(GL_QUADS)
            glNormal3f(0, 1, 0) # Normal pointing up for lighting
            # drawing a square for our chess board tiles
            glVertex3f(x, 0, z)
            glVertex3f(x + 1, 0, z)
            glVertex3f(x + 1, 0, z + 1)
            glVertex3f(x, 0, z + 1) 
            glEnd()


if __name__ == "__main__":
    main()
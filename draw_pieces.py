import glfw 
from OpenGL.GL import *
from OpenGL.GLU import *

def set_piece_color(is_white):
    if is_white:
        glColor3f(0.95, 0.95, 0.95)
    else:
        glColor3f(0.15, 0.15, 0.15)
        


pieces = [] # the position of pieces is read and updated on this table

def init_pieces():
    global pieces
    pieces = [] # clears the positions of the pieces from the previous game
    
    # White pieces (bottom rows)
    for x in range(8):
        pieces.append(['pawn', x, 1, 'white'])  # White pawns
    
    # White back row
    pieces.append(['rook', 0, 0, 'white'])
    pieces.append(['knight', 1, 0, 'white'])
    pieces.append(['bishop', 2, 0, 'white'])
    pieces.append(['queen', 3, 0, 'white'])
    pieces.append(['king', 4, 0, 'white'])
    pieces.append(['bishop', 5, 0, 'white'])
    pieces.append(['knight', 6, 0, 'white'])
    pieces.append(['rook', 7, 0, 'white'])
    
    # Black pieces (top rows)
    for x in range(8):
        pieces.append(['pawn', x, 6, 'black'])  # Black pawns
    
    # Black back row
    pieces.append(['rook', 0, 7, 'black'])
    pieces.append(['knight', 1, 7, 'black'])
    pieces.append(['bishop', 2, 7, 'black'])
    pieces.append(['queen', 3, 7, 'black'])
    pieces.append(['king', 4, 7, 'black'])
    pieces.append(['bishop', 5, 7, 'black'])
    pieces.append(['knight', 6, 7, 'black'])
    pieces.append(['rook', 7, 7, 'black'])


def draw_piece(piece_type, x, y, color):
    glPushMatrix()
    
    # Convert board to 3D
    board_x = x - 3
    board_z = y - 3
    glTranslatef(board_x, 0.1, board_z)  # 0.5 = above board
    
    # Color
    if color == 'white':
        glColor3f(0.95, 0.95, 0.95)
    else:
        glColor3f(0.1, 0.1, 0.1)
    
    if piece_type == "pawn":
        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)

        glPushMatrix()
        glRotatef(-90, 1, 0, 0)

        # Scale everything down by 1/3
        glScalef(0.33, 0.33, 0.33)

        # --- 1. Base ---
        gluDisk(quadric, 0.0, 1.0, 32, 1)
        gluCylinder(quadric, 1.0, 1.0, 0.3, 32, 1)
        glTranslatef(0, 0, 0.3)
        gluDisk(quadric, 0.0, 1.0, 32, 1)

        # --- 2. Body ---
        gluCylinder(quadric, 0.9, 0.4, 1.5, 32, 1)

        # --- 3. Collar ---
        glTranslatef(0, 0, 1.4)
        gluCylinder(quadric, 0.4, 0.6, 0.1, 32, 1)
        glTranslatef(0, 0, 0.1)
        gluDisk(quadric, 0, 0.6, 32, 1)

        # --- 4. Head ---
        glTranslatef(0, 0, 0.4)
        gluSphere(quadric, 0.55, 32, 32)

        glPopMatrix()
        gluDeleteQuadric(quadric)


    elif piece_type == "rook":
        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)

        glPushMatrix()
        # Rotate to point upwards along Y-axis
        glRotatef(-90, 1, 0, 0)
        
        # Global scale to keep it manageable
        glScalef(0.3, 0.3, 0.2)

        # --- 1. The Base (Tiered) ---
        # Bottom heavy ring
        gluCylinder(quadric, 1.4, 1.4, 0.4, 32, 1)
        gluDisk(quadric, 0.0, 1.4, 32, 1) # Floor
        glTranslatef(0, 0, 0.4)
        
        # Cap the ring
        gluDisk(quadric, 1.2, 1.4, 32, 1)
        
        # Slope up to the body
        gluCylinder(quadric, 1.2, 1.0, 0.4, 32, 1)
        glTranslatef(0, 0, 0.4)

        # --- 2. The Body (Tower) ---
        # Slight taper for elegance
        gluCylinder(quadric, 1.0, 0.8, 2.5, 32, 1)
        glTranslatef(0, 0, 2.5)

        # --- 3. The Neck (Collar) ---
        # A small ring before the turret flares out
        gluCylinder(quadric, 0.8, 0.9, 0.1, 32, 1)
        glTranslatef(0, 0, 0.1)
        
        # The overhang/flare of the turret
        gluCylinder(quadric, 0.9, 1.3, 0.5, 32, 1)
        gluDisk(quadric, 0.0, 0.9, 32, 1) # Close gap from body
        glTranslatef(0, 0, 0.5)
        
        # The vertical side of the turret head
        gluCylinder(quadric, 1.3, 1.3, 0.6, 32, 1)
        glTranslatef(0, 0, 0.6)

        # --- 4. The Top (Merlons/Teeth) ---
        # Top rim surface (between outer edge and inner bowl)
        gluDisk(quadric, 0.9, 1.3, 32, 1)
        
        # Inner "bowl" (so it looks hollow)
        glTranslatef(0, 0, -0.2)
        gluCylinder(quadric, 0.9, 0.9, 0.2, 32, 1) # Inner walls
        gluDisk(quadric, 0.0, 0.9, 32, 1)          # Inner floor
        glTranslatef(0, 0, 0.2) # Move back up to the rim

        # --- The Teeth (Crenellations) ---
        # Drawing 6 blocks arranged in a circle
        num_teeth = 6
        radius = 1.1 # Position teeth between inner and outer rim
        
        for i in range(num_teeth):
            angle_deg = (360 / num_teeth) * i
            
            glPushMatrix()
            glRotatef(angle_deg, 0, 0, 1) # Rotate around Z (up)
            glTranslatef(radius, 0, 0)    # Push out to rim
            
            # Draw a solid Cube/Block for the tooth
            # Using manual quads to avoid GLUT dependency
            w = 0.15 # half-width
            d = 0.2  # half-depth (thickness)
            h = 0.3  # height
            
            glBegin(GL_QUADS)
            # Front Face
            glNormal3f(1.0, 0.0, 0.0)
            glVertex3f(d, -w, 0.0); glVertex3f(d, w, 0.0)
            glVertex3f(d, w, h);    glVertex3f(d, -w, h)
            # Back Face
            glNormal3f(-1.0, 0.0, 0.0)
            glVertex3f(-d, -w, 0.0); glVertex3f(-d, -w, h)
            glVertex3f(-d, w, h);    glVertex3f(-d, w, 0.0)
            # Top Face
            glNormal3f(0.0, 0.0, 1.0)
            glVertex3f(-d, -w, h);   glVertex3f(d, -w, h)
            glVertex3f(d, w, h);     glVertex3f(-d, w, h)
            # Left Face
            glNormal3f(0.0, -1.0, 0.0)
            glVertex3f(-d, -w, 0.0); glVertex3f(d, -w, 0.0)
            glVertex3f(d, -w, h);    glVertex3f(-d, -w, h)
            # Right Face
            glNormal3f(0.0, 1.0, 0.0)
            glVertex3f(-d, w, 0.0);  glVertex3f(-d, w, h)
            glVertex3f(d, w, h);     glVertex3f(d, w, 0.0)
            glEnd()
            
            glPopMatrix()

        glPopMatrix()
        gluDeleteQuadric(quadric)


    elif piece_type == "knight":
        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        
        glPushMatrix()
        glRotatef(-90, 1, 0, 0) # Orient Upward
        
        glScalef(0.4, 0.4, 0.45)
        # --- 1. Base ---
        gluDisk(quadric, 0.0, 1.2, 32, 1)
        gluCylinder(quadric, 1.2, 1.1, 0.4, 32, 1)
        glTranslatef(0, 0, 0.4)
        gluDisk(quadric, 0.0, 1.1, 32, 1)
        
        # --- 2. The Neck (Flattened Sphere) ---
        # We move up and scale the sphere so it's thin on the X axis
        glPushMatrix()
        glTranslatef(0, 0, 0.8) 
        glScalef(0.4, 0.8, 1.5) # Squash X, stretch Y and Z
        gluSphere(quadric, 1.0, 32, 32)
        glPopMatrix()
        
        # --- 3. The Head (Snout) ---
        glPushMatrix()
        # Move to the top-front of the neck
        glTranslatef(0, 0.6, 1.8) 
        glRotatef(40, 1, 0, 0)  # Tilt the head down
        glScalef(0.35, 0.5, 1.0) # Flattened snout
        gluSphere(quadric, 0.8, 32, 32)
        glPopMatrix()

        # --- 4. Ears ---
        for side in [-0.2, 0.2]:
            glPushMatrix()
            glTranslatef(side, 0.3, 2.2)
            glScalef(0.1, 0.1, 0.3)
            gluSphere(quadric, 1.0, 16, 16)
            glPopMatrix()

        glPopMatrix()
        gluDeleteQuadric(quadric)


    elif piece_type == "bishop":
        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        
        glPushMatrix()
        # Orient upward along Y-axis
        glRotatef(-90, 1, 0, 0)

        glScalef(0.38, 0.36, 0.39)
        SyntaxWarning
        # --- 1. Base ---
        gluDisk(quadric, 0.0, 1.1, 32, 1)
        gluCylinder(quadric, 1.1, 1.1, 0.3, 32, 1)
        glTranslatef(0, 0, 0.3)
        gluDisk(quadric, 0.0, 1.1, 32, 1)
        
        # --- 2. Slender Stem ---
        # Tapers from the base up to a narrow neck
        gluCylinder(quadric, 0.9, 0.4, 2.2, 32, 1)
        glTranslatef(0, 0, 2.2)
        
        # --- 3. The Collar ---
        # A decorative ring before the head
        gluDisk(quadric, 0.0, 0.7, 32, 1)
        gluCylinder(quadric, 0.7, 0.7, 0.15, 32, 1)
        glTranslatef(0, 0, 0.15)
        gluDisk(quadric, 0.0, 0.7, 32, 1)
        
        # --- 4. The Miter (Head) ---
        # We use a slightly elongated sphere for the bishop's hat
        glPushMatrix()
        glTranslatef(0, 0, 0.5)
        glScalef(1.0, 1.0, 1.4) # Stretch the sphere vertically
        gluSphere(quadric, 0.5, 32, 32)
        glPopMatrix()
        
        # --- 5. The Top Pommel ---
        # Small sphere at the very tip
        glTranslatef(0, 0, 1.1)
        gluSphere(quadric, 0.12, 16, 16)
        
        glPopMatrix()
        gluDeleteQuadric(quadric)

    elif piece_type == "queen":
        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        
        glPushMatrix()
        # Orient upward along Y-axis
        glRotatef(-90, 1, 0, 0)

        glScalef(0.33, 0.33, 0.39)
        
        # --- 1. Base ---
        gluDisk(quadric, 0.0, 1.3, 32, 1)
        gluCylinder(quadric, 1.3, 1.3, 0.4, 32, 1)
        glTranslatef(0, 0, 0.4)
        gluDisk(quadric, 0.0, 1.3, 32, 1)
        
        # --- 2. Main Body (Tall Taper) ---
        # Tapers from the base up to a very slender neck
        gluCylinder(quadric, 1.1, 0.45, 3.0, 32, 1)
        glTranslatef(0, 0, 3.0)
        
        # --- 3. The Lower Collar ---
        gluDisk(quadric, 0.0, 0.7, 32, 1)
        gluCylinder(quadric, 0.7, 0.7, 0.2, 32, 1)
        glTranslatef(0, 0, 0.2)
        gluDisk(quadric, 0.0, 0.7, 32, 1)
        
        # --- 4. The Crown (Coronet) ---
        # Flared cylinder to represent the crown opening
        gluCylinder(quadric, 0.5, 0.9, 0.6, 32, 1)
        glTranslatef(0, 0, 0.6)
        # Surface inside the crown
        gluDisk(quadric, 0.0, 0.9, 32, 1)
        
        # --- 5. The Top Sphere (Monde) ---
        # Final decorative sphere on the very top
        glTranslatef(0, 0, 0.1)
        gluSphere(quadric, 0.25, 32, 32)
        
        glPopMatrix()
        gluDeleteQuadric(quadric)


    elif piece_type == "king":
        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        
        glPushMatrix()
        # Orient upward along Y-axis
        glRotatef(-90, 1, 0, 0)

        glScalef(0.33, 0.33, 0.43)
        
        # --- 1. Base ---
        gluDisk(quadric, 0.0, 1.4, 32, 1)
        gluCylinder(quadric, 1.4, 1.4, 0.4, 32, 1)
        glTranslatef(0, 0, 0.4)
        gluDisk(quadric, 0.0, 1.4, 32, 1)
        
        # --- 2. Main Body (Tall Taper) ---
        gluCylinder(quadric, 1.2, 0.5, 3.2, 32, 1)
        glTranslatef(0, 0, 3.2)
        
        # --- 3. The Decorative Collar ---
        gluDisk(quadric, 0.0, 0.8, 32, 1)
        gluCylinder(quadric, 0.8, 0.8, 0.2, 32, 1)
        glTranslatef(0, 0, 0.2)
        gluDisk(quadric, 0.0, 0.8, 32, 1)
        
        # --- 4. The King's Crown ---
        # Unlike the queen's flare, the king's crown is usually a bit more cylindrical
        gluCylinder(quadric, 0.6, 0.8, 0.7, 32, 1)
        glTranslatef(0, 0, 0.7)
        gluDisk(quadric, 0.0, 0.8, 32, 1)
        
        # --- 5. The Cross ---
        # Vertical Bar
        glPushMatrix()
        glTranslatef(0, 0, 0.3) # Move above the crown
        glScalef(0.15, 0.15, 0.6)
        gluSphere(quadric, 1.0, 16, 16)
        glPopMatrix()
        
        # Horizontal Bar
        glPushMatrix()
        glTranslatef(0, 0, 0.6) # Move to the middle of the vertical bar
        glScalef(0.4, 0.15, 0.15)
        gluSphere(quadric, 1.0, 16, 16)
        glPopMatrix()
        
        glPopMatrix()
        gluDeleteQuadric(quadric)

    glPopMatrix()

def draw_all_pieces():
    for piece in pieces:
        piece_type, x, y, color = piece
        draw_piece(piece_type, x, y, color)


# ... (keep all your existing imports and the init_pieces/draw_piece functions)

# --- ADD THESE FUNCTIONS TO THE BOTTOM OF draw_pieces.py ---

def get_piece_at(x, y):
    """Returns the piece list [type, x, y, color] if found, else None"""
    for p in pieces:
        if p[1] == x and p[2] == y:
            return p
    return None


def move_piece_location(start_x, start_y, end_x, end_y):
    """Updates the piece coordinates in the global list"""
    global pieces
    
    # 1. Find the piece we are moving
    moving_piece = get_piece_at(start_x, start_y)
    
    if moving_piece:
        # 2. Check if there is a piece at the destination (Capture logic)
        target_piece = get_piece_at(end_x, end_y)
        if target_piece:
            # Remove the captured piece from the list
            pieces.remove(target_piece)
            print(f"Captured {target_piece[0]}!")

        # 3. Update coordinates of the moving piece
        moving_piece[1] = end_x
        moving_piece[2] = end_y
        print(f"Moved {moving_piece[0]} to {end_x}, {end_y}")
        return True
    
    return False


# --- ADD TO BOTTOM OF draw_pieces.py ---

def is_path_clear(start_x, start_y, end_x, end_y):
    """Checks if the path between start and end is empty (non-inclusive of end)"""
    dx = end_x - start_x
    dy = end_y - start_y
    
    steps = max(abs(dx), abs(dy)) # Total squares to traverse
    if steps == 0: return True

    # Direction of movement (-1, 0, or 1)
    step_x = dx // steps
    step_y = dy // steps
    
    # Check every square BETWEEN start and end
    curr_x = start_x + step_x
    curr_y = start_y + step_y
    
    while (curr_x, curr_y) != (end_x, end_y):
        if get_piece_at(curr_x, curr_y):
            return False # Path is blocked
        curr_x += step_x
        curr_y += step_y
        
    return True


def is_move_valid(start_x, start_y, end_x, end_y):
    """
    Returns (True, "Reason") if valid, (False, "Reason") if invalid.
    Handles piece-specific geometry and path blocking.
    """
    piece = get_piece_at(start_x, start_y)
    if not piece: return False, "No piece found."
    
    p_type, _, _, p_color = piece
    target_piece = get_piece_at(end_x, end_y) # Is there a piece at destination?
    
    dx = end_x - start_x
    dy = end_y - start_y
    abs_dx = abs(dx)
    abs_dy = abs(dy)
    
    # --- PAWN LOGIC ---
    if p_type == 'pawn':
        # Direction: White moves UP (+y), Black moves DOWN (-y)
        direction = 1 if p_color == 'white' else -1
        
        # 1. Forward Move (Non-Capture)
        if dx == 0:
            if target_piece: 
                return False, "Pawns cannot capture forward."
            
            # Move 1 square forward
            if dy == direction:
                return True, "Step"
            
            # Move 2 squares forward (First move only)
            start_row = 1 if p_color == 'white' else 6
            if start_y == start_row and dy == 2 * direction:
                if is_path_clear(start_x, start_y, end_x, end_y):
                    return True, "Double Step"
                return False, "Path blocked."
                
        # 2. Diagonal Capture
        elif abs_dx == 1 and dy == direction:
            if target_piece: # Must be an enemy (friendlies checked in main loop)
                return True, "Capture"
            return False, "Pawns can only move diagonal to capture."
            
        return False, "Invalid Pawn move."

    # --- ROOK LOGIC ---
    if p_type == 'rook':
        # Must move straight (either dx is 0 OR dy is 0)
        if dx != 0 and dy != 0:
            return False, "Rooks move in straight lines."
        if not is_path_clear(start_x, start_y, end_x, end_y):
            return False, "Path blocked."
        return True, "Valid Rook move."

    # --- BISHOP LOGIC ---
    if p_type == 'bishop':
        # Must move diagonal (abs(dx) must equal abs(dy))
        if abs_dx != abs_dy:
            return False, "Bishops move diagonally."
        if not is_path_clear(start_x, start_y, end_x, end_y):
            return False, "Path blocked."
        return True, "Valid Bishop move."

    # --- KNIGHT LOGIC ---
    if p_type == 'knight':
        # L-Shape: 2x1 or 1x2 
        if (abs_dx == 2 and abs_dy == 1) or (abs_dx == 1 and abs_dy == 2):
            return True, "Valid Knight jump." # Knights jump, so no path check
        return False, "Knights move in an L-shape."

    # --- QUEEN LOGIC ---
    if p_type == 'queen':
        # Rook movement OR Bishop movement
        is_straight = (dx == 0 or dy == 0)
        is_diagonal = (abs_dx == abs_dy)
        
        if not (is_straight or is_diagonal):
            return False, "Queens move straight or diagonal."
        if not is_path_clear(start_x, start_y, end_x, end_y):
            return False, "Path blocked."
        return True, "Valid Queen move."

    # --- KING LOGIC ---
    if p_type == 'king':
        # Move 1 square in any direction
        if abs_dx <= 1 and abs_dy <= 1:
            return True, "Valid King step."
        return False, "Kings only move 1 step."

    return False, "Unknown piece type."
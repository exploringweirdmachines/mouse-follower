import gizeh
import numpy as np
import pygame

################################ WINDOW SETUP  #################################
WIDTH, HEIGHT = 640, 480

WINDOW = pygame.display.set_mode([WIDTH, HEIGHT], flags=pygame.RESIZABLE)

WHITE = (255, 255, 255)

WINDOW.fill(WHITE)

FPS = 60

pygame.display.set_caption("Nice Window")


################################ OBJECT SETUP #################################
class VectorWalker:
    def __init__(self):
        self.location = np.array([WIDTH / 2, HEIGHT / 2])
        self.direction = np.array([0, 0])
        self.acceleration = np.array([0.0, 0.0])

        self.circle_radius = 20

    def _check_edges(self):
        self.locx, self.locy = self.location
        self.velx, self.vely = self.direction

        if (int(self.locx + self.circle_radius) > WIDTH) or (
            (int(self.locx - self.circle_radius) < 0)
        ):
            self.velx = self.velx * -1
            self.acceleration *= -1

        if (int(self.locy + self.circle_radius) > HEIGHT) or (
            int(self.locy - self.circle_radius) < 0
        ):
            self.vely = self.vely * -1
            self.acceleration *= -1

        self.direction = self.velx, self.vely

    def _compute_vectors(self):
        self.mouse = np.array(pygame.mouse.get_pos())
        self.mouse = np.subtract(self.mouse, self.location)
        self.mouse = self.mouse / np.linalg.norm(
            self.mouse
        )  # SetMag() function from Processing is using normalize first and then multiplication to scale the unit vector(unit vector is what you get after normalization) I ditched here the sklearn Normalize
        self.mouse = np.multiply(self.mouse, 0.1)

        self.acceleration = self.mouse
        self.acceleration = np.clip(self.acceleration, a_min=-1, a_max=1)
        # print(self.mouse, type(self.mouse))
        self.direction = np.add(self.direction, self.acceleration)
        self.location = np.add(self.location, self.direction)

    def _unit_vector(self, vector):
        """Returns the unit vector of the vector."""
        return vector / np.linalg.norm(vector)

    def _angle_between(self, v1, v2):
        """Return the angle in radians between two vectors"""
        v1_u = self._unit_vector(v1)
        v2_u = self._unit_vector(v2)
        angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
        if v1_u[1] < v2_u[1]:  # if the y component is negative, we need to adjust the angle for the correct quadrant
            angle = -angle
        return angle

    def render(self):
        self._compute_vectors()
        self._check_edges()
        surface = gizeh.Surface(WIDTH, HEIGHT, bg_color=(255, 255, 255))

        # mosx, mosy = np.array(pygame.mouse.get_pos())

        # dirx, diry = self.direction

        v = 10 # for the pointing triangle

        theta = self._angle_between(self.direction, [1, 0])

        drawing = gizeh.Group(
            [
                gizeh.circle(r=self.circle_radius, xy=[self.locx, self.locy], fill=(0.5, 0.1, 0, 0.1)),
                gizeh.polyline(points=[(0, 0), (self.locx, self.locy)], stroke_width=1, stroke=(1, 0, 0)),
                gizeh.polyline(points=[(-v, v/2), (-v, -v/2), (v, 0)], xy=(self.locx, self.locy), angle=theta, stroke_width=1, stroke=(1, 0, 0), close_path=True),
                gizeh.text(f"x: {0:.2f}, y: {0:.2f}", fontfamily="Dancing Script", fontsize=10, fill=(0, 0, 0), xy=(45, 15)),
                gizeh.text(f"x: {self.locx:.2f}, y: {self.locy:.2f}", fontfamily="Dancing Script", fontsize=10, fill=(0, 0, 0), xy=(self.locx+25, self.locy+15))
            ]
        )
        drawing.draw(surface)

        return surface.get_npimage()


################################ RENDER FUNCTIONS ################################
def draw_window_no_resize(walker: VectorWalker):
    """
    Resizing the window will crash, but this function is faster.
    The mismatch between gizeh surface and pygame surface is matching, because we transpose
    """
    walk = walker.render()
    walk = np.transpose(walk, axes=(1, 0, 2))

    pygame.surfarray.blit_array(WINDOW, array=walk)
    pygame.display.update()


def draw_window_resize(walker: VectorWalker):
    """
    The mismatch between gizeh surface and pygame surface is matching, because we transpose
    """
    walk = walker.render()
    walk = np.transpose(walk, axes=(1, 0, 2))
    surf = pygame.surfarray.make_surface(walk)

    WINDOW.blit(surf, dest=(0, 0))
    pygame.display.update()


################################ MAIN RUN LOOP  ################################
def main():

    clock = pygame.time.Clock()
    run = True
    walker = VectorWalker()

    while run:
        clock.tick(FPS)
        draw_window_resize(walker)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # print(pygame.mouse.get_pos(), type(pygame.mouse.get_pos()))
    pygame.quit()


if __name__ == "__main__":
    main()

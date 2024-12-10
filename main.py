import pygame
from body import Body
from node import Node

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

pygame.init()
pygame.display.set_caption("Procedural Generation")
pygame.mouse.set_visible(False)

class WorldState:
    def __init__(self):
        self.running = True
        self.body = Body([], 25)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.mousePos = [0, 0]
        self.displayParametric = False
        self.displayCircles = True
        self.displayConnections = False
        self.displayLateralPoints = False
    
    def handleKeyBoardInput(self):
        for event in pygame.event.get():
            # Handle quitting
            if event.type == pygame.QUIT:
                self.running = False
            # Handle keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    self.displayParametric = not self.displayParametric
                elif event.key == pygame.K_1:
                    self.displayCircles = not self.displayCircles
                elif event.key == pygame.K_4:
                    self.displayConnections = not self.displayConnections
                elif event.key == pygame.K_2:
                    self.displayLateralPoints = not self.displayLateralPoints
                elif event.key == pygame.K_SPACE:
                    self.body.switchColor()

    def drawMouse(self):
        pygame.draw.circle(self.screen, pygame.color.Color(255, 255, 255), (self.mousePos[0], self.mousePos[1]), 5)

    def draw(self):
        # Reset screen
        self.screen.fill(pygame.color.Color(50, 50, 60))

        # Display mouse
        self.drawMouse()

        if self.displayCircles:
            # Display Nodes in Body
            self.body.displayNodes(self.screen)

        if self.displayLateralPoints:
            # Display lateral points
            self.body.displayLateralPoints(self.screen)

        if self.displayConnections:
            # Display body connections
            self.body.displayLinesBetweenNodes(self.screen)

        if self.displayParametric:
            # Display parametric curve
            self.body.display(self.screen)
    
    def update(self):
        # Update mouse position
        self.mousePos = pygame.mouse.get_pos()

        # Move head of body towards mouse
        if pygame.mouse.get_pressed()[0]:
            self.body.update(True)
        else:
            self.body.update(False)

        self.handleKeyBoardInput()
    
def main():
    ws = WorldState()
    runGame(ws)
        

def runGame(ws: WorldState):
    # Set body to example
    ws.body.setExampleBody()

    while ws.running:

        ws.draw()
        ws.update()

        # Update screen
        pygame.display.flip()
        ws.clock.tick(60)
    
    # Quit pygame when not runnning
    pygame.quit()





if __name__ == "__main__":
    main()

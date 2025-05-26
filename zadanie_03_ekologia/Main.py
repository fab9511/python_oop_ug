import pygame
from World import World
from Position import Position
from Organisms.Grass import Grass
from Organisms.Sheep import Sheep
from Organisms.Lynx import Lynx
from Organisms.Antelope import Antelope

import os

class Simulation:
    WIDTH, HEIGHT = 1000, 600
    BOARD_SIZE = 600
    INFO_PANEL_WIDTH = WIDTH - BOARD_SIZE
    ROWS, COLS = 10, 10
    CELL_SIZE = BOARD_SIZE // COLS

    COLOR_MAP = {
        'Grass': (34, 139, 34),
        'Sheep': (255, 255, 255),
        'Lynx': (255, 69, 0),
        'Antelope': (210, 180, 140)
    }

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Symulacja Ekologii")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

        self.pyWorld = World(self.COLS, self.ROWS)
        self.pyWorld.addOrganism(Grass(position=Position(xPosition=9, yPosition=9), world=self.pyWorld))
        self.pyWorld.addOrganism(Grass(position=Position(xPosition=1, yPosition=1), world=self.pyWorld))
        self.pyWorld.addOrganism(Sheep(position=Position(xPosition=2, yPosition=2), world=self.pyWorld))
        self.pyWorld.addOrganism(Lynx(position=Position(xPosition=6, yPosition=6), world=self.pyWorld))
        self.pyWorld.addOrganism(Antelope(position=Position(xPosition=5, yPosition=5), world=self.pyWorld))

        self.running = True
        self.adding_mode = False
        self.organism_to_add = None

    def draw_grid(self):
        for x in range(0, self.BOARD_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, (200, 200, 200), (x, 0), (x, self.BOARD_SIZE))
        for y in range(0, self.BOARD_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, (200, 200, 200), (0, y), (self.BOARD_SIZE, y))

    def draw_cols(self):
        for col in range(1, self.COLS+1):
            x = col * self.CELL_SIZE + self.CELL_SIZE // 2
            text = self.font.render(str(col), True, (255, 255, 255))
            text_rect = text.get_rect(center=(x, self.CELL_SIZE // 2))
            self.screen.blit(text, text_rect)

    def draw_rows(self):
        for row in range(1, self.ROWS+1):
            y = row * self.CELL_SIZE + self.CELL_SIZE // 2
            text = self.font.render(str(row), True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.CELL_SIZE // 2, y))
            self.screen.blit(text, text_rect)

    def draw_coordinates(self):
        self.draw_cols()
        self.draw_rows()

    def draw_world(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        self.draw_coordinates()
        for org in self.pyWorld.organisms:
            x = org.position.x * self.CELL_SIZE
            y = org.position.y * self.CELL_SIZE
            c = self.COLOR_MAP.get(org.__class__.__name__, (128, 128, 128))
            pygame.draw.rect(self.screen, c, (x, y, self.CELL_SIZE, self.CELL_SIZE))

    def draw_info_panel(self):
        panel_x = self.BOARD_SIZE
        panel_y = 0
        pygame.draw.rect(self.screen, (40, 40, 40), (panel_x, panel_y, self.INFO_PANEL_WIDTH, self.HEIGHT))


        lines = [
            "Dostępne klawisze:",
            "Enter - kolejna tura",
            "P - włącz plagę",
            "A - dodaj organizm",
            "Q - wyjście",
        ]

        if self.pyWorld.plagueActive:
            lines.append("")
            lines.append(" PLAGA!! Plaga aktywna")
            lines.append(f"Pozostało: {self.pyWorld.plagueTurnsLeft} tur")
        if self.adding_mode:
            if self.organism_to_add is None:
                lines.append("")
                lines.append("Tryb dodawania (wciśnij klawisz):")
                lines.append("1. Trawa")
                lines.append("2. Owca")
                lines.append("3. Ryś")
                lines.append("4. Antylopa")
                lines.append("ESC Zamknij tryb")
            else:
                lines.append(f"Dodajesz: {self.organism_to_add} (kliknij na planszę)")

        y_offset = 10
        for line in lines:
            text_surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surf, (panel_x + 10, y_offset))
            y_offset += 30

    def handle_keydown(self, event):
        if event.key == pygame.K_RETURN:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.pyWorld.makeTurn()
        elif event.key == pygame.K_p:
            self.pyWorld.plagueActive = True
            print("Plaga została aktywowana.")
        elif event.key == pygame.K_q:
            self.running = False
        elif event.key == pygame.K_a and not self.adding_mode:
            self.adding_mode = True
            self.organism_to_add = None
        elif self.adding_mode and self.organism_to_add is None:
            if event.key == pygame.K_1:
                self.organism_to_add = "Grass"
                print("Wybrano: Grass")
            elif event.key == pygame.K_2:
                self.organism_to_add = "Sheep"
                print("Wybrano: Sheep")
            elif event.key == pygame.K_3:
                self.organism_to_add = "Lynx"
                print("Wybrano: Lynx")
            elif event.key == pygame.K_4:
                self.organism_to_add = "Antelope"
                print("Wybrano: Antelope")
            elif event.key == pygame.K_ESCAPE:
                self.adding_mode = False
                print("Anulowano dodawanie.")
        else:
            print(f"Nieznany klawisz: {event.key}")

    def handle_mouse_button_down(self, event):
        mouse_x, mouse_y = event.pos
        grid_x = mouse_x // self.CELL_SIZE
        grid_y = mouse_y // self.CELL_SIZE

        if grid_x < self.COLS and grid_y < self.ROWS:
            pos = Position(xPosition=grid_x, yPosition=grid_y)
            if self.pyWorld.isPositionFree(pos):
                if self.organism_to_add == 'Grass':
                    new_org = Grass(position=pos, world=self.pyWorld)
                elif self.organism_to_add == 'Sheep':
                    new_org = Sheep(position=pos, world=self.pyWorld)
                elif self.organism_to_add == 'Lynx':
                    new_org = Lynx(position=pos, world=self.pyWorld)
                elif self.organism_to_add == 'Antelope':
                    new_org = Antelope(position=pos, world=self.pyWorld)

                self.pyWorld.addOrganism(new_org)
                print(f"Dodano {self.organism_to_add} na pozycję ({grid_x}, {grid_y})")
            else:
                print("To pole jest już zajęte.")
        else:
            print("Kliknięto poza planszą.")

        self.adding_mode = False
        self.organism_to_add = None

    def run(self):
        while self.running:
            self.clock.tick(10)  # 10 fps
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)
                elif event.type == pygame.MOUSEBUTTONDOWN and self.adding_mode and self.organism_to_add:
                    self.handle_mouse_button_down(event)

            self.draw_world()
            self.draw_info_panel()
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    sim = Simulation()
    sim.run()



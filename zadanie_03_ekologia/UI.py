import pygame
from World import World
from Position import Position
from Organisms.Grass import Grass
from Organisms.Sheep import Sheep
from Organisms.Lynx import Lynx
from Organisms.Antelope import Antelope


class Simulation:
    WIDTH, HEIGHT = 920, 750
    BOARD_SIZE = 600
    INFO_PANEL_WIDTH = WIDTH - BOARD_SIZE
    ROWS, COLS = 10, 10
    CELL_SIZE = BOARD_SIZE // COLS
    LOG_PANEL_HEIGHT = 150

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
        self.initialize_organisms()

        self.running = True
        self.adding_mode = False
        self.organism_to_add = None

        self.log_scroll = 0
        self.max_visible_logs = 6
        self.images = self.load_images()

    def initialize_organisms(self):
        self.pyWorld.addOrganism(Grass(position=Position(xPosition=9, yPosition=9), world=self.pyWorld))
        self.pyWorld.addOrganism(Grass(position=Position(xPosition=1, yPosition=1), world=self.pyWorld))
        self.pyWorld.addOrganism(Sheep(position=Position(xPosition=2, yPosition=2), world=self.pyWorld))
        self.pyWorld.addOrganism(Lynx(position=Position(xPosition=6, yPosition=6), world=self.pyWorld))
        self.pyWorld.addOrganism(Antelope(position=Position(xPosition=5, yPosition=5), world=self.pyWorld))


    def load_images(self):
        return {
            "Antelope": pygame.image.load("images/antelope.png").convert_alpha(),
            "Sheep": pygame.image.load("images/sheep.png").convert_alpha(),
            "Lynx": pygame.image.load("images/lynx.png").convert_alpha(),
            "Grass": pygame.image.load("images/grass.png").convert_alpha(),
        }

    def draw_grid(self):
        for x in range(0, self.BOARD_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, (200, 200, 200), (x, 0), (x, self.BOARD_SIZE))
        for y in range(0, self.BOARD_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, (200, 200, 200), (0, y), (self.BOARD_SIZE, y))

    def draw_world(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        for org in self.pyWorld.organisms:
            x = org.position.x * self.CELL_SIZE
            y = org.position.y * self.CELL_SIZE
            c = self.COLOR_MAP.get(org.__class__.__name__, (128, 128, 128))
            pygame.draw.rect(self.screen, c, (x+5, y+5, self.CELL_SIZE-10, self.CELL_SIZE-10))

            image = self.images.get(org.__class__.__name__, None)
            if image:
                self.screen.blit(image, (x+self.CELL_SIZE//4, y+self.CELL_SIZE//4, self.CELL_SIZE, self.CELL_SIZE))

    def draw_info_panel(self):
        self.draw_info_panel_background()
        lines = self.get_base_info_lines()
        lines += self.get_plague_info_lines()
        lines += self.get_adding_mode_lines()
        self.draw_text_lines(lines)

    def draw_info_panel_background(self):
        panel_x = self.BOARD_SIZE
        panel_y = 0
        pygame.draw.rect(self.screen, (40, 40, 40), (panel_x, panel_y, self.INFO_PANEL_WIDTH, self.HEIGHT))

    def get_base_info_lines(self):
        return [
            f"Numer tury: {str(self.pyWorld.numberTurns)}",
            "Dostępne klawisze:",
            "Enter - kolejna tura",
            "P - włącz plagę",
            "A - dodaj organizm",
            "Q - wyjście"
        ]

    def get_plague_info_lines(self):
        lines = []
        if self.pyWorld.plagueActive:
            lines.append("")
            lines.append(" PLAGA!! Plaga aktywna")
            lines.append(f"Pozostało: {self.pyWorld.plagueTurnsLeft} tur")
        return lines

    def get_adding_mode_lines(self):
        lines = []
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
                lines.append("")
                organism_names = {"Grass": "Trawa", "Sheep": "Owca", "Lynx": "Ryś", "Antelope": "Antylopa"}
                lines.append(f"Dodajesz: {organism_names.get(self.organism_to_add, 'Nieznany')} (kliknij na planszę)")
        return lines

    def draw_text_lines(self, lines):
        panel_x = self.BOARD_SIZE
        y_offset = 10
        for line in lines:
            text_surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surf, (panel_x + 10, y_offset))
            y_offset += 30

    def draw_logs_panel(self):
        self.draw_logs_background()
        visible_logs = self.get_visible_logs()
        self.draw_logs_header()
        self.draw_logs_text(visible_logs)
        self.draw_scrollbar_if_needed()

    def draw_logs_background(self):
        log_start_y = self.BOARD_SIZE
        log_height = self.HEIGHT - self.BOARD_SIZE
        pygame.draw.rect(self.screen, (30, 30, 30), (0, log_start_y, self.BOARD_SIZE, log_height))

    def get_visible_logs(self):
        total_logs = len(self.pyWorld.logs)
        start = max(0, total_logs - self.max_visible_logs - self.log_scroll)
        end = max(0, total_logs - self.log_scroll)
        return self.pyWorld.logs[start:end]

    def draw_logs_header(self):
        log_start_y = self.BOARD_SIZE
        y_offset = 10
        header_text = "=> => => => => Logi danej tury => => => => =>  (przewijanie - strzałki)"
        header = self.font.render(header_text, True, (255, 255, 255))
        self.screen.blit(header, (10, log_start_y + y_offset))

    def draw_logs_text(self, logs):
        log_start_y = self.BOARD_SIZE
        y_offset = 10
        for i, log in enumerate(logs):
            color_value = 255 - (i % 2) * 100 ##naprzemienne kolory
            text = self.font.render(str(log), True, (255, 255, color_value))
            self.screen.blit(text, (10, log_start_y + y_offset + (i + 1) * 20))

    def draw_scrollbar_if_needed(self):
        if len(self.pyWorld.logs) > self.max_visible_logs:
            self.draw_scrollbar()

    def draw_scrollbar(self):
        log_start_y = self.BOARD_SIZE
        total_logs = len(self.pyWorld.logs)
        log_height = self.HEIGHT - self.BOARD_SIZE

        scrollbar_width = 8
        scrollbar_x = self.BOARD_SIZE - scrollbar_width - 2
        track_height = log_height - 20
        track_y = log_start_y + 10

        thumb_height = max(20, int(self.max_visible_logs / total_logs * track_height))
        scroll_ratio = self.log_scroll / max(1, total_logs - self.max_visible_logs)
        thumb_y = track_y + (track_height - thumb_height) * scroll_ratio

        pygame.draw.rect(self.screen, (70, 70, 70), (scrollbar_x, track_y, scrollbar_width, track_height))
        pygame.draw.rect(self.screen, (200, 200, 200), (scrollbar_x, thumb_y, scrollbar_width, thumb_height))

    def handle_keydown(self, event):
        if event.key == pygame.K_RETURN:
            self.adding_mode = False #żeby znikło jak mamy next tur
            self.pyWorld.makeTurn()
        elif event.key == pygame.K_p:
            self.pyWorld.plagueActive = True
            self.adding_mode = False
        elif event.key == pygame.K_q:
            self.running = False
        elif event.key == pygame.K_a and not self.adding_mode:
            self.adding_mode = True
            self.organism_to_add = None
        elif self.adding_mode and self.organism_to_add is None:
            self.addAnimal(event.key)
        else:
            print(f"Nieznany klawisz: {event.key}")

    def addAnimal(self, key):
        if key == pygame.K_1:
            self.organism_to_add = "Grass"
        elif key == pygame.K_2:
            self.organism_to_add = "Sheep"
        elif key == pygame.K_3:
            self.organism_to_add = "Lynx"
        elif key == pygame.K_4:
            self.organism_to_add = "Antelope"
        elif key == pygame.K_ESCAPE:
            self.adding_mode = False

    def handle_mouse_button_down(self, event):
        mouse_x, mouse_y = event.pos
        grid_x = mouse_x // self.CELL_SIZE
        grid_y = mouse_y // self.CELL_SIZE
        new_org = None
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
                self.pyWorld.log(f"Dodano {self.organism_to_add} na pozycję ({grid_x}, {grid_y})")
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
                    if event.key == pygame.K_DOWN:
                        if self.log_scroll < max(0, len(self.pyWorld.logs) - self.max_visible_logs):
                            self.log_scroll += 1
                    elif event.key == pygame.K_UP:
                        if self.log_scroll > 0:
                            self.log_scroll -= 1
                    else:
                        self.handle_keydown(event)
                elif event.type == pygame.MOUSEBUTTONDOWN and self.adding_mode and self.organism_to_add:
                    self.handle_mouse_button_down(event)

            self.draw_world()
            self.draw_info_panel()
            self.draw_logs_panel()
            pygame.display.flip()

        pygame.quit()
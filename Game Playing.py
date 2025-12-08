# %%

import pygame
import sys

pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EthicaBot - Moral Lessons Edition")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
LIGHT_BLUE = (100, 150, 255)
DARK_BLUE = (60, 110, 210)
GREEN = (80, 200, 120)
RED = (220, 80, 80)
GRAY = (230, 230, 230)
PANEL = (245, 245, 250)

# --- Fonts ---
title_font = pygame.font.SysFont("arial", 48, bold=True)
text_font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 22)
lesson_font = pygame.font.SysFont("arial", 24, italic=True)

# --- Scenarios (each has a question, options, and a moral lesson) ---
scenarios = [
    {
        "question": "You are designing an AI for hiring. Should you ignore demographic features entirely?",
        "options": ["Remove demographic data and proceed", "Audit and mitigate bias in data"],
        "lesson": "Moral: AI must actively detect and mitigate bias. Blind removal doesn't guarantee fairness—inspect datasets and correct unfair patterns."
    },
    {
        "question": "An AI assistant can record voice for training without telling users. Should it record?",
        "options": ["Record silently for better training", "Ask for informed consent before recording"],
        "lesson": "Moral: Respect user privacy. Always obtain informed consent before collecting or storing personal data."
    },
    {
        "question": "A self-driving car must choose between risking passengers or pedestrians. How to decide?",
        "options": ["Always prioritize passenger safety", "Design policies balancing fairness and safety"],
        "lesson": "Moral: Ethical AI balances harms and benefits; decisions should be guided by clear policy, fairness, and legal/ethical standards."
    },
    {
        "question": "An AI uses personal data for targeted ads to raise revenue. Should it do so without notifying users?",
        "options": ["Use the data for ads without notice", "Disclose and let users opt in/out"],
        "lesson": "Moral: Transparency and user control are essential. Disclosing data use and offering choices preserves trust."
    },
    {
        "question": "Deploy facial recognition widely for convenience. Is this acceptable without oversight?",
        "options": ["Yes — convenience outweighs concerns", "Only with strict rules and oversight"],
        "lesson": "Moral: Surveillance tech must be responsibly governed. Restrict use, audit systems, and protect civil liberties."
    },
    {
        "question": "AI produces content that looks like a human wrote it. Should you label it?",
        "options": ["No label to avoid friction", "Label content clearly as AI-generated"],
        "lesson": "Moral: Label AI-generated content to promote transparency and reduce misinformation and confusion."
    }
]

# --- Button class ---
class Button:
    def __init__(self, text, x, y, w, h, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.hover_color = hover_color

    def draw(self, surface, mouse_pos):
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=12)
        txt = text_font.render(self.text, True, BLACK)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# --- UI state ---
index = 0
lesson_display = ""      # Stores moral text after a click
show_lesson = False
learned_lessons = []     # Accumulate lessons for final summary

# Pre-create next button and option buttons placeholder
next_button = Button("Next", WIDTH - 200, HEIGHT - 90, 160, 55, DARK_BLUE, LIGHT_BLUE)

def make_option_buttons(option_texts):
    buttons = []
    start_y = 280
    gap = 110
    btn_w = 860
    btn_h = 80
    x = (WIDTH - btn_w) // 2
    for i, t in enumerate(option_texts):
        btn = Button(t, x, start_y + i * gap, btn_w, btn_h, GRAY, PANEL)
        buttons.append(btn)
    return buttons

option_buttons = make_option_buttons(scenarios[index]["options"])

clock = pygame.time.Clock()

# --- Main loop ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    screen.fill(WHITE)

    # Top panel
    pygame.draw.rect(screen, PANEL, (40, 30, WIDTH - 80, 120), border_radius=14)
    title = title_font.render("EthicaBot — Moral Lessons on AI Ethics", True, BLACK)
    screen.blit(title, (70, 50))
    subtitle = small_font.render("Make decisions and learn an ethical principle after each choice.", True, BLACK)
    screen.blit(subtitle, (70, 110))

    # Scenario panel
    pygame.draw.rect(screen, (250, 250, 255), (60, 170, WIDTH - 120, 370), border_radius=14)
    question = text_font.render(f"Scenario {index + 1}: {scenarios[index]['question']}", True, BLACK)
    screen.blit(question, (90, 200))

    # Draw option buttons
    if not show_lesson:
        for btn in option_buttons:
            btn.draw(screen, mouse_pos)
    else:
        # Show moral lesson panel
        pygame.draw.rect(screen, (245, 245, 245), (100, 320, WIDTH - 200, 180), border_radius=12)
        lesson_lines = []
        # split long lesson into lines roughly
        text = lesson_display
        # simple wrap
        words = text.split()
        line = ""
        for w in words:
            if len(line + " " + w) > 80:
                lesson_lines.append(line)
                line = w
            else:
                line = (line + " " + w).strip()
        if line:
            lesson_lines.append(line)
        # render lines
        y = 340
        for ln in lesson_lines:
            screen.blit(lesson_font.render(ln, True, BLACK), (120, y))
            y += 32

        # Next button to proceed
        next_button.draw(screen, mouse_pos)

    # Footer: summary of learned lessons count
    footer_text = small_font.render(f"Lessons learned: {len(learned_lessons)}/{len(scenarios)}", True, BLACK)
    screen.blit(footer_text, (70, HEIGHT - 60))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not show_lesson:
                # Check option buttons clicked
                for i, btn in enumerate(option_buttons):
                    if btn.is_clicked(mouse_pos):
                        # When a choice is made, always show the moral lesson for that scenario
                        lesson_display = scenarios[index]["lesson"]
                        show_lesson = True
                        # Add to learned lessons list (avoid duplicates)
                        if lesson_display not in learned_lessons:
                            learned_lessons.append(lesson_display)
                        break
            else:
                # Next pressed? advance to next scenario or show final summary
                if next_button.is_clicked(mouse_pos):
                    index += 1
                    if index >= len(scenarios):
                        # Show final summary screen
                        screen.fill(WHITE)
                        title_end = title_font.render("Summary of Moral Lessons", True, BLACK)
                        screen.blit(title_end, (WIDTH // 2 - title_end.get_width() // 2, 60))
                        # List all lessons
                        y = 160
                        for i, lesson in enumerate(learned_lessons, start=1):
                            # wrap each lesson
                            wrapped = []
                            words = lesson.split()
                            line = ""
                            for w in words:
                                if len(line + " " + w) > 80:
                                    wrapped.append(line)
                                    line = w
                                else:
                                    line = (line + " " + w).strip()
                            if line:
                                wrapped.append(line)
                            # render heading + wrapped lines
                            heading = text_font.render(f"{i}.", True, BLACK)
                            screen.blit(heading, (90, y))
                            ly = y
                            for ln in wrapped:
                                screen.blit(lesson_font.render(ln, True, BLACK), (130, ly))
                                ly += 28
                            y = ly + 14
                            if y > HEIGHT - 120:
                                break
                        pygame.display.flip()
                        # delay then exit
                        pygame.time.delay(7000)
                        running = False
                    else:
                        # load next scenario
                        option_buttons = make_option_buttons(scenarios[index]["options"])
                        show_lesson = False
                        lesson_display = ""

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()


# %%




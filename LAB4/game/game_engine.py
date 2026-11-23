import pygame
import time
from game.deck import Deck

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.deck = Deck()

        self.current_card = self.deck.draw()
        self.next_card = None
        self.previous_card = None
        self.score = 0
        self.status_msg = "Will the next card be HIGHER or LOWER?"
        self.status_color = (220, 220, 220)

        # Task 2: Streak tracking
        self.streak = 0
        self.multiplier = 1

        # Task 3 & 4: Tie handling and animation
        self.showing_comparison = False
        self.comparison_start_time = 0
        self.comparison_duration = 1.0  # seconds to show both cards

        btn_w, btn_h = 140, 48
        self.btn_higher = pygame.Rect(width // 2 - btn_w - 20, height - 90, btn_w, btn_h)
        self.btn_lower = pygame.Rect(width // 2 + 20, height - 90, btn_w, btn_h)

        self.font_title = pygame.font.SysFont(None, 40)
        self.font_medium = pygame.font.SysFont(None, 30)
        self.font_small = pygame.font.SysFont(None, 24)
        self.font_streak = pygame.font.SysFont(None, 28)

    def evaluate_guess(self, guess):
        """Draws next card and evaluates prediction."""
        self.previous_card = self.current_card
        self.next_card = self.deck.draw()

        # Task 1: Fix bug - use numeric_rank for comparison
        current_rank = self.current_card.numeric_rank
        next_rank = self.next_card.numeric_rank

        if next_rank == current_rank:
            # Task 3: Tie handling - PUSH, no score change, streak preserved
            self.status_msg = f"PUSH! Both {self.next_card.rank_str} - Score & Streak preserved"
            self.status_color = (255, 200, 50)  # Yellow/gold for tie
            self.showing_comparison = True
            self.comparison_start_time = time.time()
            return

        if guess == "HIGHER":
            correct = next_rank > current_rank
        else:
            correct = next_rank < current_rank

        if correct:
            # Task 2: Streak multiplier
            self.streak += 1
            if self.streak >= 2:
                self.multiplier = min(self.streak, 5)  # Cap at 5x
            else:
                self.multiplier = 1
            points = 1 * self.multiplier
            self.score += points
            if self.streak >= 2:
                self.status_msg = f"CORRECT! {self.next_card.rank_str} vs {self.current_card.rank_str} | Streak: {self.streak}x (+{points})"
            else:
                self.status_msg = f"CORRECT! {self.next_card.rank_str} vs {self.current_card.rank_str} (+1)"
            self.status_color = (80, 220, 80)
        else:
            # Wrong guess - reset streak and multiplier
            self.streak = 0
            self.multiplier = 1
            self.score = max(0, self.score - 1)
            self.status_msg = f"WRONG! {self.next_card.rank_str} vs {self.current_card.rank_str} (-1)"
            self.status_color = (235, 75, 75)

        self.showing_comparison = True
        self.comparison_start_time = time.time()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Ignore clicks during comparison animation
            if self.showing_comparison:
                return
            if self.btn_higher.collidepoint(event.pos):
                self.evaluate_guess("HIGHER")
            elif self.btn_lower.collidepoint(event.pos):
                self.evaluate_guess("LOWER")

    def update(self):
        # Task 4: Handle comparison animation timing
        if self.showing_comparison:
            elapsed = time.time() - self.comparison_start_time
            if elapsed >= self.comparison_duration:
                self.showing_comparison = False
                self.current_card = self.next_card
                self.previous_card = None
                self.next_card = None

    def render(self, screen):
        screen.fill((25, 80, 45))

        title_surf = self.font_title.render("High-Low Card Predictor", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 25))

        # Score with streak indicator
        score_text = f"Score: {self.score}"
        if self.streak >= 2:
            score_text += f"  |  Streak: {self.streak}x"
        score_surf = self.font_medium.render(score_text, True, (255, 220, 80))
        screen.blit(score_surf, (30, 30))

        rem_surf = self.font_small.render(f"Deck: {self.deck.remaining} left", True, (210, 210, 210))
        screen.blit(rem_surf, (self.width - rem_surf.get_width() - 30, 35))

        card_w, card_h = 130, 180

        if self.showing_comparison and self.previous_card and self.next_card:
            # Task 4: Side-by-side card reveal
            gap = 40
            total_width = 2 * card_w + gap
            start_x = (self.width - total_width) // 2
            y_pos = 100

            # Previous card (left)
            self.previous_card.render(screen, start_x, y_pos, card_w, card_h)
            # Arrow or "vs" between
            vs_surf = self.font_medium.render("vs", True, (255, 255, 255))
            screen.blit(vs_surf, (start_x + card_w + gap // 2 - vs_surf.get_width() // 2, y_pos + card_h // 2 - vs_surf.get_height() // 2))
            # Next card (right)
            self.next_card.render(screen, start_x + card_w + gap, y_pos, card_w, card_h)
        else:
            # Normal single card display
            self.current_card.render(screen, self.width // 2 - card_w // 2, 100, card_w, card_h)

        status_surf = self.font_small.render(self.status_msg, True, self.status_color)
        screen.blit(status_surf, (self.width // 2 - status_surf.get_width() // 2, 310))

        # Draw buttons (disabled during comparison)
        if self.showing_comparison:
            btn_color_higher = (80, 80, 80)
            btn_color_lower = (80, 80, 80)
            border_color = (100, 100, 100)
        else:
            btn_color_higher = (40, 140, 60)
            btn_color_lower = (170, 50, 50)
            border_color = (220, 220, 220)

        pygame.draw.rect(screen, btn_color_higher, self.btn_higher, border_radius=8)
        pygame.draw.rect(screen, border_color, self.btn_higher, width=2, border_radius=8)
        high_surf = self.font_medium.render("HIGHER", True, (255, 255, 255))
        screen.blit(
            high_surf,
            (self.btn_higher.centerx - high_surf.get_width() // 2, self.btn_higher.centery - high_surf.get_height() // 2),
        )

        pygame.draw.rect(screen, btn_color_lower, self.btn_lower, border_radius=8)
        pygame.draw.rect(screen, border_color, self.btn_lower, width=2, border_radius=8)
        low_surf = self.font_medium.render("LOWER", True, (255, 255, 255))
        screen.blit(
            low_surf,
            (self.btn_lower.centerx - low_surf.get_width() // 2, self.btn_lower.centery - low_surf.get_height() // 2),
        )
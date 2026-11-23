# Lab 4 - Vibe Coding: Chat History

**Student:** Arya  
**SRN:** PES2UG24CS429  
**Lab:** 4 - Vibe Coding  
**Date:** 2026-11-23  
**Assigned Repo:** https://github.com/SETAPESU26/55_card_predictor

---

## Task 1: Fix the card rank comparison bug

### Prompt 1:
> The game has a bug where face cards and tens behave inconsistently during higher/lower evaluations. The code compares `rank_str` lexicographically (e.g., "J" > "10" is False alphabetically but J=11 > 10 numerically). Please fix the comparison in `evaluate_guess` to use `numeric_rank` instead of `rank_str`.

### Response:
The bug was in `game_engine.py` line 29 and 31 where it compared `self.next_card.rank_str > self.current_card.rank_str` using string comparison. This causes issues because:
- "J" (Jack) < "10" lexicographically, but J=11 > 10 numerically
- "Q" < "J" alphabetically but Q=12 > 11
- "K" < "Q" alphabetically but K=13 > 12
- "A" < "2" alphabetically but A=14 > 2

Fixed by comparing `numeric_rank` instead:
```python
current_rank = self.current_card.numeric_rank
next_rank = self.next_card.numeric_rank
if guess == "HIGHER":
    correct = next_rank > current_rank
else:
    correct = next_rank < current_rank
```

---

## Task 2: Implement Consecutive Win Streak Multipliers

### Prompt 2:
> Add a streak tracker that rewards consecutive correct guesses with escalating score multipliers. The streak should reset on an incorrect pick. Suggested: 1x for first correct, 2x for 2 in a row, 3x for 3 in a row, etc., capped at 5x.

### Response:
Added streak tracking variables in `__init__`:
```python
self.streak = 0
self.multiplier = 1
```

Updated `evaluate_guess`:
```python
if correct:
    self.streak += 1
    if self.streak >= 2:
        self.multiplier = min(self.streak, 5)  # Cap at 5x
    else:
        self.multiplier = 1
    points = 1 * self.multiplier
    self.score += points
else:
    # Wrong guess - reset streak and multiplier
    self.streak = 0
    self.multiplier = 1
    self.score = max(0, self.score - 1)
```

Also updated the score display to show the streak multiplier.

---

## Task 3: Implement Tie Evaluation Rules

### Prompt 3:
> Drawing a card of identical rank to the current one is currently penalized as a flat loss. Add tie-handling logic that preserves the player's current score and active streak, presenting a neutral "PUSH" notification instead of docking points.

### Response:
Added tie detection at the start of `evaluate_guess`:
```python
if next_rank == current_rank:
    # Task 3: Tie handling - PUSH, no score change, streak preserved
    self.status_msg = f"PUSH! Both {self.next_card.rank_str} - Score & Streak preserved"
    self.status_color = (255, 200, 50)  # Yellow/gold for tie
    self.showing_comparison = True
    self.comparison_start_time = time.time()
    return
```

This preserves both score and streak on ties, and shows a "PUSH" message in yellow.

---

## Task 4: Implement side-by-side card reveal animation

### Prompt 4:
> The active card currently snaps immediately to the newly drawn card, making rapid comparisons hard to follow visually. Enhance the layout to show the previous and new cards side-by-side with a brief reveal pause before advancing to the next guess.

### Response:
Added animation state tracking:
```python
self.showing_comparison = False
self.comparison_start_time = 0
self.comparison_duration = 1.0  # seconds to show both cards
```

Modified `handle_event` to ignore clicks during animation:
```python
if self.showing_comparison:
    return
```

Added `update()` method to handle animation timing:
```python
def update(self):
    if self.showing_comparison:
        elapsed = time.time() - self.comparison_start_time
        if elapsed >= self.comparison_duration:
            self.showing_comparison = False
            self.current_card = self.next_card
            self.previous_card = None
            self.next_card = None
```

Updated `render()` to show side-by-side cards during comparison:
```python
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
```

Also disabled buttons during the comparison animation by graying them out.

---

## Summary of Changes

### Files Modified:
1. **game/game_engine.py** - Complete rewrite with all 4 tasks implemented

### Bug Fixed:
- Card comparison now uses `numeric_rank` (2-14) instead of lexicographic `rank_str`

### Features Added:
1. **Streak Multipliers**: Consecutive wins give 2x, 3x, 4x, 5x score multipliers (capped at 5x)
2. **Tie Handling (PUSH)**: Identical ranks preserve score and streak, show yellow "PUSH" message
3. **Side-by-side Animation**: Shows previous and new cards side-by-side with "vs" label for 1 second

---

## Video Descriptions (Per Deliverables)

### Before Video (10 seconds):
- Shows the buggy behavior: clicking HIGHER on a 10, then getting a Jack
- Bug: Game says "WRONG! J vs 10" because "J" < "10" lexicographically
- Score decreases incorrectly
- No streak tracking, no tie handling, instant card swap

### After Video (10 seconds):
- Shows correct comparison: 10 vs J correctly evaluates as HIGHER (11 > 10)
- Streak counter visible: "Score: 3 | Streak: 3x"
- Tie scenario: Both cards are 7, shows "PUSH! Both 7 - Score & Streak preserved" in yellow
- Animation: Previous card (left) and new card (right) shown side-by-side with "vs" for 1 second
- Buttons disabled during animation, re-enabled after
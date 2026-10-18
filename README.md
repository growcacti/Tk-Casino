# TkCasino
A set of casino games made in Python with Tkinter 
#User Guide

A desktop collection of seven casino games using fictional chips: **Slots, Blackjack, Roulette, Dice, Coin Flip, Hi-Lo, and Video Poker**. All games share one balance. The supplied artwork gives the games illustrated cards, slot symbols, dice, betting chips, and a roulette wheel. Drawn graphics remain available when images cannot be loaded.


Double-clicking the Python file may also work if `.py` files are associated with Python. Running from a terminal makes error messages easier to see.

## Understanding the screen

| Control or display | What it does |
| --- | --- |
| Game buttons across the top | Switch between the seven games when the current round is finished. |
| CHIPS | Available balance. A bet is deducted while the round is in progress. |
| BET entry | Type a positive amount, at least 0.01 and no more than your available balance. Use a decimal point and no currency symbol or commas. |
| Chip buttons: 5, 25, 50, 100 | Set the bet to that amount; they do not add chips to the balance. |
| Buttons below the bet | Show the actions available for the selected game or current hand. |
| Result message | Shows what happened and the round's net gain or loss. |
| Rules / Help | Opens rules for the selected game. |
| New Session | Asks before resetting to 1,000 chips and clearing session totals and recent results. An unfinished hand is discarded. |
| Asset Folder… | Selects the image folder and remembers its location on this PC. |
| Rounds / Wins / Session | Completed rounds, rounds with a positive profit, and the balance difference from the starting 1,000 chips. During play, Session also reflects the reserved bet. |
| Recent results | Shows the last three completed rounds. |
| Image status at the bottom | Shows the number of images loaded and the selected folder. |

Betting controls and game switching are disabled during a round. Finish the current hand or wait for the animation. **New Session** and asset-folder changes cannot take effect during an animation.

## How bets and payouts work

This game keeps the original program's **profit-based payouts**. A payout of **2:1** means you gain two times your bet as profit **and receive your original stake back**.

For a 25-chip bet starting from 1,000 chips:

| Result | Returned after the round | Final balance |
| --- | --- | --- |
| Lose | 0 | 975 |
| Tie / push | 25 | 1,000 |
| Win at 1:1 | 50: stake 25 + profit 25 | 1,025 |
| Win at 1.5:1 | 62.50: stake 25 + profit 37.50 | 1,037.50 |
| Win at 2:1 | 75: stake 25 + profit 50 | 1,050 |

The stake is reserved when the round begins. This explains why CHIPS decreases before the result appears. Balances are rounded to two decimal places. If you run out, click **New Session**.

## Playing each game

### Slots

1. Set your bet.
2. Click **SPIN** and wait for the animation to finish.
3. Read the three symbols and result message.

| Matching result | Profit multiplier |
| --- | --- |
| Three cherries | 1.5× bet |
| Three lemons | 2× bet |
| Three apples | 3× bet |
| Three grapes | 4× bet |
| Three gems | 6× bet |
| Three diamonds | 10× bet |
| Three BONUS symbols | 20× bet |
| Any two matching symbols | 0.75× bet |
| No matching symbols | Lose the bet |

A pair can occupy any two reel positions. BONUS is a regular paying symbol; it does not launch a separate bonus game.

### Blackjack

Try to finish closer to **21** than the dealer without going over.

1. Set your bet and click **DEAL**.
2. Choose **HIT** to take another card or **STAND** to keep your total.
3. If available, choose **DOUBLE** to double your original stake, take exactly one additional card, and stand.
4. After you stand, the dealer reveals the hidden card and draws until reaching at least 17.

Number cards have their printed value; J, Q, and K are worth 10. An ace counts as 11, reduced to 1 when needed to avoid a bust. Your total appears beside your hand.

- Going over 21 is a bust and loses the stake.
- A dealer bust or a higher valid player total wins at **1:1**.
- Equal totals are a **push**: the stake is returned.
- DOUBLE is offered only on your first two cards and when your remaining balance covers the additional stake.
- The dealer stands on all 17s, including a soft 17 containing an ace counted as 11.
- This simplified version has no splitting, insurance, surrender, or special 3:2 blackjack payout. An opening 21 moves directly to dealer play.

### Roulette

This edition uses an **American wheel with 38 outcomes: 1–36, 0, and 00**, matching the supplied artwork.

1. Set your bet.
2. Choose **Red**, **Black**, **Odd**, or **Even**, or click a numbered square for an exact-number bet.
3. Confirm the selection in the **BET** label on the table.
4. Click **PLAY**.
5. Read the final winning number in the central badge and result message.

| Bet | Winning condition | Profit payout |
| --- | --- | --- |
| Red / Black | Ball result has your selected color | 1:1 |
| Odd / Even | Result is a matching number from 1–36 | 1:1 |
| Number | Exact selected number, including 0 or 00 | 35:1 |

**0 and 00 are green and lose all red, black, odd, and even bets.** The **Number** button uses the currently selected number; clicking a square both selects that number and switches to the exact-number bet. Only one bet is placed per spin.

The moving ball is decorative. The central number badge and final result message determine the winning result; the ball does not settle on a corresponding printed pocket.

### Dice

1. Set your bet.
2. Choose **Low**, **High**, or **Seven**.
3. Click **PLAY** to roll two dice.
4. Their combined total determines the result.

| Selection | Winning total | Profit payout |
| --- | --- | --- |
| Low | 2–6 | 1.5:1 |
| High | 8–12 | 1.5:1 |
| Seven | Exactly 7 | 4:1 |

A total of 7 loses Low and High bets.

### Coin Flip

Choose **Heads** or **Tails**, set your bet, and click **PLAY**. A correct call pays **1:1**; an incorrect call loses the stake. The coin is drawn by the program rather than loaded from an image file.

### Hi-Lo

Guess whether the next card has a higher or lower rank than the current card.

1. Set your bet and click **DEAL**.
2. Click **HIGHER** or **LOWER**. Compare against the most recently revealed card, at the right of the displayed sequence.
3. After a correct guess, either keep guessing or click **CASH OUT**.
4. Five correct guesses cash out automatically.

Ranks run from **2 up to Ace**. Suits do not affect the result. Equal ranks leave the streak unchanged and let you guess again. A wrong guess loses the entire stake, including any potential profit built up in that round.

| Correct guesses | Cash-out profit |
| --- | --- |
| 1 | 1.5× bet |
| 2 | 2× bet |
| 3 | 3× bet |
| 4 | 5× bet |
| 5 | 10× bet; automatic cash-out |

Before a correct guess, **RETURN BET** ends the round and returns your stake. The program displays up to five recent cards in this round.

### Video Poker

1. Set your bet and click **DEAL** to receive five cards.
2. Click each card you want to keep. A gold outline and **HOLD** label mark held cards.
3. Click a held card again to unhold it.
4. Click **DRAW** once. All unheld cards are replaced, then the final hand is scored.

Holding no cards replaces all five. Holding all cards keeps the original hand and scores it when you click DRAW.

| Final hand | Description | Profit multiplier |
| --- | --- | --- |
| Royal flush | 10, J, Q, K, A, all one suit | 250× |
| Straight flush | Five consecutive ranks, all one suit | 50× |
| Four of a kind | Four cards of the same rank | 25× |
| Full house | Three of one rank plus two of another | 9× |
| Flush | Five cards of one suit | 6× |
| Straight | Five consecutive ranks; mixed suits allowed | 4× |
| Three of a kind | Three cards of the same rank | 3× |
| Two pair | Two separate pairs | 2× |
| Jacks or better | One pair of J, Q, K, or A | 1× |
| Other hand | Includes a single pair of 10s or lower | Lose the bet |

Aces can be low in A–2–3–4–5 or high in 10–J–Q–K–A. Only the highest qualifying hand pays. These multipliers are **profit**, following the original program; they are not a standard casino video-poker return table.

## Using the artwork

### Where the assets belong

The easiest setup is to keep these items together in the extracted game folder:

| Location | Purpose |
| --- | --- |
| `TkCasino.py` | Main program |
| `README.md` | This detailed user guide |
| 
| `assets/cards/` | 52 playing-card faces |
| `assets/slots/` | Slot symbols and additional supplied artwork |
| `assets/wheel.png` | Roulette wheel |
| `assets/dice-1.png` through `dice-6.png` | Six dice faces |
| `assets/chip-1.png` through `chip-4.png` | Four betting-chip images |

The game first uses an existing remembered folder, if available. Otherwise it looks for `assets` beside the Python file, regardless of the terminal's current directory.

### Choosing a different folder

1. Wait for any current animation to finish.
2. Click **Asset Folder…**.
3. Select the supplied **assets** folder. Selecting its containing **TkCasino** folder also works.
4. Check the bottom status line for **70/70 loaded**.

Your choice is remembered separately on each PC in `Tk_casino_settings.json' in your user home folder. Only the asset location is saved; the chip balance and game progress are not saved.

The status counts **70 required images**: 52 card faces, 7 active slot symbols, 6 dice faces, 4 chips, and 1 wheel. Extra slot artwork is included but does not increase this count.

An unrelated folder is rejected. A partially complete folder can be selected; the missing images use drawn graphics. After restoring files, reselect the folder to clear cached failures and reload images.

The original `card_set.zip` and `slots.zip` are source artwork. Select the prepared **assets** folder from the game package, rather than those ZIPs or a folder of unprepared originals.

### Moving to another PC or using a shared folder

Copy or extract **the entireTkCasino_Casino folder**, not just the `.py` file. On the other PC, run the program and choose Asset Folder… if necessary. A saved folder path from one PC is not automatically valid on another.

For a Samba share, select a folder accessible through a normal filesystem path: a mounted share on Linux, or a mapped drive/accessible network folder on Windows. The game does not mount shares or accept an `smb://` address directly. Ensure your user can read the PNG files.

### Replacing images

Back up the image first. Replace it with another **PNG of exactly the same filename and location**, then restart the game or reselect the asset folder. Keep the image canvas dimensions below because Tkinter displays these files at their stored size without automatic resizing.

| Image type | Packaged size, in pixels |
| --- | --- |
| Cards | 110 × 150 |
| Slot symbols | 150 × 140 |
| Dice | 120 × 120 |
| Betting chips | 40 × 40 |
| Wheel | 300 × 273 |

The seven active slot filenames are `cherry.png`, `lemon.png`, `apple.png`, `raz.png` (grapes), `gem.png`, `diamond.png`, and `bonus.png`, inside `assets/slots/`. Changing an image does not change its label, payout, or game rules. Extra slot files are available for customization but are not selected automatically.

Card filenames use names such as `ace_of_spades.png`, `10_of_hearts.png`, and `queen_of_clubs.png`. Card backs and the coin are deliberately drawn; they are not included in the image count.

## Troubleshooting

| Problem | What to try |
| --- | --- |
| All games show drawn graphics | Extract the complete ZIP, choose Asset Folder…, and select the packaged assets folder. |
| Only some artwork appears | Check the image count and folder permissions. Restore missing or damaged PNGs from the ZIP, then reselect the folder. |
| Folder selection says “Assets not found” | Select assets or its direct parent. Do not select a ZIP, cards alone, slots alone, or an unrelated folder. |
| Images remain missing after you copy them back | Reselect the folder or restart; failed image loads are cached until refreshed. |
| Images look oversized or cover labels | Restore the packaged files or resize replacements to the dimensions listed above. |
| Buttons are disabled | Finish the current hand, cash out Hi-Lo, or wait for the animation. |
| Bet is rejected | Enter a number such as `25` or `12.50`, at least 0.01 and within your balance. Do not include a currency symbol or commas. |
| Cannot double in blackjack | Double is available only on the opening two cards and requires enough additional chips. |
| Window closes immediately | Start from a terminal to see the error. Confirm Python and Tkinter are installed. |
| No display / DISPLAY error | Run from a graphical desktop. An ordinary SSH terminal without graphical forwarding cannot show the window. |
| Controls extend beyond the screen | Maximize the window. Its minimum size is 980 × 780; a larger display workspace or reduced desktop scaling may be needed. |
| Folder preference cannot be saved | The selected images still work for the session. Check write permissions for your user home folder. |
| Balance resets after restarting | Expected: balance, totals, and hands are kept only for the current running session. |

## Current scope

This is a local, single-player Tkinter application with random outcomes. It has no saved games, sound controls, multiplayer, real-money features, or automatic image resizing. Closing the application ends the session. The supplied art is user-provided; this package does not establish redistribution rights for that artwork.

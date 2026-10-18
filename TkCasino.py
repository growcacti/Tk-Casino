#!/usr/bin/env python   3
"""TkCasino. Python 3 + Tkinter; no external assets required.
ALl chips are fictional. Original game's net-profit payouts are retained.
"""
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog
import json
import random
import math
from collections import Counter

BG = '#101923'
PANEL = '#1c2a38'
FELT = '#125347'
GOLD = '#f4c66a'
WHITE = '#f5f2e9'
RED = '#d74759'
RANKS = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
REDS = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
GAMES = ['Slots','Blackjack','Roulette','Dice','Coin Flip','Hi-Lo','Video Poker']
RULES = {
 'Slots':'Three matching symbols win 1.5–20 times your bet as profit. Any pair wins 0.75 times. No match loses the bet.',
 'Blackjack':'Get closer to 21 than the dealer. Aces count as 1 or 11. Dealer stands on all 17s. Win pays 1:1; ties push. Double on the first two cards only. No splitting or special natural payout.',
 'Roulette':'American wheel with 0 and 00. Red/black and odd/even pay 1:1. Exact number pays 35:1. Both 0 and 00 lose all outside bets. Select a number by clicking its square.',
 'Dice':'Two fair dice. Low (2–6) or High (8–12) pays 1.5:1. Seven pays 4:1.',
 'Coin Flip':'Choose heads or tails. Correct guess pays 1:1.',
 'Hi-Lo':'Ace is high. Guess higher/lower. Equal ranks do not change the streak. Cash out for profit of 1.5, 2, 3, 5 or 10 times your bet. Wrong guess loses the bet. Five correct guesses cash out automatically.',
 'Video Poker':'Click cards to HOLD, then Draw. Profit multipliers: royal flush 250, straight flush 50, four of a kind 25, full house 9, flush 6, straight 4, trips 3, two pair 2, jacks or better 1. Other hands lose.'}

def deck():
    cards = [(r,s) for r in RANKS for s in range(4)]
    random.shuffle(cards) 
    return cards

def value(hand):
    total = sum(11 if r == 'A' else 10 if r in 'JQK' else int(r) for r,s in hand)
    aces = sum(r == 'A' for r,s in hand)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def poker(hand):
    counts = Counter(r for r,s in hand)
    groups = sorted(counts.values(), reverse=True)
    vals = sorted(RANKS.index(r) for r,s in hand)
    flush = len({s for r,s in hand}) == 1
    straight = len(counts) == 5 and (vals[-1]-vals[0] == 4 or vals == [0,1,2,3,12])
    if straight and flush: return ('Royal flush',250) if vals == [8,9,10,11,12] else ('Straight flush',50)
    if groups == [4,1]: return 'Four of a kind',25
    if groups == [3,2]: return 'Full house',9
    if flush: return 'Flush',6
    if straight: return 'Straight',4
    if groups == [3,1,1]: return 'Three of a kind',3
    if groups == [2,2,1]: return 'Two pair',2
    if any(n == 2 and r in ('J','Q','K','A') for r,n in counts.items()): return 'Jacks or better',1
    return 'No winning hand',0

class Casino:
    def __init__(self, root):
        self.root = root
        self.images = {}
        self.asset_dir = Path(  __file__).resolve().parent / 'assets'
        self.settings_path = Path.home() / '.Tk_casino_settings.json'
        try:
            saved = json.loads(self.settings_path.read_text(encoding='utf-8'))
            folder = saved.get('asset_folder') if isinstance(saved,dict) else None
            if isinstance(folder,str) and Path(folder).is_dir():
                self.asset_dir = Path(folder)
        except (OSError,ValueError):
            pass
        root.title('Tk Casino')
        root.configure(bg=BG)
        root.geometry('1080x820')
        root.minsize(980,780)
        self.balance = 1000.0
        self.rounds = self.wins = 0
        self.active = self.busy = False
        self.game = 'Slots'
        self.choice = 'Red'
        self.number = 0
        self.history = []
        self.bet = tk.StringVar(value='25')
        self.status = tk.StringVar(value='Choose a game, set your bet, and play.')
        top = tk.Frame(root,bg=BG)
        top.pack(fill='x',padx=24,pady=12)
        tk.Label(top,text='C A S I N O',font=('DejaVu Sans',28,'bold'),fg=GOLD,bg=BG).pack(side='left')
        tk.Label(top,text='  PLAYER  •  CASH',fg=WHITE,bg=BG).pack(side='left')
        self.bank = tk.Label(top,fg=GOLD,bg=BG,font=('DejaVu Sans',14,'bold'))
        self.bank.pack(side='right')
        nav = tk.Frame(root,bg=BG)
        nav.pack(fill='x',padx=18)
        self.nav = {}
        for name in GAMES:
            self.nav[name] = self.button(nav,name,lambda n=name:self.select(n))
            self.nav[name].pack(side='left',padx=3)
        self.canvas = tk.Canvas(root,width=940,height=430,bg=FELT,highlightthickness=2,highlightbackground=GOLD)
        self.canvas.pack(pady=15)
        self.canvas.bind('<Button-1>',self.click_table)
        tk.Label(root,textvariable=self.status,bg=BG,fg=WHITE,font=('DejaVu Sans',12),wraplength=940).pack(pady=4)
        betting = tk.Frame(root,bg=BG)
        betting.pack(pady=8)
        tk.Label(betting,text='BET',fg=GOLD,bg=BG).pack(side='left',padx=8)
        self.entry = tk.Entry(betting,textvariable=self.bet,width=10,font=('DejaVu Sans',13),justify='center')
        self.entry.pack(side='left')
        self.chips = []
        for chip_number, amount in enumerate((5,25,50,100),1):
            b=self.button(betting,str(amount),lambda a=amount:self.bet.set(str(a)))
            img = self.asset(f'chip-{chip_number}.png')
            if img: b.config(image=img,compound='left')
            b.pack(side='left',padx=4)
            self.chips.append(b)
        self.actions = tk.Frame(root,bg=BG)
        self.actions.pack(pady=4)
        bottom = tk.Frame(root,bg=BG)
        bottom.pack(fill='x',padx=24,pady=8)
        self.button(bottom,'Rules / Help',self.help).pack(side='left')
        self.button(bottom,'New Session',self.reset).pack(side='left',padx=8)
        self.button(bottom,'LOAD GFX',self.choose_asset_folder).pack(side='left',padx=8)
        self.stats = tk.Label(bottom,bg=BG,fg='#adbdc8')
        self.stats.pack(side='right')
        self.log = tk.Label(root,bg=BG,fg='#adbdc8',font=('DejaVu Sans',10))
        self.log.pack()
        self.asset_status = tk.Label(root,bg=BG,fg=GOLD,font=('DejaVu Sans',9),wraplength=940)
        self.asset_status.pack(pady=3)
        self.select('Slots')
        self.refresh_assets()

    @staticmethod
    def expected_assets():
        files = ['wheel.png']
        files += [f'chip-{i}.png' for i in range(1,5)]
        files += [f'dice-{i}.png' for i in range(1,7)]
        files += [f'slots/{n}.png' for n in ('cherry','lemon','apple','raz','gem','diamond','bonus')]
        for rank in RANKS:
            name={'A':'ace','K':'king','Q':'queen','J':'ja      ck'}.get(rank,rank)
            files += [f'cards/{name}_of_{suit}.png' for suit in ('spades','hearts','diamonds','clubs')]
        return files

    def refresh_assets(self):
        # Clear failed lookups as well, allowing a repaired folder to be reloaded.
        self.images.clear()
        expected=self.expected_assets()
        loaded=sum(self.asset(name) is not None for name in expected)
        for i,button in enumerate(self.chips,1):
            image=self.asset(f'chip-{i}.png')
            button.config(image=image if image is not None else '',compound='left')
        mode='Images ready' if loaded==len(expected) else 'Using fallback for missing/unreadable images'
        self.asset_status.config(text=f'{mode}: {loaded}/{len(expected)} loaded • {self.asset_dir}')
        self.draw()
        return loaded

    def choose_asset_folder(self):
        if self.busy:
            self.status.set('Wait for the animation to finish before changing the asset folder.')
            return
        folder=filedialog.askdirectory(parent=self.root,title='Choose assets folder (or the Tk_Casino folder)',
                                       initialdir=str(self.asset_dir if self.asset_dir.is_dir() else Path(__file__).resolve().parent))
        if not folder:return
        chosen=Path(folder)
        if (chosen/'assets').is_dir():chosen=chosen/'assets'
        # Reject unrelated folders without discarding a working configuration.
        if not any((chosen/name).is_file() for name in self.expected_assets()):
            messagebox.showwarning('Assets not found','Choose the supplied assets folder containing cards, slots, wheel.png, dice-1.png and chip-1.png. Extract the complete game ZIP first.',parent=self.root)
            return
        self.asset_dir=chosen
        loaded=self.refresh_assets()
        if loaded==0:
            self.status.set('No images could be read. Check the folder permissions and PNG files; fallback is active.')
        try:
            self.settings_path.write_text(json.dumps({'asset_folder':str(chosen)},indent=2),encoding='utf-8')
        except OSError:
            messagebox.showwarning('Folder selected','Images are selected for this session, but the folder preference could not be saved in your home folder.',parent=self.root)

    def asset(self, name):
        if name not in self.images:
            try:
                self.images[name] = tk.PhotoImage(file=str(self.asset_dir / name))
            except tk.TclError:
                self.images[name] = None
        return self.images[name]

    def button(self,parent,text,cmd):
        return tk.Button(parent,text=text,command=cmd,bg=PANEL,fg=WHITE,activebackground=GOLD,activeforeground=BG,relief='flat',padx=12,pady=8,cursor='hand2',font=('DejaVu Sans',10,'bold'))

    def text(self,x,y,text,size=20,color=WHITE):
        self.canvas.create_text(x,y,text=text,fill=color,font=('DejaVu Sans',size,'bold'))

    def update(self):
        self.bank.config(text=f'CHIPS  {self.balance:,.2f}')
        self.stats.config(text=f'Rounds {self.rounds}  •  Wins {self.wins}  •  Session {self.balance-1000:+,.2f}')
        locked = self.active or self.busy
        for b in self.nav.values(): b.config(state='disabled' if locked else 'normal')
        self.nav[self.game].config(bg=GOLD,fg=BG)
        self.entry.config(state='disabled' if locked else 'normal')
        for b in self.chips: b.config(state='disabled' if locked else 'normal')
        self.log.config(text='   |   '.join(self.history[-3:]))

    def controls(self,items):
        for child in self.actions.winfo_children(): child.destroy()
        for label,fn in items: self.button(self.actions,label,fn).pack(side='left',padx=5)
        self.update()

    def select(self,name):
        if self.active or self.busy: return
        for b in self.nav.values(): b.config(bg=PANEL,fg=WHITE)
        self.game=name
        self.choice={'Roulette':'Red','Dice':'Low','Coin Flip':'Heads'}.get(name,'')
        self.hand=[]
        self.dealer=[]
        self.held=set()
        self.reels=[0,4,6]
        self.dice=[1,6]
        self.coin='?'
        self.spin=None
        self.streak=0
        self.status.set('Set your bet, then choose an action. Rules / Help explains payouts.')
        self.idle_controls()
        self.draw()

    def idle_controls(self):
        if self.game in ('Roulette','Dice','Coin Flip'):
            opts={'Roulette':['Red','Black','Odd','Even','Number'],'Dice':['Low','High','Seven'],'Coin Flip':['Heads','Tails']}[self.game]
            self.controls([(f'[{o}]' if o==self.choice else o,lambda v=o:self.choose(v)) for o in opts]+[('PLAY',self.start)])
        else: self.controls([('DEAL' if self.game in ('Blackjack','Hi-Lo','Video Poker') else 'SPIN',self.start)])

    def choose(self,v):
        if self.active or self.busy:return
        self.choice=v
        self.idle_controls()
        self.draw()

    def reserve(self):
        try: amount=float(self.bet.get())
        except ValueError: amount=0
        if not math.isfinite(amount) or amount<0.01 or amount>self.balance:
            self.status.set('Enter a bet of at least 0.01, within your balance. New Session refills your chips.')
            return False
        self.wager=round(amount,2)
        if self.wager>self.balance:return False
        self.balance=round(self.balance-self.wager,2)
        self.active=True
        return True

    def finish(self,label,mult):
        # Stake was reserved: a win returns it plus the original net-profit multiplier.
        payout=self.wager*(1+mult) if mult>=0 else 0
        net=round(payout-self.wager,2)
        self.balance=round(self.balance+payout,2)
        self.rounds+=1
        self.wins+=net>0
        self.active=self.busy=False
        self.history.append(f'{self.game}: {net:+,.2f}')
        self.status.set(f'{label}   •   {net:+,.2f} chips' + ('   •   New Session to play again.' if self.balance<0.01 else ''))
        self.idle_controls()
        self.draw()

    def start(self):
        if self.active or self.busy or not self.reserve():return
        self.cards=deck()
        self.hand=[]
        self.held=set()
        self.controls([])
        if self.game=='Blackjack':
            self.hand=[self.cards.pop(),self.cards.pop()]
            self.dealer=[self.cards.pop(),self.cards.pop()]
            self.status.set('Hit, stand, or double your opening bet.')
            if value(self.hand)==21 or value(self.dealer)==21:self.stand()
            else:self.blackjack_controls()
        elif self.game=='Video Poker':
            self.hand=[self.cards.pop() for _ in range(5)]
            self.status.set('Click cards to HOLD them, then click DRAW.')
            self.controls([('DRAW',self.poker_draw)])
        elif self.game=='Hi-Lo':
            self.hand=[self.cards.pop()]
            self.streak=0
            self.hilo_controls()
        else:
            self.busy=True
            self.status.set('Spinning...' if self.game in ('Slots','Roulette') else 'Rolling...' if self.game=='Dice' else 'Flipping...')
            self.animate(0)
        self.draw()

    def animate(self,tick):
        if self.game=='Slots': self.reels=[random.randrange(7) for _ in range(3)]
        elif self.game=='Dice':self.dice=[random.randint(1,6) for _ in range(2)]
        elif self.game=='Coin Flip':self.coin=random.choice(['Heads','Tails'])
        else:self.spin=random.randrange(38)
        self.draw()
        if tick<18:
            self.root.after(45+tick*4,lambda:self.animate(tick+1))
            return
        if self.game=='Slots':
            a,b,c=self.reels
            mult=[1.5,2,3,4,6,10,20][a] if a==b==c else .75 if len(set(self.reels))==2 else -1
            self.finish('Three of a kind!' if a==b==c else 'Pair!' if mult>0 else 'No match',mult)
        elif self.game=='Dice':
            total=sum(self.dice)
            win=(self.choice=='Low' and total<=6) or (self.choice=='High' and total>=8) or (self.choice=='Seven' and total==7)
            self.finish(f'Rolled {total}',(4 if self.choice=='Seven' else 1.5) if win else -1)
        elif self.game=='Coin Flip':self.finish(self.coin,1 if self.coin==self.choice else -1)
        else:
            n=self.spin
            win=(self.choice=='Number' and n==self.number) or (n not in (0,37) and ((self.choice=='Red' and n in REDS) or (self.choice=='Black' and n not in REDS) or (self.choice=='Odd' and n%2==1) or (self.choice=='Even' and n%2==0)))
            self.finish(f'{self.number_label(n)} — '+('Green' if n in (0,37) else 'Red' if n in REDS else 'Black'),(35 if self.choice=='Number' else 1) if win else -1)

    def blackjack_controls(self):
        items=[('HIT',self.hit),('STAND',self.stand)]
        if len(self.hand)==2 and self.balance>=self.wager:items.append(('DOUBLE',self.double))
        self.controls(items)

    def hit(self):
        self.hand.append(self.cards.pop())
        if value(self.hand)>21:self.finish('Bust!',-1)
        elif value(self.hand)==21:self.stand()
        else:self.blackjack_controls();self.draw()

    def double(self):
        if self.balance<self.wager:return
        self.balance=round(self.balance-self.wager,2)
        self.wager*=2
        self.hand.append(self.cards.pop())
        if value(self.hand)>21:self.finish('Bust!',-1)
        else:self.stand()

    def stand(self):
        self.busy=True
        self.controls([])
        self.dealer_step()

    def dealer_step(self):
        self.draw()
        if value(self.dealer)<17:
            self.dealer.append(self.cards.pop())
            self.root.after(450,self.dealer_step)
            return
        p,d=value(self.hand),value(self.dealer)
        self.finish('Dealer busts!' if d>21 else f'You {p} • Dealer {d}',1 if d>21 or p>d else 0 if p==d else -1)

    def poker_draw(self):
        for i in range(5):
            if i not in self.held:self.hand[i]=self.cards.pop()
        name,mult=poker(self.hand)
        self.finish(name,mult if mult else -1)

    def hilo_controls(self):
        self.status.set(f'Streak {self.streak}/5 • Ace is high • '+(f'Cash out profit: {self.wager*[1.5,2,3,5,10][self.streak-1]:,.2f}' if self.streak else 'Guess higher or lower; ties replay.'))
        self.controls([('HIGHER',lambda:self.guess(True)),('LOWER',lambda:self.guess(False)),('CASH OUT' if self.streak else 'RETURN BET',self.cashout)])

    def guess(self,higher):
        old=RANKS.index(self.hand[-1][0])
        self.hand.append(self.cards.pop())
        new=RANKS.index(self.hand[-1][0])
        self.hand=self.hand[-5:]
        if new==old:self.hilo_controls();self.status.set('Same rank — streak unchanged. Guess again.')
        elif (new>old)==higher:
            self.streak+=1
            if self.streak==5:self.cashout()
            else:self.hilo_controls()
        else:self.finish('Wrong guess',-1)
        self.draw()

    def cashout(self):self.finish('Cashed out' if self.streak else 'Bet returned',[1.5,2,3,5,10][self.streak-1] if self.streak else 0)

    @staticmethod
    def number_label(n):
        return '00' if n == 37 else str(n)

    def click_table(self,event):
        if self.busy:return
        x,y=event.x,event.y
        if self.game=='Video Poker' and self.active and 140<=y<=310:
            for i in range(5):
                if 140+i*135<=x<=250+i*135:
                    if i in self.held:self.held.remove(i)
                    else:self.held.add(i)
                    self.draw()
        elif self.game=='Roulette' and not self.active:
            for n in range(38):
                left=360+(n%10)*54;top=125+(n//10)*58
                if left<=x<=left+49 and top<=y<=top+50:
                    self.number=n;self.choice='Number';self.idle_controls();self.draw();break

    def card(self,x,y,card,hidden=False,held=False):
        c=self.canvas
        rank,suit=card
        filename = {'A':'ace','K':'king','Q':'queen','J':'jack'}.get(rank,rank)
        image = None if hidden else self.asset(f'cards/{filename}_of_{["spades","hearts","diamonds","clubs"][suit]}.png')
        if image:
            c.create_image(x+55,y+75,image=image)
            if held:
                c.create_rectangle(x-2,y-2,x+112,y+152,outline=GOLD,width=4)
                self.text(x+55,y+170,'HOLD',13,GOLD)
            return
        c.create_rectangle(x,y,x+110,y+150,fill='#243d76' if hidden else WHITE,outline=GOLD if held else '#c4cabf',width=4 if held else 2)
        if hidden:
            for j in range(6):c.create_line(x+10,y+15+j*23,x+100,y+15+j*23,fill='#6484bd')
            self.text(x+55,y+75,'?',36)
        else:
            rank,suit=card
            color=RED if suit in (1,2) else '#17232e'
            self.text(x+23,y+24,rank,18,color)
            self.text(x+55,y+77,['♠','♥','♦','♣'][suit],42,color)
            self.text(x+87,y+126,rank,18,color)
        if held:self.text(x+55,y+170,'HOLD',13,GOLD)

    def die(self,x,y,n):
        image=self.asset(f'dice-{n}.png')
        if image:
            self.canvas.create_image(x+60,y+60,image=image)
            return
        self.canvas.create_rectangle(x,y,x+120,y+120,fill=WHITE,outline=GOLD,width=3)
        dots={1:[(1,1)],2:[(0,0),(2,2)],3:[(0,0),(1,1),(2,2)],4:[(0,0),(2,0),(0,2),(2,2)],5:[(0,0),(2,0),(1,1),(0,2),(2,2)],6:[(0,0),(0,1),(0,2),(2,0),(2,1),(2,2)]}
        for dx,dy in dots[n]:
            cx=x+26+dx*34;cy=y+26+dy*34
            self.canvas.create_oval(cx-9,cy-9,cx+9,cy+9,fill=RED,outline='')

    def draw(self):
        c=self.canvas
        c.delete('all')
        self.text(470,32,self.game.upper(),22,GOLD)
        if self.active:self.text(470,65,f'In play: {self.wager:,.2f}',12)
        if self.game=='Slots':
            names=['CHERRY','LEMON','APPLE','GRAPES','GEM','DIAMOND','BONUS']
            files=['cherry','lemon','apple','raz','gem','diamond','bonus']
            colors=[RED,'#e2c82d','#f5a33f','#b58bd9',GOLD,'#65dae7',RED]
            for i,n in enumerate(self.reels):
                x=170+i*205
                c.create_rectangle(x,125,x+185,310,fill=BG,outline=GOLD,width=4)
                image=self.asset(f'slots/{files[n]}.png')
                if image:c.create_image(x+92,205,image=image)
                else:self.text(x+92,211,names[n],22,colors[n])
                self.text(x+92,281,names[n],13)
            self.text(470,362,'TRIPLES  1.5–20:1     •     ANY PAIR  0.75:1',14,GOLD)
        elif self.game=='Blackjack':
            self.text(92,105,'DEALER',13,GOLD)
            for i,card in enumerate(self.dealer):self.card(180+i*min(118,600/max(1,len(self.dealer))),85,card,self.active and not self.busy and i==1)
            self.text(92,290,'YOU',13,GOLD)
            for i,card in enumerate(self.hand):self.card(180+i*min(118,600/max(1,len(self.hand))),260,card)
            if self.hand:self.text(85,325,str(value(self.hand)),24)
            if self.dealer and (not self.active or self.busy):self.text(85,144,str(value(self.dealer)),24)
        elif self.game=='Roulette':
            cx,cy=172,232
            image=self.asset('wheel.png')
            if image:
                c.create_image(cx,cy,image=image)
            else:
                c.create_oval(cx-120,cy-120,cx+120,cy+120,fill=BG,outline=GOLD,width=4)
            if self.busy:
                angle=math.radians((self.spin or 0)*360/38)
                bx=cx+112*math.sin(angle);by=cy-112*math.cos(angle)
                c.create_oval(bx-6,by-6,bx+6,by+6,fill=WHITE,outline=GOLD,width=2)
            c.create_rectangle(96,cy-27,248,cy+27,fill=BG,outline=GOLD,width=2)
            self.text(cx,cy,self.number_label(self.spin) if self.spin is not None else 'READY',27,GOLD)
            self.text(cx,385,f'BET: {self.number_label(self.number) if self.choice=="Number" else self.choice}',17,GOLD)
            for n in range(38):
                x=360+(n%10)*54;y=125+(n//10)*58
                c.create_rectangle(x,y,x+49,y+50,fill='#348867' if n in (0,37) else RED if n in REDS else BG,outline=GOLD if self.choice=='Number' and n==self.number else '#86a59a',width=3 if self.choice=='Number' and n==self.number else 1)
                self.text(x+24,y+25,self.number_label(n),16)
        elif self.game=='Dice':
            for i,n in enumerate(self.dice):self.die(300+i*210,160,n)
            self.text(470,335,f'TOTAL  {sum(self.dice)}     •     BET: {self.choice.upper()}',21,GOLD)
        elif self.game=='Coin Flip':
            c.create_oval(350,100,590,340,fill=GOLD,outline='#a77d2f',width=7)
            c.create_oval(365,115,575,325,outline='#a77d2f',width=3)
            self.text(470,216,self.coin.upper(),28,BG)
            self.text(470,380,f'YOUR CALL: {self.choice.upper()}',17,GOLD)
        else:
            for i,card in enumerate(self.hand):self.card(140+i*135,140,card,held=i in self.held if self.game=='Video Poker' else False)
            if not self.hand:self.text(470,220,'DEAL TO BEGIN',24)
            self.text(470,380,'CLICK CARDS TO HOLD' if self.game=='Video Poker' else 'PROFIT LADDER:  1.5x   2x   3x   5x   10x',15,GOLD)

    def help(self):
        messagebox.showinfo(self.game+' — Rules',RULES[self.game]+'\n\nPayouts describe PROFIT, matching the original game. Your stake is also returned on wins and ties. Fictional chips only.\n\nLinux: python3 Tk_Casino.py\nIf Tkinter is missing: sudo apt install python3-tk\nWindows: install Python with Tcl/Tk enabled, then double-click the file.',parent=self.root)

    def reset(self):
        if self.busy:return
        if not messagebox.askyesno('New Session','Reset to 1,000 chips? Any current hand will be discarded.',parent=self.root):return
        self.active=False
        self.balance=1000.0
        self.rounds=self.wins=0
        self.history=[]
        self.select(self.game)

if __name__=='__main__':
    root=tk.Tk()
    Casino(root)
    root.mainloop()

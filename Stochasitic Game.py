# %%
import tkinter as tk
from tkinter import ttk, messagebox
import random
from typing import Dict, List

class AIStartupGameGUI:
    """
    AI Startup Funding Journey - GUI Version with Tkinter
    A stochastic game simulating AI startup decision-making under uncertainty
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI Startup Funding Journey")
        self.root.geometry("1000x800")
        self.root.configure(bg='#1e293b')
        
        # Game state variables
        self.difficulty = None
        self.quarter = 1
        self.cash = 500000
        self.burn_rate = 40000
        self.team_size = 3
        self.product_dev = 30
        self.market_traction = 10
        self.funding_round = "Seed"
        self.valuation = 2000000
        self.quarters_survived = 0
        self.event_log = []
        self.game_active = False
        
        self.show_main_menu()
        
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def show_main_menu(self):
        """Display main menu"""
        self.clear_window()
        
        # Title
        title_frame = tk.Frame(self.root, bg='#1e293b')
        title_frame.pack(pady=50)
        
        title = tk.Label(title_frame, text="🚀 AI STARTUP FUNDING JOURNEY 🚀", 
                        font=('Arial', 28, 'bold'), fg='#60a5fa', bg='#1e293b')
        title.pack()
        
        subtitle = tk.Label(title_frame, 
                           text="Navigate the uncertain world of AI entrepreneurship",
                           font=('Arial', 14), fg='#cbd5e1', bg='#1e293b')
        subtitle.pack(pady=10)
        
        # Difficulty selection
        diff_frame = tk.Frame(self.root, bg='#1e293b')
        diff_frame.pack(pady=30)
        
        # Basic Mode Card
        basic_frame = tk.Frame(diff_frame, bg='#0f172a', relief='raised', borderwidth=3)
        basic_frame.grid(row=0, column=0, padx=20, pady=10)
        
        tk.Label(basic_frame, text="BASIC MODE", font=('Arial', 18, 'bold'), 
                fg='#22c55e', bg='#0f172a').pack(pady=10)
        tk.Label(basic_frame, text="More predictable market conditions",
                font=('Arial', 11), fg='#cbd5e1', bg='#0f172a').pack(pady=5)
        
        basic_features = [
            "• Higher starting cash ($500k)",
            "• Lower burn rate ($40k/mo)",
            "• Fewer random events",
            "• Better decision outcomes"
        ]
        for feature in basic_features:
            tk.Label(basic_frame, text=feature, font=('Arial', 10), 
                    fg='#94a3b8', bg='#0f172a', anchor='w').pack(pady=2, padx=20)
        
        tk.Button(basic_frame, text="START BASIC MODE", font=('Arial', 12, 'bold'),
                 bg='#22c55e', fg='white', command=lambda: self.start_game('basic'),
                 padx=20, pady=10, cursor='hand2').pack(pady=15)
        
        # Advanced Mode Card
        advanced_frame = tk.Frame(diff_frame, bg='#0f172a', relief='raised', borderwidth=3)
        advanced_frame.grid(row=0, column=1, padx=20, pady=10)
        
        tk.Label(advanced_frame, text="ADVANCED MODE", font=('Arial', 18, 'bold'),
                fg='#ef4444', bg='#0f172a').pack(pady=10)
        tk.Label(advanced_frame, text="Volatile, unpredictable environment",
                font=('Arial', 11), fg='#cbd5e1', bg='#0f172a').pack(pady=5)
        
        advanced_features = [
            "• Lower starting cash ($400k)",
            "• Higher burn rate ($50k/mo)",
            "• Frequent random events",
            "• Market volatility"
        ]
        for feature in advanced_features:
            tk.Label(advanced_frame, text=feature, font=('Arial', 10),
                    fg='#94a3b8', bg='#0f172a', anchor='w').pack(pady=2, padx=20)
        
        tk.Button(advanced_frame, text="START ADVANCED MODE", font=('Arial', 12, 'bold'),
                 bg='#ef4444', fg='white', command=lambda: self.start_game('advanced'),
                 padx=20, pady=10, cursor='hand2').pack(pady=15)
        
    def start_game(self, difficulty):
        """Initialize game with selected difficulty"""
        self.difficulty = difficulty
        self.game_active = True
        self.quarter = 1
        self.quarters_survived = 0
        self.event_log = []
        
        if difficulty == 'basic':
            self.cash = 500000
            self.burn_rate = 40000
            self.product_dev = 30
            self.market_traction = 10
        else:  # advanced
            self.cash = 400000
            self.burn_rate = 50000
            self.product_dev = 20
            self.market_traction = 5
        
        self.team_size = 3
        self.funding_round = "Seed"
        self.valuation = 2000000
        
        self.add_log("🚀 Your AI startup journey begins! Seed funding raised.")
        self.show_game_screen()
        
    def add_log(self, message):
        """Add message to event log"""
        self.event_log.append(f"Q{self.quarter}: {message}")
        if len(self.event_log) > 10:
            self.event_log.pop(0)
            
    def show_game_screen(self):
        """Display main game screen"""
        self.clear_window()
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#1e293b')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#0f172a', relief='raised', borderwidth=2)
        header_frame.pack(fill='x', pady=(0, 10))
        
        header_top = tk.Frame(header_frame, bg='#0f172a')
        header_top.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_top, text=f"Quarter {self.quarter}", font=('Arial', 20, 'bold'),
                fg='#60a5fa', bg='#0f172a').pack(side='left')
        
        mode_color = '#22c55e' if self.difficulty == 'basic' else '#ef4444'
        tk.Label(header_top, text=f"{self.difficulty.upper()} MODE",
                font=('Arial', 12), fg=mode_color, bg='#0f172a').pack(side='left', padx=20)
        
        tk.Label(header_top, text=f"{self.funding_round} Round",
                font=('Arial', 12), fg='#cbd5e1', bg='#0f172a').pack(side='left')
        
        tk.Label(header_top, text=f"Valuation: ${self.valuation/1000000:.1f}M",
                font=('Arial', 14, 'bold'), fg='#a78bfa', bg='#0f172a').pack(side='right')
        
        # Metrics section
        metrics_frame = tk.Frame(main_frame, bg='#0f172a', relief='raised', borderwidth=2)
        metrics_frame.pack(fill='x', pady=(0, 10))
        
        metrics_grid = tk.Frame(metrics_frame, bg='#0f172a')
        metrics_grid.pack(padx=20, pady=15)
        
        # Metric cards
        runway_months = int(self.cash / self.burn_rate) if self.burn_rate > 0 else 999
        
        metrics = [
            ("💰 Cash", f"${self.cash/1000:.0f}k", f"{runway_months}mo runway", '#22c55e'),
            ("🔥 Burn Rate", f"${self.burn_rate/1000:.0f}k/mo", "", '#eab308'),
            ("👥 Team", f"{self.team_size}", "people", '#3b82f6'),
            ("⏱️ Quarters", f"{self.quarters_survived}", "survived", '#a78bfa')
        ]
        
        for i, (label, value, subtitle, color) in enumerate(metrics):
            card = tk.Frame(metrics_grid, bg='#1e293b', relief='raised', borderwidth=1)
            card.grid(row=0, column=i, padx=10, pady=5)
            
            tk.Label(card, text=label, font=('Arial', 10), fg='#94a3b8', bg='#1e293b').pack(pady=(10, 0))
            tk.Label(card, text=value, font=('Arial', 18, 'bold'), fg=color, bg='#1e293b').pack()
            if subtitle:
                tk.Label(card, text=subtitle, font=('Arial', 8), fg='#64748b', bg='#1e293b').pack(pady=(0, 10))
            else:
                tk.Label(card, text=" ", font=('Arial', 8), bg='#1e293b').pack(pady=(0, 10))
        
        # Progress bars
        progress_frame = tk.Frame(main_frame, bg='#0f172a', relief='raised', borderwidth=2)
        progress_frame.pack(fill='x', pady=(0, 10))
        
        progress_container = tk.Frame(progress_frame, bg='#0f172a')
        progress_container.pack(padx=20, pady=15, fill='x')
        
        # Product Development
        tk.Label(progress_container, text=f"📈 Product Development: {self.product_dev}%",
                font=('Arial', 11, 'bold'), fg='#60a5fa', bg='#0f172a', anchor='w').pack(fill='x')
        product_bar = ttk.Progressbar(progress_container, length=400, mode='determinate',
                                      value=self.product_dev)
        product_bar.pack(fill='x', pady=(5, 15))
        
        # Market Traction
        tk.Label(progress_container, text=f"🎯 Market Traction: {self.market_traction}%",
                font=('Arial', 11, 'bold'), fg='#22c55e', bg='#0f172a', anchor='w').pack(fill='x')
        traction_bar = ttk.Progressbar(progress_container, length=400, mode='determinate',
                                       value=self.market_traction)
        traction_bar.pack(fill='x', pady=5)
        
        # Decisions section
        decisions_frame = tk.Frame(main_frame, bg='#0f172a', relief='raised', borderwidth=2)
        decisions_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        tk.Label(decisions_frame, text="⚡ Strategic Decisions", font=('Arial', 14, 'bold'),
                fg='#cbd5e1', bg='#0f172a').pack(pady=10)
        
        buttons_container = tk.Frame(decisions_frame, bg='#0f172a')
        buttons_container.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Decision buttons
        decisions = [
            ("Hire Engineers", "💼", "-$100k | +2 Team | +$15k Burn | +Product", 
             lambda: self.action_hire(), self.cash >= 100000, '#3b82f6'),
            ("Marketing Campaign", "📢", "-$80k | ++Traction",
             lambda: self.action_marketing(), self.cash >= 80000, '#22c55e'),
            ("R&D Investment", "🔬", "-$60k | ++Product",
             lambda: self.action_research(), self.cash >= 60000, '#a78bfa'),
            ("Form Partnership", "🤝", "-$40k | +Product | +Traction",
             lambda: self.action_partnership(), self.cash >= 40000, '#eab308'),
            ("Raise Funding", "💼", f"Attempt {self.get_next_round()}",
             lambda: self.action_fundraise(), 
             self.product_dev >= 30 or self.market_traction >= 30, '#ec4899'),
            ("Pivot Strategy", "🔄", "-$50k | Reset metrics (risky)",
             lambda: self.action_pivot(), self.cash >= 50000, '#ef4444'),
        ]
        
        for i, (name, emoji, desc, cmd, enabled, color) in enumerate(decisions):
            btn_frame = tk.Frame(buttons_container, bg='#1e293b', relief='raised', borderwidth=1)
            btn_frame.grid(row=i//3, column=i%3, padx=5, pady=5, sticky='nsew')
            
            tk.Label(btn_frame, text=f"{emoji} {name}", font=('Arial', 11, 'bold'),
                    fg=color if enabled else '#475569', bg='#1e293b').pack(pady=(8, 2))
            tk.Label(btn_frame, text=desc, font=('Arial', 8),
                    fg='#94a3b8' if enabled else '#475569', bg='#1e293b').pack(pady=(0, 8))
            
            btn = tk.Button(btn_frame, text="Execute", font=('Arial', 9, 'bold'),
                           bg=color if enabled else '#334155',
                           fg='white', command=cmd if enabled else None,
                           state='normal' if enabled else 'disabled',
                           cursor='hand2' if enabled else 'arrow')
            btn.pack(pady=(0, 8), padx=10)
        
        for i in range(3):
            buttons_container.columnconfigure(i, weight=1)
        
        # Bottom section
        bottom_frame = tk.Frame(main_frame, bg='#1e293b')
        bottom_frame.pack(fill='x')
        
        # Advance Quarter button
        advance_btn = tk.Button(bottom_frame, text="▶ ADVANCE TO NEXT QUARTER",
                               font=('Arial', 12, 'bold'), bg='#6366f1', fg='white',
                               command=self.advance_quarter, padx=30, pady=12, cursor='hand2')
        advance_btn.pack(side='left', padx=(0, 10))
        
        # Event log button
        log_btn = tk.Button(bottom_frame, text="📜 Event Log",
                           font=('Arial', 10), bg='#475569', fg='white',
                           command=self.show_event_log, padx=15, pady=8, cursor='hand2')
        log_btn.pack(side='left', padx=5)
        
        # Menu button
        menu_btn = tk.Button(bottom_frame, text="🏠 Main Menu",
                            font=('Arial', 10), bg='#dc2626', fg='white',
                            command=self.confirm_quit, padx=15, pady=8, cursor='hand2')
        menu_btn.pack(side='right')
        
    def get_next_round(self):
        """Get next funding round name"""
        rounds = {"Seed": "Series A", "Series A": "Series B", "Series B": "Series C"}
        return rounds.get(self.funding_round, "Unknown")
        
    def trigger_random_event(self):
        """Trigger a random event based on difficulty"""
        if self.difficulty == 'basic':
            events = [
                {"msg": "✨ Small technical breakthrough!", "cash": 0, "prod": 8, "trac": 3, "burn": 0},
                {"msg": "📰 Positive press coverage.", "cash": 0, "prod": 0, "trac": 12, "burn": 0},
                {"msg": "🐛 Minor bug found and fixed.", "cash": -10000, "prod": -3, "trac": 0, "burn": 0},
                {"msg": "🎯 New customer signed!", "cash": 30000, "prod": 0, "trac": 8, "burn": 0},
                {"msg": "👔 Advisor joined the team.", "cash": 0, "prod": 5, "trac": 5, "burn": 0},
                {"msg": "⚡ Server costs lower than expected.", "cash": 20000, "prod": 0, "trac": 0, "burn": 0},
            ]
        else:  # advanced
            events = [
                {"msg": "🚨 Major competitor launches!", "cash": 0, "prod": -10, "trac": -15, "burn": 0},
                {"msg": "🎊 Breakthrough! Algorithm 50% better!", "cash": 0, "prod": 25, "trac": 10, "burn": 0},
                {"msg": "😰 Key engineer quits.", "cash": -50000, "prod": -15, "trac": -5, "burn": -10000},
                {"msg": "💥 Viral moment! Trending on social media.", "cash": 0, "prod": 0, "trac": 30, "burn": 0},
                {"msg": "⚠️ Data breach scare (false alarm).", "cash": -100000, "prod": 0, "trac": -12, "burn": 0},
                {"msg": "🏆 Won industry award!", "cash": 0, "prod": 5, "trac": 20, "burn": 0},
                {"msg": "🤖 GPT API costs increased 40%.", "cash": 0, "prod": 0, "trac": 0, "burn": 20000},
                {"msg": "🎯 Enterprise deal closed early!", "cash": 150000, "prod": 0, "trac": 15, "burn": 0},
            ]
        
        event = random.choice(events)
        
        self.cash = max(0, self.cash + event['cash'])
        self.product_dev = max(0, min(100, self.product_dev + event['prod']))
        self.market_traction = max(0, min(100, self.market_traction + event['trac']))
        self.burn_rate += event['burn']
        
        self.add_log(event['msg'])
        
        # Show event popup
        messagebox.showinfo("🎲 Random Event!", event['msg'])
        
    def action_hire(self):
        if self.cash < 100000:
            messagebox.showerror("Error", "Insufficient cash to hire!")
            return
        
        self.cash -= 100000
        self.team_size += 2
        self.burn_rate += 15000
        self.product_dev = min(100, self.product_dev + 5)
        
        self.add_log("💼 Hired 2 engineers. Burn rate increased.")
        self.trigger_random_event()
        self.show_game_screen()
        
    def action_marketing(self):
        if self.cash < 80000:
            messagebox.showerror("Error", "Insufficient cash for marketing!")
            return
        
        self.cash -= 80000
        gain = 15 if self.difficulty == 'basic' else 10
        self.market_traction = min(100, self.market_traction + gain)
        
        self.add_log("📢 Marketing campaign launched.")
        self.trigger_random_event()
        self.show_game_screen()
        
    def action_research(self):
        if self.cash < 60000:
            messagebox.showerror("Error", "Insufficient cash for R&D!")
            return
        
        self.cash -= 60000
        gain = 20 if self.difficulty == 'basic' else 15
        self.product_dev = min(100, self.product_dev + gain)
        
        self.add_log("🔬 Invested in R&D. Product improving.")
        self.trigger_random_event()
        self.show_game_screen()
        
    def action_partnership(self):
        if self.cash < 40000:
            messagebox.showerror("Error", "Insufficient cash for partnership!")
            return
        
        self.cash -= 40000
        self.product_dev = min(100, self.product_dev + 5)
        self.market_traction = min(100, self.market_traction + 8)
        
        self.add_log("🤝 Partnership formed.")
        self.trigger_random_event()
        self.show_game_screen()
        
    def action_fundraise(self):
        if self.product_dev < 30 and self.market_traction < 30:
            messagebox.showerror("Error", "Need higher metrics to fundraise!")
            return
        
        # Calculate success
        base_chance = (self.product_dev * 0.4 + self.market_traction * 0.6) / 100
        random_factor = 0.3 if self.difficulty == 'basic' else 0.5
        final_chance = base_chance * (1 - random_factor) + random.random() * random_factor
        
        if final_chance > 0.5:
            funding_data = {
                "Seed": (2000000 if self.difficulty == 'basic' else 1500000, 8000000, "Series A"),
                "Series A": (8000000 if self.difficulty == 'basic' else 6000000, 40000000, "Series B"),
                "Series B": (15000000, 150000000, "Series C")
            }
            
            amount, new_val, new_round = funding_data[self.funding_round]
            
            self.cash += amount
            self.valuation = new_val
            self.funding_round = new_round
            
            self.add_log(f"🎉 Raised ${amount/1000000:.1f}M in {new_round}!")
            
            if new_round == "Series C":
                self.game_won()
                return
            
            messagebox.showinfo("Success!", f"🎉 Raised ${amount/1000000:.1f}M in {new_round}!\nNew valuation: ${new_val/1000000:.1f}M")
        else:
            self.add_log("❌ Fundraising attempt failed.")
            messagebox.showwarning("Failed", "❌ Fundraising failed. Investors want more traction.")
        
        self.trigger_random_event()
        self.show_game_screen()
        
    def action_pivot(self):
        if self.cash < 50000:
            messagebox.showerror("Error", "Insufficient cash to pivot!")
            return
        
        self.cash -= 50000
        self.product_dev = max(0, self.product_dev - 20)
        self.market_traction = max(0, self.market_traction - 10)
        
        self.add_log("🔄 Pivoted strategy. Short-term setback expected.")
        self.trigger_random_event()
        self.show_game_screen()
        
    def advance_quarter(self):
        self.quarter += 1
        self.quarters_survived += 1
        
        quarterly_burn = self.burn_rate * 3
        self.cash -= quarterly_burn
        
        self.add_log(f"📅 Q{self.quarter}: Burned ${quarterly_burn/1000:.0f}k.")
        
        # Organic growth
        self.product_dev = min(100, self.product_dev + (3 if self.difficulty == 'basic' else 2))
        self.market_traction = min(100, self.market_traction + (2 if self.difficulty == 'basic' else 1))
        
        if self.cash <= 0:
            self.game_over()
        else:
            self.show_game_screen()
            
    def show_event_log(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("Event Log")
        log_window.geometry("500x400")
        log_window.configure(bg='#1e293b')
        
        tk.Label(log_window, text="📜 Recent Events", font=('Arial', 16, 'bold'),
                fg='#60a5fa', bg='#1e293b').pack(pady=15)
        
        log_frame = tk.Frame(log_window, bg='#0f172a', relief='sunken', borderwidth=2)
        log_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        for event in reversed(self.event_log[-10:]):
            tk.Label(log_frame, text=event, font=('Arial', 10),
                    fg='#cbd5e1', bg='#0f172a', anchor='w').pack(pady=3, padx=10, fill='x')
        
        tk.Button(log_window, text="Close", command=log_window.destroy,
                 bg='#475569', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=5).pack(pady=10)
        
    def game_over(self):
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#1e293b')
        frame.pack(expand=True)
        
        tk.Label(frame, text="💀", font=('Arial', 60), bg='#1e293b').pack(pady=20)
        tk.Label(frame, text="GAME OVER", font=('Arial', 36, 'bold'),
                fg='#ef4444', bg='#1e293b').pack()
        tk.Label(frame, text="Your startup ran out of cash!", font=('Arial', 14),
                fg='#cbd5e1', bg='#1e293b').pack(pady=10)
        
        stats_frame = tk.Frame(frame, bg='#0f172a', relief='raised', borderwidth=2)
        stats_frame.pack(pady=20, padx=40)
        
        stats = [
            f"Quarters Survived: {self.quarters_survived}",
            f"Final Round: {self.funding_round}",
            f"Product Dev: {self.product_dev}%",
            f"Market Traction: {self.market_traction}%",
            f"Team Size: {self.team_size}"
        ]
        
        for stat in stats:
            tk.Label(stats_frame, text=stat, font=('Arial', 12),
                    fg='#cbd5e1', bg='#0f172a').pack(pady=5, padx=30)
        
        tk.Button(frame, text="🔄 Play Again", font=('Arial', 14, 'bold'),
                 bg='#3b82f6', fg='white', command=self.show_main_menu,
                 padx=30, pady=10, cursor='hand2').pack(pady=20)
        
    def game_won(self):
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#1e293b')
        frame.pack(expand=True)
        
        tk.Label(frame, text="🎉", font=('Arial', 60), bg='#1e293b').pack(pady=20)
        tk.Label(frame, text="CONGRATULATIONS!", font=('Arial', 36, 'bold'),
                fg='#22c55e', bg='#1e293b').pack()
        tk.Label(frame, text="You've reached Series C funding!", font=('Arial', 14),
                fg='#cbd5e1', bg='#1e293b').pack(pady=10)
        
        stats_frame = tk.Frame(frame, bg='#0f172a', relief='raised', borderwidth=2)
        stats_frame.pack(pady=20, padx=40)
        
        stats = [
            f"Quarters to Victory: {self.quarters_survived}",
            f"Final Valuation: ${self.valuation/1000000:.1f}M",
            f"Product Dev: {self.product_dev}%",
            f"Market Traction: {self.market_traction}%",
            f"Team Size: {self.team_size}",
            f"Cash Remaining: ${self.cash/1000:.0f}k"
        ]
        
        for stat in stats:
            tk.Label(stats_frame, text=stat, font=('Arial', 12),
                    fg='#cbd5e1', bg='#0f172a').pack(pady=5, padx=30)
        
        tk.Button(frame, text="🏆 Play Again", font=('Arial', 14, 'bold'),
                 bg='#22c55e', fg='white', command=self.show_main_menu,
                 padx=30, pady=10, cursor='hand2').pack(pady=20)
        
    def confirm_quit(self):
        if messagebox.askyesno("Quit Game", "Are you sure you want to return to main menu?"):
            self.show_main_menu()


def main():
    root = tk.Tk()
    game = AIStartupGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# %%




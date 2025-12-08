"""
TechBuild Pro - IT Hardware Assistant (GUI Version)

A modern GUI chatbot to help customers choose PC parts and hardware specifications

Created on September 2025
@author: IT Hardware Specialist
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
from datetime import datetime
import threading

class TechBuildChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TechBuild Pro - IT Hardware Assistant")
        self.root.geometry("1100x750")
        self.root.configure(bg='#0d1117')
        
        self.customer_build = {
            'budget': 0,
            'use_case': '',
            'selected_parts': {}
        }
        
        self.chat_history = []
        self.current_category = None
        
        self._create_styles()
        self._create_widgets()
        self._show_welcome_message()
    
    def _create_styles(self):
        """Create custom styles for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colors
        bg_dark = '#0d1117'
        bg_medium = '#161b22'
        bg_light = '#21262d'
        fg_color = '#c9d1d9'
        accent_color = '#58a6ff'
        
        style.configure('TFrame', background=bg_dark)
        style.configure('Chat.TFrame', background=bg_medium)
        style.configure('TLabel', background=bg_dark, foreground=fg_color, font=('Segoe UI', 10))
        style.configure('Title.TLabel', background=bg_dark, foreground=accent_color, font=('Segoe UI', 16, 'bold'))
        style.configure('Category.TLabel', background=bg_light, foreground=fg_color, font=('Segoe UI', 11, 'bold'))
        
        style.configure('TButton', 
                       font=('Segoe UI', 10),
                       padding=8,
                       background=accent_color,
                       foreground='white')
        style.map('TButton', 
                 background=[('active', '#4184e4'), ('pressed', '#3a7dd8')])
        
        style.configure('Category.TButton',
                       font=('Segoe UI', 10),
                       padding=10,
                       background=bg_light)
    
    def _create_widgets(self):
        """Create main GUI widgets"""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Categories
        left_panel = ttk.Frame(main_container, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        left_panel.pack_propagate(False)
        
        ttk.Label(left_panel, text="🖥️ TechBuild Pro", style='Title.TLabel').pack(pady=15)
        
        # Category buttons
        categories_frame = ttk.Frame(left_panel)
        categories_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.categories = [
            ("💻 Processors (CPUs)", self.show_cpu_menu),
            ("🎮 Graphics Cards", self.show_gpu_menu),
            ("💾 Memory & Storage", self.show_memory_menu),
            ("⚡ Motherboard & Power", self.show_mobo_menu),
            ("🔧 Build Planner", self.show_build_menu),
            ("📊 My Build", self.view_current_build)
        ]
        
        for text, command in self.categories:
            btn = ttk.Button(categories_frame, text=text, command=command, style='Category.TButton')
            btn.pack(fill=tk.X, pady=5, padx=10)
        
        # About section
        about_frame = ttk.Frame(left_panel)
        about_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        ttk.Label(about_frame, text="Your IT Hardware Expert", 
                 font=('Segoe UI', 9, 'italic')).pack()
        
        # Right panel - Chat interface
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Chat display area
        chat_frame = ttk.Frame(right_panel, style='Chat.TFrame')
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrolled text for chat
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            bg='#0d1117',
            fg='#c9d1d9',
            font=('Segoe UI', 10),
            padx=15,
            pady=15,
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for styling
        self.chat_display.tag_config('bot', foreground='#58a6ff', font=('Segoe UI', 10, 'bold'))
        self.chat_display.tag_config('user', foreground='#7ee787', font=('Segoe UI', 10, 'bold'))
        self.chat_display.tag_config('system', foreground='#ffa657', font=('Segoe UI', 10, 'italic'))
        self.chat_display.tag_config('price', foreground='#f85149', font=('Segoe UI', 10, 'bold'))
        self.chat_display.tag_config('component', foreground='#d2a8ff', font=('Segoe UI', 10))
        
        # Input area
        input_frame = ttk.Frame(right_panel)
        input_frame.pack(fill=tk.X)
        
        self.user_input = ttk.Entry(input_frame, font=('Segoe UI', 11))
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.user_input.bind('<Return>', lambda e: self.send_message())
        
        send_btn = ttk.Button(input_frame, text="Send", command=self.send_message)
        send_btn.pack(side=tk.RIGHT)
    
    def add_chat_message(self, message, sender='bot', tag=None):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M")
        
        if sender == 'bot':
            self.chat_display.insert(tk.END, f"🤖 TechBuild Pro ", 'bot')
            self.chat_display.insert(tk.END, f"({timestamp})\n")
        elif sender == 'user':
            self.chat_display.insert(tk.END, f"👤 You ", 'user')
            self.chat_display.insert(tk.END, f"({timestamp})\n")
        elif sender == 'system':
            self.chat_display.insert(tk.END, f"📢 System ", 'system')
            self.chat_display.insert(tk.END, f"({timestamp})\n")
        
        if tag:
            self.chat_display.insert(tk.END, f"{message}\n\n", tag)
        else:
            self.chat_display.insert(tk.END, f"{message}\n\n")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        self.chat_history.append({'sender': sender, 'message': message, 'time': timestamp})
    
    def send_message(self):
        """Handle user message input"""
        message = self.user_input.get().strip()
        if message:
            self.add_chat_message(message, 'user')
            self.user_input.delete(0, tk.END)
            # Process user input (can be expanded for interactive responses)
            self.process_user_input(message)
    
    def process_user_input(self, message):
        """Process user input and provide responses"""
        message_lower = message.lower()
        
        if 'budget' in message_lower:
            self.add_chat_message("I can help you plan within your budget! Click on '🔧 Build Planner' to set your budget and get recommendations.")
        elif 'gaming' in message_lower:
            self.add_chat_message("Great! For gaming builds, GPU is typically the most important component. Check out the Graphics Cards section!")
        elif 'cpu' in message_lower or 'processor' in message_lower:
            self.add_chat_message("I have excellent CPU recommendations! Click on '💻 Processors (CPUs)' to see options.")
        elif 'help' in message_lower:
            self.add_chat_message("I'm here to help! Use the menu on the left to explore components, or click 'Build Planner' to get a complete system recommendation.")
        else:
            self.add_chat_message("I'm here to help with hardware selection! Use the category buttons on the left to explore components, or ask me specific questions about CPUs, GPUs, RAM, or builds.")
    
    def _show_welcome_message(self):
        """Display welcome message"""
        welcome = """Welcome to TechBuild Pro! 🎉

I'm your personal IT hardware specialist, here to help you choose the perfect PC components for your needs and budget.

Use the category buttons on the left to:
• Explore CPUs, GPUs, RAM, and Storage options
• Get motherboard and power supply recommendations
• Plan a complete build with budget guidance
• Check compatibility

Ready to build your dream PC? Let's get started! 💪"""
        
        self.add_chat_message(welcome, 'bot')
    
    def show_cpu_menu(self):
        """Display CPU options"""
        menu = """💻 PROCESSOR (CPU) OPTIONS

What type of CPU are you looking for?

1️⃣ Gaming CPUs - Optimized for high frame rates
2️⃣ Workstation CPUs - For content creation & rendering
3️⃣ Budget CPUs - Best value options under $200
4️⃣ CPU Comparison - Compare specific models

Reply with a number (1-4) or ask me anything!"""
        
        self.add_chat_message(menu, 'bot')
        self.current_category = 'cpu'
    
    def show_gpu_menu(self):
        """Display GPU options"""
        menu = """🎮 GRAPHICS CARD (GPU) OPTIONS

What type of GPU do you need?

1️⃣ Gaming GPUs - By resolution (1080p/1440p/4K)
2️⃣ Content Creation GPUs - For rendering & editing
3️⃣ Budget GPUs - Great value options
4️⃣ GPU Benchmarks - Performance comparisons

Reply with a number (1-4) or ask me anything!"""
        
        self.add_chat_message(menu, 'bot')
        self.current_category = 'gpu'
    
    def show_memory_menu(self):
        """Display memory and storage options"""
        menu = """💾 MEMORY & STORAGE OPTIONS

What would you like to know about?

1️⃣ RAM Recommendations - How much RAM do you need?
2️⃣ SSD vs HDD Guide - Which storage is right for you?
3️⃣ NVMe SSD Recommendations - Fastest storage options
4️⃣ Storage Calculator - Calculate your storage needs

Reply with a number (1-4) or ask me anything!"""
        
        self.add_chat_message(menu, 'bot')
        self.current_category = 'memory'
    
    def show_mobo_menu(self):
        """Display motherboard and power options"""
        menu = """⚡ MOTHERBOARD & POWER OPTIONS

What do you need help with?

1️⃣ Motherboard Selection - Find the right board
2️⃣ Power Supply Calculator - How many watts?
3️⃣ Cooling Solutions - Keep your PC cool
4️⃣ Case Recommendations - Find the perfect case

Reply with a number (1-4) or ask me anything!"""
        
        self.add_chat_message(menu, 'bot')
        self.current_category = 'mobo'
    
    def show_build_menu(self):
        """Display build planner options"""
        menu = """🔧 BUILD PLANNER

Let me help you plan your perfect build!

1️⃣ Set Budget & Use Case - Tell me your needs
2️⃣ Complete Build Recommendation - Get a full system
3️⃣ Compatibility Check - Verify your parts work together
4️⃣ View Current Build - See your selected components

What would you like to do?"""
        
        self.add_chat_message(menu, 'bot')
        self.show_budget_dialog()
    
    def show_budget_dialog(self):
        """Show budget selection dialog"""
        budget_window = tk.Toplevel(self.root)
        budget_window.title("Set Budget & Use Case")
        budget_window.geometry("500x550")
        budget_window.configure(bg='#0d1117')
        budget_window.transient(self.root)
        budget_window.grab_set()
        
        # Budget section
        ttk.Label(budget_window, text="💰 Select Your Budget", style='Title.TLabel').pack(pady=15)
        
        budget_frame = ttk.Frame(budget_window)
        budget_frame.pack(pady=10, padx=20, fill=tk.X)
        
        budget_var = tk.IntVar(value=1150)
        
        budgets = [
            ("Budget Build ($500-800)", 650),
            ("Mid-Range Build ($800-1500)", 1150),
            ("High-End Build ($1500-3000)", 2250),
            ("Enthusiast Build ($3000+)", 4000)
        ]
        
        for text, value in budgets:
            ttk.Radiobutton(budget_frame, text=text, variable=budget_var, value=value).pack(anchor='w', pady=5)
        
        # Custom budget
        custom_frame = ttk.Frame(budget_frame)
        custom_frame.pack(pady=10, anchor='w')
        
        ttk.Label(custom_frame, text="Custom Budget: $").pack(side=tk.LEFT)
        custom_entry = ttk.Entry(custom_frame, width=15)
        custom_entry.pack(side=tk.LEFT, padx=5)
        
        # Use case section
        ttk.Label(budget_window, text="🎯 Primary Use Case", style='Title.TLabel').pack(pady=15)
        
        usecase_frame = ttk.Frame(budget_window)
        usecase_frame.pack(pady=10, padx=20, fill=tk.X)
        
        usecase_var = tk.StringVar(value="Gaming")
        
        use_cases = [
            "Gaming",
            "Content Creation/Video Editing",
            "Office Work/Programming",
            "Gaming + Streaming",
            "AI/Machine Learning",
            "General Use"
        ]
        
        for use_case in use_cases:
            ttk.Radiobutton(usecase_frame, text=use_case, variable=usecase_var, value=use_case).pack(anchor='w', pady=5)
        
        # Submit button
        def submit_budget():
            custom = custom_entry.get()
            if custom and custom.isdigit():
                self.customer_build['budget'] = int(custom)
            else:
                self.customer_build['budget'] = budget_var.get()
            
            self.customer_build['use_case'] = usecase_var.get()
            
            budget_window.destroy()
            self.add_chat_message(f"Perfect! Budget set to ${self.customer_build['budget']:,} for {self.customer_build['use_case']}", 'system')
            self.recommend_build()
        
        ttk.Button(budget_window, text="Generate Recommendation", command=submit_budget).pack(pady=20)
    
    def recommend_build(self):
        """Generate and display build recommendation"""
        if not self.customer_build['budget'] or not self.customer_build['use_case']:
            self.add_chat_message("Please set your budget and use case first!", 'system')
            return
        
        budget = self.customer_build['budget']
        use_case = self.customer_build['use_case']
        
        self.add_chat_message(f"🔍 Analyzing requirements for {use_case} build with ${budget:,} budget...", 'system')
        
        # Build recommendations based on budget and use case
        if budget <= 800 and "Gaming" in use_case:
            build = {
                "CPU": ("AMD Ryzen 5 5600", 149),
                "GPU": ("AMD RX 6600", 229),
                "RAM": ("16GB DDR4-3200", 45),
                "Storage": ("1TB NVMe SSD", 65),
                "Motherboard": ("B450M PRO-VDH MAX", 69),
                "PSU": ("650W 80+ Bronze", 75),
                "Case": ("Cooler Master MasterBox Q300L", 44),
            }
            total = 676
        elif budget > 1500 and "Gaming" in use_case:
            build = {
                "CPU": ("AMD Ryzen 7 7800X3D", 449),
                "GPU": ("NVIDIA RTX 4070 Ti", 799),
                "RAM": ("32GB DDR5-6000", 149),
                "Storage": ("2TB NVMe SSD", 129),
                "Motherboard": ("X670 Chipset", 199),
                "PSU": ("850W 80+ Gold Modular", 139),
                "Case": ("Fractal Design Define 7", 169),
            }
            total = 2033
        elif "Content Creation" in use_case:
            build = {
                "CPU": ("AMD Ryzen 9 7950X", 699),
                "GPU": ("NVIDIA RTX 4070", 599),
                "RAM": ("64GB DDR5-5600", 299),
                "Storage": ("2TB NVMe SSD", 129),
                "Motherboard": ("X670 Chipset", 199),
                "PSU": ("850W 80+ Gold", 139),
                "Case": ("Fractal Design Meshify 2", 149),
            }
            total = 2213
        else:
            build = {
                "CPU": ("AMD Ryzen 5 7600X", 299),
                "GPU": ("NVIDIA RTX 4060 Ti", 399),
                "RAM": ("16GB DDR5-5600", 89),
                "Storage": ("1TB NVMe SSD", 65),
                "Motherboard": ("B650 Chipset", 129),
                "PSU": ("750W 80+ Gold", 109),
                "Case": ("Phanteks Eclipse P300A", 69),
            }
            total = 1159
        
        # Display build
        message = f"\n🔧 RECOMMENDED BUILD FOR {use_case.upper()}\n{'='*50}\n\n"
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"🤖 TechBuild Pro ", 'bot')
        self.chat_display.insert(tk.END, f"({datetime.now().strftime('%H:%M')})\n")
        self.chat_display.insert(tk.END, message, 'system')
        
        for component, (name, price) in build.items():
            self.chat_display.insert(tk.END, f"{component}: ", 'component')
            self.chat_display.insert(tk.END, name)
            self.chat_display.insert(tk.END, f" - ${price:,}\n", 'price')
        
        self.chat_display.insert(tk.END, f"\n{'='*50}\n")
        self.chat_display.insert(tk.END, f"TOTAL COST: ${total:,}\n", 'price')
        self.chat_display.insert(tk.END, f"Budget Remaining: ${budget - total:,}\n\n", 'system')
        
        # Add recommendations
        self.chat_display.insert(tk.END, "💡 Recommendations:\n", 'system')
        
        recommendations = []
        if "Gaming" in use_case:
            recommendations.extend([
                "✓ This build will handle modern games at high settings",
                "✓ Consider a 144Hz+ monitor to match GPU capabilities",
                "✓ Ensure adequate cooling for sustained performance"
            ])
        elif "Content Creation" in use_case:
            recommendations.extend([
                "✓ Excellent for video editing and 3D rendering",
                "✓ Consider additional storage for project files",
                "✓ Dual monitors recommended for workflow"
            ])
        
        for rec in recommendations:
            self.chat_display.insert(tk.END, f"{rec}\n")
        
        self.chat_display.insert(tk.END, "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        # Store build
        self.customer_build['selected_parts'] = {k: f"{v[0]} - ${v[1]:,}" for k, v in build.items()}
        self.customer_build['total_cost'] = total
    
    def view_current_build(self):
        """Display current build summary"""
        if not self.customer_build['selected_parts']:
            self.add_chat_message("No build selected yet! Use the Build Planner to create your custom build.", 'system')
            return
        
        message = f"\n📊 YOUR CURRENT BUILD\n{'='*50}\n\n"
        message += f"💰 Budget: ${self.customer_build['budget']:,}\n"
        message += f"🎯 Use Case: {self.customer_build['use_case']}\n"
        message += f"💵 Total Cost: ${self.customer_build.get('total_cost', 0):,}\n\n"
        message += "🔧 COMPONENTS:\n"
        
        for component, spec in self.customer_build['selected_parts'].items():
            message += f"  • {component}: {spec}\n"
        
        message += f"\n{'='*50}\n"
        message += "✅ Build saved! You can export or modify anytime."
        
        self.add_chat_message(message, 'system')
    
    def save_build(self):
        """Save build to file"""
        if not self.customer_build['selected_parts']:
            messagebox.showwarning("No Build", "Please create a build first!")
            return
        
        filename = f"techbuild_pro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.customer_build, f, indent=4)
            
            messagebox.showinfo("Success", f"Build saved to {filename}")
            self.add_chat_message(f"✅ Build saved successfully to {filename}", 'system')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save build: {e}")

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = TechBuildChatbotGUI(root)
    
    # Add menu bar
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Save Build", command=app.save_build)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", 
                         command=lambda: messagebox.showinfo("About", 
                         "TechBuild Pro v2.0\n\nYour IT Hardware Specialist\n\nCreated September 2025"))
    
    root.mainloop()

if __name__ == "__main__":
    main()
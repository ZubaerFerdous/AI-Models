# %%
"""
TechBuild Pro - Model-Based Reflex IT Hardware Assistant with GUI

A model-based reflex agent that maintains internal state and provides
intelligent hardware recommendations through a graphical interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime


# ============== MODEL COMPONENTS ==============

class UserProfileModel:
    """Tracks user preferences and build history"""
    def __init__(self):
        self.budget = 0
        self.use_case = ""
        self.selected_parts = {}
        self.preferences = {
            'brand_preference': 'neutral',
            'rgb_lighting': False,
            'quiet_operation': False
        }
        self.interaction_history = []
    
    def log_interaction(self, action):
        self.interaction_history.append({
            'time': datetime.now().strftime("%H:%M:%S"),
            'action': action
        })


class HardwareKnowledgeModel:
    """Internal knowledge base of hardware components"""
    def __init__(self):
        self.cpus = {
            'budget': [
                {'name': 'AMD Ryzen 5 5600', 'price': 149, 'cores': 6, 'use': 'Gaming'},
                {'name': 'Intel Core i5-12400F', 'price': 159, 'cores': 6, 'use': 'Gaming'}
            ],
            'mid_range': [
                {'name': 'AMD Ryzen 5 7600X', 'price': 299, 'cores': 6, 'use': 'Gaming'},
                {'name': 'Intel Core i5-13600K', 'price': 319, 'cores': 14, 'use': 'Gaming+'}
            ],
            'high_end': [
                {'name': 'AMD Ryzen 7 7800X3D', 'price': 449, 'cores': 8, 'use': 'Gaming Pro'},
                {'name': 'Intel Core i7-13700K', 'price': 409, 'cores': 16, 'use': 'All-Around'}
            ]
        }
        
        self.gpus = {
            'budget': [
                {'name': 'AMD RX 6600', 'price': 229, 'vram': '8GB', 'resolution': '1080p'},
                {'name': 'NVIDIA RTX 4060', 'price': 299, 'vram': '8GB', 'resolution': '1080p'}
            ],
            'mid_range': [
                {'name': 'AMD RX 7800 XT', 'price': 499, 'vram': '16GB', 'resolution': '1440p'},
                {'name': 'NVIDIA RTX 4070', 'price': 599, 'vram': '12GB', 'resolution': '1440p'}
            ],
            'high_end': [
                {'name': 'NVIDIA RTX 4080', 'price': 1199, 'vram': '16GB', 'resolution': '4K'},
                {'name': 'AMD RX 7900 XTX', 'price': 999, 'vram': '24GB', 'resolution': '4K'}
            ]
        }
        
        self.ram_specs = {
            'Gaming': {'size': '16GB', 'speed': 'DDR5-5600', 'price': 89},
            'Content Creation': {'size': '32GB', 'speed': 'DDR5-6000', 'price': 149},
            'Office Work': {'size': '16GB', 'speed': 'DDR4-3200', 'price': 45}
        }


class ReflexAgent:
    """Main reflex agent that perceives state and makes decisions"""
    def __init__(self):
        self.user_model = UserProfileModel()
        self.hardware_model = HardwareKnowledgeModel()
    
    def perceive_budget_tier(self):
        """Perceive which budget tier the user falls into"""
        budget = self.user_model.budget
        if budget < 800:
            return 'budget'
        elif budget < 1500:
            return 'mid_range'
        else:
            return 'high_end'
    
    def recommend_cpu(self):
        """Reflex action: recommend CPU based on current state"""
        tier = self.perceive_budget_tier()
        cpus = self.hardware_model.cpus[tier]
        
        # Apply preferences
        if self.user_model.preferences['brand_preference'] == 'AMD':
            cpus = [cpu for cpu in cpus if 'AMD' in cpu['name']]
        elif self.user_model.preferences['brand_preference'] == 'Intel':
            cpus = [cpu for cpu in cpus if 'Intel' in cpu['name']]
        
        return cpus[0] if cpus else self.hardware_model.cpus[tier][0]
    
    def recommend_gpu(self):
        """Reflex action: recommend GPU based on current state"""
        tier = self.perceive_budget_tier()
        gpus = self.hardware_model.gpus[tier]
        
        if self.user_model.preferences['brand_preference'] == 'AMD':
            gpus = [gpu for gpu in gpus if 'AMD' in gpu['name']]
        elif self.user_model.preferences['brand_preference'] == 'NVIDIA':
            gpus = [gpu for gpu in gpus if 'NVIDIA' in gpu['name']]
        
        return gpus[0] if gpus else self.hardware_model.gpus[tier][0]
    
    def recommend_ram(self):
        """Reflex action: recommend RAM based on use case"""
        use_case = self.user_model.use_case
        return self.hardware_model.ram_specs.get(use_case, self.hardware_model.ram_specs['Gaming'])
    
    def generate_complete_build(self):
        """Generate complete build based on current model state"""
        cpu = self.recommend_cpu()
        gpu = self.recommend_gpu()
        ram = self.recommend_ram()
        
        # Calculate remaining budget for other components
        remaining = self.user_model.budget - cpu['price'] - gpu['price'] - ram['price']
        
        build = {
            'CPU': f"{cpu['name']} - ${cpu['price']}",
            'GPU': f"{gpu['name']} - ${gpu['price']}",
            'RAM': f"{ram['size']} {ram['speed']} - ${ram['price']}",
            'Storage': f"1TB NVMe SSD - $65",
            'Motherboard': f"Compatible Board - ${int(remaining * 0.35)}",
            'PSU': f"750W 80+ Gold - ${int(remaining * 0.30)}",
            'Case': f"Mid Tower - ${int(remaining * 0.20)}",
            'Total': f"~${self.user_model.budget}"
        }
        
        self.user_model.selected_parts = build
        self.user_model.log_interaction(f"Generated build for {self.user_model.use_case}")
        return build


# ============== GUI APPLICATION ==============

class TechBuildProGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TechBuild Pro - Model-Based Reflex Agent")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Initialize the reflex agent
        self.agent = ReflexAgent()
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🖥️ TechBuild Pro", font=("Arial", 24, "bold"),
                bg="#2c3e50", fg="white").pack(pady=10)
        tk.Label(header_frame, text="Model-Based Reflex Hardware Assistant",
                font=("Arial", 11), bg="#2c3e50", fg="#ecf0f1").pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - User Input
        left_frame = tk.LabelFrame(main_frame, text="User Profile & Preferences",
                                   font=("Arial", 12, "bold"), bg="#ecf0f1", padx=15, pady=15)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Budget section
        tk.Label(left_frame, text="Budget ($):", font=("Arial", 10, "bold"),
                bg="#ecf0f1").grid(row=0, column=0, sticky="w", pady=5)
        self.budget_var = tk.StringVar(value="1200")
        budget_entry = tk.Entry(left_frame, textvariable=self.budget_var,
                               font=("Arial", 11), width=15)
        budget_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Use case section
        tk.Label(left_frame, text="Primary Use:", font=("Arial", 10, "bold"),
                bg="#ecf0f1").grid(row=1, column=0, sticky="w", pady=5)
        self.use_case_var = tk.StringVar(value="Gaming")
        use_case_combo = ttk.Combobox(left_frame, textvariable=self.use_case_var,
                                     values=["Gaming", "Content Creation", "Office Work"],
                                     state="readonly", width=18)
        use_case_combo.grid(row=1, column=1, pady=5, padx=5)
        
        # Brand preference
        tk.Label(left_frame, text="Brand Preference:", font=("Arial", 10, "bold"),
                bg="#ecf0f1").grid(row=2, column=0, sticky="w", pady=5)
        self.brand_var = tk.StringVar(value="neutral")
        brand_combo = ttk.Combobox(left_frame, textvariable=self.brand_var,
                                   values=["neutral", "AMD", "Intel", "NVIDIA"],
                                   state="readonly", width=18)
        brand_combo.grid(row=2, column=1, pady=5, padx=5)
        
        # Checkboxes for preferences
        self.rgb_var = tk.BooleanVar()
        tk.Checkbutton(left_frame, text="RGB Lighting", variable=self.rgb_var,
                      bg="#ecf0f1", font=("Arial", 10)).grid(row=3, column=0,
                                                             columnspan=2, sticky="w", pady=5)
        
        self.quiet_var = tk.BooleanVar()
        tk.Checkbutton(left_frame, text="Quiet Operation Priority", variable=self.quiet_var,
                      bg="#ecf0f1", font=("Arial", 10)).grid(row=4, column=0,
                                                             columnspan=2, sticky="w", pady=5)
        
        # Action buttons
        btn_frame = tk.Frame(left_frame, bg="#ecf0f1")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        tk.Button(btn_frame, text="🔍 Generate Build", command=self.generate_build,
                 bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
                 padx=15, pady=8, cursor="hand2").pack(pady=5, fill=tk.X)
        
        tk.Button(btn_frame, text="📊 View Agent State", command=self.view_agent_state,
                 bg="#3498db", fg="white", font=("Arial", 11, "bold"),
                 padx=15, pady=8, cursor="hand2").pack(pady=5, fill=tk.X)
        
        tk.Button(btn_frame, text="🔄 Reset", command=self.reset_agent,
                 bg="#e74c3c", fg="white", font=("Arial", 11, "bold"),
                 padx=15, pady=8, cursor="hand2").pack(pady=5, fill=tk.X)
        
        # Right panel - Output
        right_frame = tk.LabelFrame(main_frame, text="Recommended Build",
                                    font=("Arial", 12, "bold"), bg="#ecf0f1", padx=15, pady=15)
        right_frame.grid(row=0, column=1, sticky="nsew")
        
        self.output_text = scrolledtext.ScrolledText(right_frame, width=45, height=25,
                                                     font=("Courier New", 10), wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Initial message
        self.display_welcome_message()
    
    def display_welcome_message(self):
        welcome = """
╔════════════════════════════════════════╗
║   Welcome to TechBuild Pro!            ║
║   Model-Based Reflex Agent             ║
╚════════════════════════════════════════╝

This intelligent agent maintains an internal
model of:
  • Your budget and preferences
  • Hardware compatibility rules
  • Current market conditions
  • Component performance metrics

👈 Set your preferences on the left
🔍 Click "Generate Build" to get started!

The agent will use its internal model to
recommend the best components for your needs.
        """
        self.output_text.insert(tk.END, welcome)
    
    def update_agent_model(self):
        """Update the agent's internal model based on user inputs"""
        try:
            self.agent.user_model.budget = int(self.budget_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid budget number")
            return False
        
        self.agent.user_model.use_case = self.use_case_var.get()
        self.agent.user_model.preferences['brand_preference'] = self.brand_var.get()
        self.agent.user_model.preferences['rgb_lighting'] = self.rgb_var.get()
        self.agent.user_model.preferences['quiet_operation'] = self.quiet_var.get()
        
        return True
    
    def generate_build(self):
        """Main reflex action: perceive state and generate recommendation"""
        if not self.update_agent_model():
            return
        
        self.output_text.delete(1.0, tk.END)
        
        # Display perception phase
        self.output_text.insert(tk.END, "🔍 PERCEPTION PHASE\n", "header")
        self.output_text.insert(tk.END, "="*50 + "\n\n")
        self.output_text.insert(tk.END, f"Budget Detected: ${self.agent.user_model.budget}\n")
        self.output_text.insert(tk.END, f"Use Case: {self.agent.user_model.use_case}\n")
        self.output_text.insert(tk.END, f"Budget Tier: {self.agent.perceive_budget_tier().upper()}\n")
        self.output_text.insert(tk.END, f"Brand Preference: {self.agent.user_model.preferences['brand_preference']}\n\n")
        
        # Display action phase
        self.output_text.insert(tk.END, "⚡ REFLEX ACTION PHASE\n", "header")
        self.output_text.insert(tk.END, "="*50 + "\n\n")
        
        build = self.agent.generate_complete_build()
        
        self.output_text.insert(tk.END, "🔧 RECOMMENDED BUILD\n\n", "header")
        
        for component, spec in build.items():
            if component == 'Total':
                self.output_text.insert(tk.END, "\n" + "-"*50 + "\n")
                self.output_text.insert(tk.END, f"💰 {component}: {spec}\n", "total")
            else:
                self.output_text.insert(tk.END, f"  • {component}: {spec}\n")
        
        self.output_text.insert(tk.END, "\n✅ Build optimized for your requirements!\n")
        
        # Configure text tags for styling
        self.output_text.tag_config("header", font=("Arial", 11, "bold"), foreground="#2980b9")
        self.output_text.tag_config("total", font=("Courier New", 11, "bold"), foreground="#27ae60")
    
    def view_agent_state(self):
        """Display the internal state of the agent's model"""
        self.output_text.delete(1.0, tk.END)
        
        self.output_text.insert(tk.END, "🧠 AGENT INTERNAL MODEL STATE\n", "header")
        self.output_text.insert(tk.END, "="*50 + "\n\n")
        
        self.output_text.insert(tk.END, "📊 User Profile Model:\n", "subheader")
        self.output_text.insert(tk.END, f"  Budget: ${self.agent.user_model.budget}\n")
        self.output_text.insert(tk.END, f"  Use Case: {self.agent.user_model.use_case}\n")
        self.output_text.insert(tk.END, f"  Brand Pref: {self.agent.user_model.preferences['brand_preference']}\n")
        self.output_text.insert(tk.END, f"  RGB Lighting: {self.agent.user_model.preferences['rgb_lighting']}\n")
        self.output_text.insert(tk.END, f"  Quiet Mode: {self.agent.user_model.preferences['quiet_operation']}\n\n")
        
        self.output_text.insert(tk.END, "🔧 Selected Components:\n", "subheader")
        if self.agent.user_model.selected_parts:
            for comp, spec in self.agent.user_model.selected_parts.items():
                self.output_text.insert(tk.END, f"  {comp}: {spec}\n")
        else:
            self.output_text.insert(tk.END, "  No build generated yet.\n")
        
        self.output_text.insert(tk.END, "\n📝 Interaction History:\n", "subheader")
        if self.agent.user_model.interaction_history:
            for interaction in self.agent.user_model.interaction_history[-5:]:
                self.output_text.insert(tk.END, f"  [{interaction['time']}] {interaction['action']}\n")
        else:
            self.output_text.insert(tk.END, "  No interactions recorded yet.\n")
        
        self.output_text.tag_config("header", font=("Arial", 12, "bold"), foreground="#2c3e50")
        self.output_text.tag_config("subheader", font=("Arial", 10, "bold"), foreground="#34495e")
    
    def reset_agent(self):
        """Reset the agent's internal model"""
        if messagebox.askyesno("Reset Agent", "Reset all agent state and preferences?"):
            self.agent = ReflexAgent()
            self.budget_var.set("1200")
            self.use_case_var.set("Gaming")
            self.brand_var.set("neutral")
            self.rgb_var.set(False)
            self.quiet_var.set(False)
            self.output_text.delete(1.0, tk.END)
            self.display_welcome_message()
            messagebox.showinfo("Reset Complete", "Agent model has been reset!")


# ============== MAIN ==============

if __name__ == "__main__":
    root = tk.Tk()
    app = TechBuildProGUI(root)
    root.mainloop()

# %%




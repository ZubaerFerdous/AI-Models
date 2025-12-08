"""
Advanced IT Hardware Expert System - GUI Version
Modern GUI-based expert system for IT hardware consultation

Author: A K M Zubaer Ferdous
Course: AI
Date: September 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from typing import Dict, List, Tuple, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class UseCase(Enum):
    """Enumeration of primary use cases"""
    GAMING = "gaming"
    CONTENT_CREATION = "content_creation"
    PROGRAMMING = "programming"
    AI_ML = "ai_ml"
    SERVER = "server"
    OFFICE = "office"
    STREAMING = "streaming"

@dataclass
class Component:
    """Hardware component data structure"""
    name: str
    category: str
    price: float
    specs: Dict[str, Any]
    performance_rating: Dict[UseCase, int]

class InferenceEngine:
    """Advanced inference engine with forward chaining"""
    
    def __init__(self):
        self.facts = {}
        self.rules = []
        self.explanation_trace = []
    
    def add_fact(self, fact_name: str, value: Any):
        self.facts[fact_name] = value
        self.explanation_trace.append(f"Added fact: {fact_name} = {value}")
    
    def add_rule(self, rule_name: str, conditions: Dict, conclusions: Dict):
        self.rules.append({
            'name': rule_name,
            'conditions': conditions,
            'conclusions': conclusions,
            'fired': False
        })
    
    def evaluate_condition(self, condition_key: str, condition_value: Any) -> bool:
        if condition_key not in self.facts:
            return False
        
        fact_value = self.facts[condition_key]
        
        if isinstance(condition_value, dict):
            op = condition_value.get('operator')
            val = condition_value.get('value')
            
            if op == 'greater_than':
                return fact_value > val
            elif op == 'less_than':
                return fact_value < val
            elif op == 'in':
                return fact_value in val
        
        return fact_value == condition_value
    
    def fire_rules(self) -> List[str]:
        fired_rules = []
        changes_made = True
        iteration = 0
        
        while changes_made and iteration < 50:
            changes_made = False
            iteration += 1
            
            for rule in self.rules:
                if rule['fired']:
                    continue
                
                conditions_met = all(
                    self.evaluate_condition(k, v)
                    for k, v in rule['conditions'].items()
                )
                
                if conditions_met:
                    for k, v in rule['conclusions'].items():
                        self.facts[k] = v
                        changes_made = True
                    
                    rule['fired'] = True
                    fired_rules.append(rule['name'])
                    self.explanation_trace.append(f"Rule fired: {rule['name']}")
        
        return fired_rules
    
    def reset(self):
        self.facts.clear()
        self.explanation_trace.clear()
        for rule in self.rules:
            rule['fired'] = False

class KnowledgeBase:
    """Hardware components knowledge base"""
    
    def __init__(self):
        self.components = self._initialize_components()
    
    def _initialize_components(self) -> Dict[str, List[Component]]:
        return {
            'cpu': [
                Component(
                    name="AMD Ryzen 9 7950X",
                    category="cpu",
                    price=699,
                    specs={"cores": 16, "threads": 32, "boost": 5.7, "socket": "AM5"},
                    performance_rating={
                        UseCase.GAMING: 9, UseCase.CONTENT_CREATION: 10,
                        UseCase.AI_ML: 10, UseCase.PROGRAMMING: 9,
                        UseCase.STREAMING: 9, UseCase.OFFICE: 10
                    }
                ),
                Component(
                    name="AMD Ryzen 7 7800X3D",
                    category="cpu",
                    price=449,
                    specs={"cores": 8, "threads": 16, "boost": 5.0, "socket": "AM5"},
                    performance_rating={
                        UseCase.GAMING: 10, UseCase.CONTENT_CREATION: 8,
                        UseCase.AI_ML: 7, UseCase.PROGRAMMING: 8,
                        UseCase.STREAMING: 8, UseCase.OFFICE: 9
                    }
                ),
                Component(
                    name="Intel Core i7-13700K",
                    category="cpu",
                    price=409,
                    specs={"cores": 16, "threads": 24, "boost": 5.4, "socket": "LGA1700"},
                    performance_rating={
                        UseCase.GAMING: 9, UseCase.CONTENT_CREATION: 9,
                        UseCase.AI_ML: 8, UseCase.PROGRAMMING: 9,
                        UseCase.STREAMING: 9, UseCase.OFFICE: 9
                    }
                ),
                Component(
                    name="AMD Ryzen 5 7600X",
                    category="cpu",
                    price=299,
                    specs={"cores": 6, "threads": 12, "boost": 5.3, "socket": "AM5"},
                    performance_rating={
                        UseCase.GAMING: 8, UseCase.CONTENT_CREATION: 7,
                        UseCase.AI_ML: 6, UseCase.PROGRAMMING: 8,
                        UseCase.STREAMING: 7, UseCase.OFFICE: 8
                    }
                )
            ],
            'gpu': [
                Component(
                    name="NVIDIA RTX 4090",
                    category="gpu",
                    price=1599,
                    specs={"vram": 24, "cuda_cores": 16384, "boost": 2520},
                    performance_rating={
                        UseCase.GAMING: 10, UseCase.CONTENT_CREATION: 10,
                        UseCase.AI_ML: 10, UseCase.PROGRAMMING: 7,
                        UseCase.STREAMING: 10, UseCase.OFFICE: 6
                    }
                ),
                Component(
                    name="NVIDIA RTX 4070 Ti",
                    category="gpu",
                    price=799,
                    specs={"vram": 12, "cuda_cores": 7680, "boost": 2610},
                    performance_rating={
                        UseCase.GAMING: 9, UseCase.CONTENT_CREATION: 8,
                        UseCase.AI_ML: 8, UseCase.PROGRAMMING: 6,
                        UseCase.STREAMING: 9, UseCase.OFFICE: 5
                    }
                ),
                Component(
                    name="AMD RX 7800 XT",
                    category="gpu",
                    price=499,
                    specs={"vram": 16, "stream_processors": 3840, "boost": 2430},
                    performance_rating={
                        UseCase.GAMING: 8, UseCase.CONTENT_CREATION: 7,
                        UseCase.AI_ML: 6, UseCase.PROGRAMMING: 6,
                        UseCase.STREAMING: 8, UseCase.OFFICE: 5
                    }
                )
            ],
            'memory': [
                Component(
                    name="Corsair Dominator 32GB DDR5-6000",
                    category="memory",
                    price=179,
                    specs={"capacity": 32, "type": "DDR5", "speed": 6000},
                    performance_rating={
                        UseCase.GAMING: 8, UseCase.CONTENT_CREATION: 9,
                        UseCase.AI_ML: 9, UseCase.PROGRAMMING: 8,
                        UseCase.STREAMING: 8, UseCase.OFFICE: 7
                    }
                ),
                Component(
                    name="G.Skill Trident Z5 64GB DDR5-5600",
                    category="memory",
                    price=299,
                    specs={"capacity": 64, "type": "DDR5", "speed": 5600},
                    performance_rating={
                        UseCase.GAMING: 7, UseCase.CONTENT_CREATION: 10,
                        UseCase.AI_ML: 10, UseCase.PROGRAMMING: 9,
                        UseCase.STREAMING: 9, UseCase.OFFICE: 8
                    }
                )
            ],
            'storage': [
                Component(
                    name="Samsung 990 Pro 2TB NVMe",
                    category="storage",
                    price=129,
                    specs={"capacity": 2000, "type": "NVMe", "read": 7450, "write": 6900},
                    performance_rating={
                        UseCase.GAMING: 9, UseCase.CONTENT_CREATION: 10,
                        UseCase.AI_ML: 10, UseCase.PROGRAMMING: 9,
                        UseCase.STREAMING: 9, UseCase.OFFICE: 8
                    }
                )
            ]
        }

class ITHardwareExpertGUI:
    """Main GUI application for IT Hardware Expert System"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("IT Hardware Expert System")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1e1e1e')
        
        self.inference_engine = InferenceEngine()
        self.knowledge_base = KnowledgeBase()
        self.requirements = {}
        self.selected_build = {}
        
        self._initialize_rules()
        self._create_styles()
        self._create_widgets()
        self.show_welcome_screen()
    
    def _initialize_rules(self):
        """Initialize expert system rules"""
        self.inference_engine.add_rule(
            "gaming_gpu_priority",
            conditions={"use_case": UseCase.GAMING, "budget": {"operator": "greater_than", "value": 1200}},
            conclusions={"prioritize_gpu": True, "gpu_ratio": 0.4}
        )
        
        self.inference_engine.add_rule(
            "content_cpu_priority",
            conditions={"use_case": UseCase.CONTENT_CREATION, "budget": {"operator": "greater_than", "value": 1500}},
            conclusions={"prioritize_cpu": True, "min_cpu_cores": 12}
        )
        
        self.inference_engine.add_rule(
            "ai_ml_vram",
            conditions={"use_case": UseCase.AI_ML},
            conclusions={"min_vram": 16, "prioritize_gpu": True}
        )
        
        self.inference_engine.add_rule(
            "professional_memory",
            conditions={"use_case": {"operator": "in", "value": [UseCase.CONTENT_CREATION, UseCase.AI_ML, UseCase.PROGRAMMING]}},
            conclusions={"min_memory": 32}
        )
    
    def _create_styles(self):
        """Create custom styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        bg_color = '#1e1e1e'
        fg_color = '#ffffff'
        accent_color = '#0078d4'
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 10))
        style.configure('Title.TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 18, 'bold'))
        style.configure('Header.TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 14, 'bold'))
        style.configure('TButton', font=('Segoe UI', 10), padding=10)
        style.map('TButton', background=[('active', accent_color)])
    
    def _create_widgets(self):
        """Create main GUI widgets"""
        # Main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def show_welcome_screen(self):
        """Display welcome screen"""
        self._clear_container()
        
        welcome_frame = ttk.Frame(self.main_container)
        welcome_frame.pack(expand=True)
        
        ttk.Label(
            welcome_frame,
            text="🔧 IT Hardware Expert System",
            style='Title.TLabel'
        ).pack(pady=20)
        
        ttk.Label(
            welcome_frame,
            text="Advanced AI-powered hardware consultation with intelligent recommendations",
            font=('Segoe UI', 11)
        ).pack(pady=10)
        
        features = [
            "✓ Human-like reasoning with explanation",
            "✓ Advanced compatibility analysis",
            "✓ Performance optimization",
            "✓ Bottleneck detection"
        ]
        
        for feature in features:
            ttk.Label(welcome_frame, text=feature, font=('Segoe UI', 10)).pack(pady=5)
        
        ttk.Button(
            welcome_frame,
            text="Start Consultation",
            command=self.show_budget_screen
        ).pack(pady=30)
    
    def show_budget_screen(self):
        """Display budget selection screen"""
        self._clear_container()
        
        ttk.Label(self.main_container, text="💰 Budget Selection", style='Header.TLabel').pack(pady=20)
        
        budget_frame = ttk.Frame(self.main_container)
        budget_frame.pack(pady=20)
        
        budgets = [
            ("Budget Build", 700),
            ("Mid-Range Build", 1350),
            ("High-End Build", 2650),
            ("Enthusiast Build", 5000)
        ]
        
        self.budget_var = tk.IntVar(value=1350)
        
        for name, amount in budgets:
            ttk.Radiobutton(
                budget_frame,
                text=f"{name} (${amount:,})",
                variable=self.budget_var,
                value=amount
            ).pack(pady=5, anchor='w')
        
        # Custom budget
        custom_frame = ttk.Frame(budget_frame)
        custom_frame.pack(pady=10)
        
        ttk.Label(custom_frame, text="Custom Budget: $").pack(side=tk.LEFT)
        self.custom_budget = ttk.Entry(custom_frame, width=15)
        self.custom_budget.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            self.main_container,
            text="Next: Select Use Case",
            command=self.show_usecase_screen
        ).pack(pady=20)
    
    def show_usecase_screen(self):
        """Display use case selection screen"""
        # Get budget
        custom = self.custom_budget.get()
        if custom and custom.isdigit():
            self.requirements['budget'] = float(custom)
        else:
            self.requirements['budget'] = float(self.budget_var.get())
        
        self.inference_engine.add_fact("budget", self.requirements['budget'])
        
        self._clear_container()
        
        ttk.Label(self.main_container, text="🎯 Primary Use Case", style='Header.TLabel').pack(pady=20)
        
        usecase_frame = ttk.Frame(self.main_container)
        usecase_frame.pack(pady=20)
        
        use_cases = [
            (UseCase.GAMING, "🎮 Gaming", "High FPS, VR, Competitive"),
            (UseCase.CONTENT_CREATION, "🎨 Content Creation", "Video/Photo Editing, 3D"),
            (UseCase.AI_ML, "🤖 AI/Machine Learning", "Training, Research"),
            (UseCase.PROGRAMMING, "💻 Programming", "IDEs, Compilation"),
            (UseCase.STREAMING, "📡 Streaming", "OBS, Multi-tasking"),
            (UseCase.OFFICE, "📄 Office Work", "Documents, Browsing")
        ]
        
        self.usecase_var = tk.StringVar(value=UseCase.GAMING.value)
        
        for use_case, title, desc in use_cases:
            frame = ttk.Frame(usecase_frame)
            frame.pack(pady=5, anchor='w')
            
            ttk.Radiobutton(
                frame,
                text=f"{title} - {desc}",
                variable=self.usecase_var,
                value=use_case.value
            ).pack(anchor='w')
        
        ttk.Button(
            self.main_container,
            text="Analyze and Recommend",
            command=self.analyze_and_recommend
        ).pack(pady=20)
    
    def analyze_and_recommend(self):
        """Perform analysis and generate recommendations"""
        # Get use case
        use_case_value = self.usecase_var.get()
        self.requirements['use_case'] = UseCase(use_case_value)
        self.inference_engine.add_fact("use_case", self.requirements['use_case'])
        
        # Fire inference rules
        fired_rules = self.inference_engine.fire_rules()
        
        # Select components
        self.selected_build = self._select_components()
        
        # Show results
        self.show_results_screen()
    
    def _select_components(self) -> Dict:
        """Select optimal components based on requirements"""
        budget = self.requirements['budget']
        use_case = self.requirements['use_case']
        selected = {}
        remaining = budget
        
        # Select CPU
        cpu_candidates = []
        for cpu in self.knowledge_base.components['cpu']:
            if cpu.price > budget * 0.5:
                continue
            rating = cpu.performance_rating.get(use_case, 5)
            score = rating + (rating / (cpu.price / 100))
            if self.inference_engine.facts.get('prioritize_cpu', False):
                score += 2
            cpu_candidates.append((cpu, score))
        
        if cpu_candidates:
            selected['cpu'] = max(cpu_candidates, key=lambda x: x[1])[0]
            remaining -= selected['cpu'].price
        
        # Select GPU
        gpu_candidates = []
        for gpu in self.knowledge_base.components['gpu']:
            if gpu.price > remaining * 0.7:
                continue
            rating = gpu.performance_rating.get(use_case, 5)
            score = rating + (rating / (gpu.price / 100))
            if self.inference_engine.facts.get('prioritize_gpu', False):
                score += 2
            min_vram = self.inference_engine.facts.get('min_vram', 0)
            if gpu.specs.get('vram', 0) >= min_vram:
                score += 1
            gpu_candidates.append((gpu, score))
        
        if gpu_candidates:
            selected['gpu'] = max(gpu_candidates, key=lambda x: x[1])[0]
            remaining -= selected['gpu'].price
        
        # Select Memory
        memory_candidates = []
        for mem in self.knowledge_base.components['memory']:
            if mem.price > remaining * 0.4:
                continue
            rating = mem.performance_rating.get(use_case, 5)
            min_mem = self.inference_engine.facts.get('min_memory', 16)
            score = rating
            if mem.specs.get('capacity', 0) >= min_mem:
                score += 2
            memory_candidates.append((mem, score))
        
        if memory_candidates:
            selected['memory'] = max(memory_candidates, key=lambda x: x[1])[0]
            remaining -= selected['memory'].price
        
        # Select Storage
        storage_candidates = []
        for stor in self.knowledge_base.components['storage']:
            if stor.price > remaining:
                continue
            rating = stor.performance_rating.get(use_case, 5)
            storage_candidates.append((stor, rating))
        
        if storage_candidates:
            selected['storage'] = max(storage_candidates, key=lambda x: x[1])[0]
        
        return selected
    
    def show_results_screen(self):
        """Display recommendation results"""
        self._clear_container()
        
        # Title
        ttk.Label(
            self.main_container,
            text="🏆 Expert System Recommendation",
            style='Header.TLabel'
        ).pack(pady=20)
        
        # Create scrollable frame
        canvas = tk.Canvas(self.main_container, bg='#1e1e1e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # System overview
        total_cost = sum(comp.price for comp in self.selected_build.values())
        budget = self.requirements['budget']
        
        overview_frame = ttk.Frame(scrollable_frame)
        overview_frame.pack(pady=10, padx=20, fill=tk.X)
        
        ttk.Label(overview_frame, text=f"Budget: ${budget:,.0f}", font=('Segoe UI', 11)).pack(anchor='w')
        ttk.Label(overview_frame, text=f"Total Cost: ${total_cost:,.0f}", font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        ttk.Label(overview_frame, text=f"Budget Utilization: {(total_cost/budget)*100:.1f}%", font=('Segoe UI', 11)).pack(anchor='w')
        
        # Components
        for category, component in self.selected_build.items():
            comp_frame = ttk.Frame(scrollable_frame)
            comp_frame.pack(pady=10, padx=20, fill=tk.X)
            
            ttk.Label(
                comp_frame,
                text=f"{category.upper()}: {component.name}",
                font=('Segoe UI', 12, 'bold')
            ).pack(anchor='w')
            
            ttk.Label(comp_frame, text=f"Price: ${component.price:,.0f}").pack(anchor='w', padx=20)
            
            rating = component.performance_rating.get(self.requirements['use_case'], 5)
            ttk.Label(comp_frame, text=f"Performance Rating: {rating}/10").pack(anchor='w', padx=20)
            
            # Specs
            for key, value in list(component.specs.items())[:3]:
                ttk.Label(comp_frame, text=f"{key}: {value}").pack(anchor='w', padx=40)
        
        # Recommendations
        rec_frame = ttk.Frame(scrollable_frame)
        rec_frame.pack(pady=20, padx=20, fill=tk.X)
        
        ttk.Label(rec_frame, text="💡 Recommendations", font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        
        recommendations = self._generate_recommendations(total_cost, budget)
        for rec in recommendations:
            ttk.Label(rec_frame, text=f"• {rec}", wraplength=700).pack(anchor='w', padx=20, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons
        button_frame = ttk.Frame(self.main_container)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Show Reasoning", command=self.show_reasoning).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Report", command=self.save_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="New Consultation", command=self.reset_consultation).pack(side=tk.LEFT, padx=5)
    
    def _generate_recommendations(self, total_cost, budget) -> List[str]:
        """Generate recommendations"""
        recs = []
        use_case = self.requirements['use_case']
        
        if total_cost > budget * 1.1:
            recs.append(f"Build exceeds budget by ${total_cost - budget:.0f}. Consider lower-tier components.")
        elif total_cost < budget * 0.8:
            recs.append(f"Budget underutilized by ${budget - total_cost:.0f}. Consider upgrades.")
        
        if use_case == UseCase.GAMING:
            recs.append("For gaming, consider a high refresh rate monitor (144Hz+)")
            recs.append("Ensure adequate cooling for sustained performance")
        elif use_case == UseCase.CONTENT_CREATION:
            recs.append("Consider additional storage for project files")
            recs.append("Multiple monitors recommended for productivity")
        elif use_case == UseCase.AI_ML:
            recs.append("GPU memory allows for medium to large model training")
            recs.append("Consider cloud computing for very large models")
        
        return recs
    
    def show_reasoning(self):
        """Show expert system reasoning"""
        reasoning_window = tk.Toplevel(self.root)
        reasoning_window.title("Expert System Reasoning")
        reasoning_window.geometry("600x400")
        reasoning_window.configure(bg='#1e1e1e')
        
        text_widget = scrolledtext.ScrolledText(
            reasoning_window,
            wrap=tk.WORD,
            bg='#2d2d2d',
            fg='#ffffff',
            font=('Consolas', 10)
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget.insert(tk.END, "🧠 EXPERT SYSTEM REASONING TRACE\n")
        text_widget.insert(tk.END, "="*50 + "\n\n")
        
        for trace in self.inference_engine.explanation_trace:
            text_widget.insert(tk.END, f"{trace}\n")
        
        text_widget.insert(tk.END, "\n" + "="*50 + "\n")
        text_widget.insert(tk.END, f"\nFacts in Knowledge Base:\n")
        for fact, value in self.inference_engine.facts.items():
            text_widget.insert(tk.END, f"  • {fact}: {value}\n")
        
        text_widget.config(state=tk.DISABLED)
    
    def save_report(self):
        """Save consultation report"""
        filename = f"hardware_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w') as f:
            f.write("IT HARDWARE EXPERT SYSTEM REPORT\n")
            f.write("="*50 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Budget: ${self.requirements['budget']:,.0f}\n")
            f.write(f"Use Case: {self.requirements['use_case'].value}\n\n")
            
            total = sum(comp.price for comp in self.selected_build.values())
            f.write(f"Total Cost: ${total:,.0f}\n\n")
            
            f.write("RECOMMENDED COMPONENTS:\n")
            for category, component in self.selected_build.items():
                f.write(f"\n{category.upper()}: {component.name} - ${component.price:,.0f}\n")
                for key, value in component.specs.items():
                    f.write(f"  {key}: {value}\n")
        
        messagebox.showinfo("Success", f"Report saved to {filename}")
    
    def reset_consultation(self):
        """Reset and start new consultation"""
        self.inference_engine.reset()
        self.requirements.clear()
        self.selected_build.clear()
        self.show_welcome_screen()
    
    def _clear_container(self):
        """Clear main container"""
        for widget in self.main_container.winfo_children():
            widget.destroy()

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = ITHardwareExpertGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
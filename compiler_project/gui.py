import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys
import os

# Adjust path so we can import src nicely if executed directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.ai_tutor import AITutor
    HAS_BACKEND = True
except ImportError:
    HAS_BACKEND = False

class AIErrorTutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Error Tutor")
        self.root.geometry("900x600")
        self.root.configure(padx=20, pady=20)
        
        # Use a cleaner theme if available
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        
        # Header
        header_frame = ttk.Frame(root)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(header_frame, text="🧠 AI Compiler Error Tutor", font=("Helvetica", 24, "bold"))
        title_label.pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(header_frame, text="Initializing...", foreground="blue", font=("Helvetica", 10))
        self.status_label.pack(side=tk.RIGHT, anchor=tk.CENTER)

        # Main Layout (Left/Right split)
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- LEFT PANEL (Inputs) ---
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Language Selection
        ttk.Label(left_panel, text="Programming Language:", font=("Helvetica", 11, "bold")).pack(anchor=tk.W)
        self.lang_var = tk.StringVar(value="c")
        lang_frame = ttk.Frame(left_panel)
        lang_frame.pack(fill=tk.X, pady=(5, 15))
        ttk.Radiobutton(lang_frame, text="C/C++", variable=self.lang_var, value="c").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(lang_frame, text="Python", variable=self.lang_var, value="python").pack(side=tk.LEFT)
        
        # Error Input
        ttk.Label(left_panel, text="Compiler Error Message:", font=("Helvetica", 11, "bold")).pack(anchor=tk.W)
        self.error_text = tk.Text(left_panel, height=4, font=("Consolas", 10), relief=tk.SOLID, borderwidth=1)
        self.error_text.pack(fill=tk.X, pady=(5, 15))
        
        # Code Input
        ttk.Label(left_panel, text="Code Snippet / Context:", font=("Helvetica", 11, "bold")).pack(anchor=tk.W)
        self.code_text = tk.Text(left_panel, height=10, font=("Consolas", 10), relief=tk.SOLID, borderwidth=1)
        self.code_text.pack(fill=tk.BOTH, expand=True, pady=(5, 15))
        
        # Action Button
        self.analyze_btn = tk.Button(left_panel, text="🤖 Validate & Analyze Error", 
                                     bg="#2e8b57", fg="white", font=("Helvetica", 12, "bold"), 
                                     command=self.analyze_error, relief=tk.FLAT, cursor="hand2")
        self.analyze_btn.pack(fill=tk.X, ipady=5)
        
        # --- RIGHT PANEL (Outputs) ---
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        ttk.Label(right_panel, text="AI Educational Explanation:", font=("Helvetica", 11, "bold")).pack(anchor=tk.W)
        
        # The output text area with a nice background
        self.output_text = tk.Text(right_panel, font=("Helvetica", 12), wrap=tk.WORD, 
                                   bg="#f8f9fa", relief=tk.SOLID, borderwidth=1, padx=10, pady=10)
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.tutor = None
        
        if HAS_BACKEND:
            self.set_output("System is loading the T5-base AI Model...\nPlease wait.")
            threading.Thread(target=self.load_model, daemon=True).start()
        else:
            self.set_output("Warning: The 'src.ai_tutor' backend could not be imported.\n\nRunning in MOCK API Mode for UI demonstration.")
            self.status_label.config(text="Mock Mode Active", foreground="orange")

    def load_model(self):
        try:
            model_path = "models/fine_tuned_t5" if os.path.exists("models/fine_tuned_t5") else "t5-base"
            self.set_output(f"Loading {model_path} AI Model...\nPlease wait.")
            self.tutor = AITutor(model_name=model_path, device="cpu")
            msg = "✅ AI System Ready!\nUsing: " + ("Fine-Tuned Specialized Model" if "fine_tuned" in model_path else "Raw T5-Base (Untrained)")
            self.set_output(f"{msg}\n\nPaste your compiler error and source code to the left, then click analyze.")
            self.status_label.config(text="Model Loaded (Active)", foreground="green")
        except Exception as e:
            self.set_output(f"Failed to load AI Model:\n\n{str(e)}")
            self.status_label.config(text="Model Error", foreground="red")

    def set_output(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state=tk.DISABLED)

    def analyze_error(self):
        error_msg = self.error_text.get("1.0", tk.END).strip()
        code_ctx = self.code_text.get("1.0", tk.END).strip()
        lang = self.lang_var.get()
        
        if not error_msg or not code_ctx:
            messagebox.showwarning("Missing Input", "Please provide both the error message and the code context snippet.")
            return

        self.analyze_btn.config(state=tk.DISABLED, text="⏳ Analyzing in background...")
        self.set_output(f"Routing to T5 Transformer...\n\nLanguage: {lang.upper()}\n\nChecking Security Guards...")
        
        # Threading prevents the UI from freezing during inference (~2.8s)
        threading.Thread(target=self._run_inference, args=(error_msg, code_ctx, lang), daemon=True).start()

    def _run_inference(self, error_msg, code_ctx, lang):
        if self.tutor:
            try:
                explanation = self.tutor.explain_error(
                    error_message=error_msg,
                    code_context=code_ctx,
                    language=lang,
                    educational_level="beginner"
                )
                
                # Check if it returns a dictionary or raw string format based on src.ai_tutor implementation
                if isinstance(explanation, dict) and 'explanation' in explanation:
                    result_text = explanation['explanation']
                else:
                    result_text = str(explanation)
                    
                self.set_output(f"✅ AI Explanation:\n\n{result_text}")
                
            except Exception as e:
                self.set_output(f"❌ Inference Error Occurred:\n\n{str(e)}")
        else:
            import time
            time.sleep(1.5)  # Simulate model latency processing
            mock_res_text = (
                f"✅ Mock AI Analysis Complete\n\n"
                f"Detected Language: {lang.upper()}\n\n"
                f"The issue relates to this error:\n\"{error_msg}\"\n\n"
                f"Suggested Fix: Verify your syntax near the provided source code context. Ensure loops or function scopes are properly closed.\n\n"
                f"(*Note: Real model not loaded, this is a demonstration response.*)"
            )
            self.set_output(mock_res_text)
            
        self.analyze_btn.config(state=tk.NORMAL, text="🤖 Validate & Analyze Error")

if __name__ == "__main__":
    root = tk.Tk()
    app = AIErrorTutorApp(root)
    root.mainloop()

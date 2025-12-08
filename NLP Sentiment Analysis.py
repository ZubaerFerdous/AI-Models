# %%
import os
import time
import threading
import queue
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from textblob import TextBlob
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# Core processing functions
# -------------------------
def analyze_textblob_row(text):
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"
    return polarity, subjectivity, label

def process_feedback_df(df, feedback_col=None, true_label_col=None):
    # Identify feedback column if not passed
    if feedback_col is None:
        possible_columns = [c for c in df.columns if "feedback" in c.lower() or "comment" in c.lower() or "review" in c.lower()]
        if possible_columns:
            feedback_col = possible_columns[0]
        else:
            # fallback: assume first text column
            feedback_col = df.columns[0]
    # Identify true label column if present
    if true_label_col is None:
        possible_labels = [c for c in df.columns if "sentiment" in c.lower() or "label" in c.lower() or "true" in c.lower()]
        true_label_col = possible_labels[0] if possible_labels else None

    # Run TextBlob analysis
    results = df[feedback_col].apply(lambda t: pd.Series(analyze_textblob_row(t), index=["Polarity", "Subjectivity", "PredictedSentiment"]))
    out = pd.concat([df.reset_index(drop=True), results.reset_index(drop=True)], axis=1)
    if true_label_col and true_label_col in out.columns:
        out = out.rename(columns={true_label_col: "TrueSentiment"})
    else:
        out["TrueSentiment"] = None
    return out, feedback_col

def evaluate_and_metrics(out_df):
    metrics = {}
    if out_df["TrueSentiment"].notnull().any():
        # ensure labels are among expected three classes
        labels = ["Positive", "Neutral", "Negative"]
        try:
            cm = confusion_matrix(out_df["TrueSentiment"], out_df["PredictedSentiment"], labels=labels)
            acc = accuracy_score(out_df["TrueSentiment"], out_df["PredictedSentiment"])
            recall_vals = recall_score(out_df["TrueSentiment"], out_df["PredictedSentiment"], labels=labels, average=None)
            metrics["cm"] = cm
            metrics["labels"] = labels
            metrics["accuracy"] = acc
            metrics["recall"] = dict(zip(labels, recall_vals))
        except Exception as e:
            metrics["error"] = f"Evaluation error: {e}"
    else:
        metrics["cm"] = None
    return metrics

# -------------------------
# GUI class
# -------------------------
class FeedbackGUI:
    def __init__(self, root):
        self.root = root
        root.title("Student Feedback Sentiment System (GUI + Semi-Auto Watch)")
        root.geometry("1100x700")

        # Top frame controls
        control_frame = ttk.Frame(root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)

        ttk.Button(control_frame, text="Open CSV", command=self.open_file).pack(side=tk.LEFT, padx=4)
        ttk.Button(control_frame, text="Generate Synthetic (1000)", command=self.generate_synthetic).pack(side=tk.LEFT, padx=4)

        ttk.Label(control_frame, text="Watch Folder:").pack(side=tk.LEFT, padx=(10,2))
        self.watch_var = tk.StringVar(value="")
        ttk.Entry(control_frame, textvariable=self.watch_var, width=40).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Browse...", command=self.browse_watch_folder).pack(side=tk.LEFT, padx=4)

        ttk.Label(control_frame, text="Interval (s):").pack(side=tk.LEFT, padx=(10,2))
        self.interval_var = tk.IntVar(value=10)
        ttk.Entry(control_frame, textvariable=self.interval_var, width=6).pack(side=tk.LEFT, padx=2)

        self.watch_toggle = tk.BooleanVar(value=False)
        self.watch_button = ttk.Button(control_frame, text="Start Watching", command=self.toggle_watch)
        self.watch_button.pack(side=tk.LEFT, padx=8)

        ttk.Button(control_frame, text="Refresh Display", command=self.redraw_plots).pack(side=tk.LEFT, padx=4)

        # Status frame
        status_frame = ttk.Frame(root)
        status_frame.pack(side=tk.TOP, fill=tk.X, padx=8)
        self.status_label = ttk.Label(status_frame, text="Status: Idle")
        self.status_label.pack(side=tk.LEFT)

        # Metrics frame
        metrics_frame = ttk.Frame(root)
        metrics_frame.pack(side=tk.TOP, fill=tk.X, padx=8, pady=(6,0))
        self.metrics_text = tk.Text(metrics_frame, height=4, width=140)
        self.metrics_text.pack(side=tk.LEFT, fill=tk.X)
        self.metrics_text.configure(state=tk.DISABLED)

        # Plot frame (matplotlib canvases)
        plot_frame = ttk.Frame(root)
        plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=6)

        self.fig_cm, self.ax_cm = plt.subplots(figsize=(5,4))
        self.fig_scatter, self.ax_scatter = plt.subplots(figsize=(5,4))

        self.canvas_cm = FigureCanvasTkAgg(self.fig_cm, master=plot_frame)
        self.canvas_cm.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_scatter = FigureCanvasTkAgg(self.fig_scatter, master=plot_frame)
        self.canvas_scatter.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Internal state
        self.df = None
        self.last_processed_files = set()
        self.watch_job_id = None
        self.processing_queue = queue.Queue()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start a small thread to handle results from background processing if needed
        self.result_polling()

    # -------- GUI actions --------
    def open_file(self):
        fp = filedialog.askopenfilename(title="Open CSV file", filetypes=[("CSV files","*.csv"),("All files","*.*")])
        if not fp:
            return
        try:
            df = pd.read_csv(fp)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read CSV:\n{e}")
            return
        self.status_update(f"Loaded file: {os.path.basename(fp)} ({len(df)} rows)")
        self.process_and_display(df, source_path=fp)

    def generate_synthetic(self):
        # Simple synthetic generator similar to earlier code but small for demo
        positive_comments = [
            "The course was very informative and engaging.",
            "Excellent course structure with practical examples.",
            "The instructor was very passionate and knowledgeable.",
            "Assignments were fair and helpful for understanding the topics.",
            "The professor explained the material clearly."
        ]
        neutral_comments = [
            "The course was fine, nothing exceptional.",
            "It covered what was expected.",
            "The instructor was okay but not great.",
            "Assignments were manageable but not exciting.",
            "The course met my expectations but didn’t exceed them."
        ]
        negative_comments = [
            "The lectures were boring and unorganized.",
            "I found the material confusing and difficult.",
            "The professor did not explain the concepts clearly.",
            "Too much workload and unclear grading.",
            "Assignments were overwhelming and unfair."
        ]
        data = []
        for _ in range(1000):
            t = pd.np.random.choice(["Positive","Neutral","Negative"])  # using pd.np for compatibility
            if t == "Positive":
                text = pd.np.random.choice(positive_comments)
            elif t == "Neutral":
                text = pd.np.random.choice(neutral_comments)
            else:
                text = pd.np.random.choice(negative_comments)
            data.append({"Feedback": text, "TrueSentiment": t})
        df = pd.DataFrame(data)
        self.status_update("Generated synthetic dataset (1000 rows)")
        self.process_and_display(df, source_path=None)

    def browse_watch_folder(self):
        d = filedialog.askdirectory(title="Select folder to watch for CSV files")
        if d:
            self.watch_var.set(d)

    def toggle_watch(self):
        if self.watch_toggle.get():
            # currently running -> stop
            self.watch_toggle.set(False)
            self.watch_button.config(text="Start Watching")
            self.status_update("Stopped watching folder.")
            if self.watch_job_id:
                self.root.after_cancel(self.watch_job_id)
                self.watch_job_id = None
        else:
            folder = self.watch_var.get().strip()
            if not folder or not os.path.isdir(folder):
                messagebox.showwarning("Watch Folder", "Please choose a valid folder to watch first.")
                return
            self.watch_toggle.set(True)
            self.watch_button.config(text="Stop Watching")
            self.status_update(f"Watching folder: {folder}")
            # seed existing files so they aren't reprocessed immediately
            self.last_processed_files = set(os.listdir(folder))
            self.schedule_watch()

    def schedule_watch(self):
        interval = max(1, int(self.interval_var.get()))
        self.watch_job_id = self.root.after(interval * 1000, self.watch_folder_once)

    def watch_folder_once(self):
        folder = self.watch_var.get().strip()
        if not folder or not os.path.isdir(folder) or not self.watch_toggle.get():
            self.status_update("Watch folder disabled or invalid.")
            return
        try:
            current = set(os.listdir(folder))
            newfiles = [f for f in current - self.last_processed_files if f.lower().endswith(".csv")]
            if newfiles:
                for nf in newfiles:
                    fp = os.path.join(folder, nf)
                    self.status_update(f"Detected new CSV: {nf} — processing...")
                    try:
                        df = pd.read_csv(fp)
                        # Process in main thread (fast). If heavy, could be moved to thread and communicate via queue.
                        self.process_and_display(df, source_path=fp)
                    except Exception as e:
                        self.status_update(f"Failed to read {nf}: {e}")
                    self.last_processed_files.add(nf)
            else:
                self.status_update(f"No new CSVs in {folder} (checked at {time.strftime('%H:%M:%S')})")
        except Exception as e:
            self.status_update(f"Watch error: {e}")
        # schedule next check
        if self.watch_toggle.get():
            self.schedule_watch()

    # -------- Processing & UI update --------
    def process_and_display(self, df, source_path=None):
        try:
            out_df, feedback_col = process_feedback_df(df.copy())
            # Save out
            if source_path:
                base = os.path.splitext(os.path.basename(source_path))[0]
                out_path = os.path.join(os.path.dirname(source_path), f"{base}_analyzed.csv")
            else:
                out_path = os.path.abspath("generated_feedback_analyzed.csv")
            out_df.to_csv(out_path, index=False)
            self.df = out_df
            self.status_update(f"Processed and saved: {os.path.basename(out_path)} ({len(out_df)} rows)")
            # update metrics text and plots
            metrics = evaluate_and_metrics(out_df)
            self.update_metrics_display(metrics)
            self.redraw_plots()
        except Exception as e:
            self.status_update(f"Processing failed: {e}")

    def update_metrics_display(self, metrics):
        self.metrics_text.configure(state=tk.NORMAL)
        self.metrics_text.delete("1.0", tk.END)
        if metrics.get("cm") is None:
            self.metrics_text.insert(tk.END, "No TrueSentiment labels found in dataset — skipping accuracy/recall.\n")
        elif metrics.get("error"):
            self.metrics_text.insert(tk.END, f"Evaluation error: {metrics['error']}\n")
        else:
            acc = metrics.get("accuracy", None)
            if acc is not None:
                self.metrics_text.insert(tk.END, f"Overall Accuracy: {acc:.3f}\n")
            recall = metrics.get("recall", {})
            if recall:
                for k, v in recall.items():
                    self.metrics_text.insert(tk.END, f"Recall ({k}): {v:.3f}\n")
            self.metrics_text.insert(tk.END, "\nConfusion Matrix:\n")
            cm = metrics["cm"]
            labels = metrics["labels"]
            dfcm = pd.DataFrame(cm, index=labels, columns=labels)
            self.metrics_text.insert(tk.END, dfcm.to_string())
            self.metrics_text.insert(tk.END, "\n")
        self.metrics_text.configure(state=tk.DISABLED)

    def redraw_plots(self):
        # Clear previous plots
        self.ax_cm.clear()
        self.ax_scatter.clear()

        if self.df is None:
            self.ax_cm.text(0.5,0.5,"No data loaded",ha="center")
            self.ax_scatter.text(0.5,0.5,"No data loaded",ha="center")
            self.canvas_cm.draw()
            self.canvas_scatter.draw()
            return

        # Confusion matrix if TrueSentiment exists
        if self.df["TrueSentiment"].notnull().any():
            labels = ["Positive","Neutral","Negative"]
            try:
                cm = confusion_matrix(self.df["TrueSentiment"], self.df["PredictedSentiment"], labels=labels)
                sns.heatmap(cm, annot=True, fmt='d', ax=self.ax_cm, cmap="Blues", xticklabels=labels, yticklabels=labels)
                self.ax_cm.set_xlabel("Predicted")
                self.ax_cm.set_ylabel("True")
                self.ax_cm.set_title("Confusion Matrix")
            except Exception as e:
                self.ax_cm.text(0.5,0.5,f"Unable to compute confusion matrix:\n{e}", ha="center")
        else:
            self.ax_cm.text(0.5,0.5,"No TrueSentiment labels for confusion matrix", ha="center")
        # Scatter plot: Polarity vs Subjectivity for Positive/Negative
        posneg = self.df[self.df["PredictedSentiment"].isin(["Positive","Negative"])]
        if not posneg.empty:
            sns.scatterplot(data=posneg, x="Polarity", y="Subjectivity", hue="PredictedSentiment", ax=self.ax_scatter, alpha=0.7)
            self.ax_scatter.set_xlim(-1.05, 1.05)
            self.ax_scatter.set_ylim(-0.05, 1.05)
            self.ax_scatter.set_title("Polarity vs Subjectivity (Predicted Positive/Negative)")
        else:
            self.ax_scatter.text(0.5,0.5,"No Positive/Negative predictions to plot", ha="center")

        self.fig_cm.tight_layout()
        self.fig_scatter.tight_layout()
        self.canvas_cm.draw()
        self.canvas_scatter.draw()

    def status_update(self, text):
        self.status_label.config(text=f"Status: {text}")
        print("[STATUS]", text)

    def result_polling(self):
        # placeholder for future background thread results handling
        self.root.after(1000, self.result_polling)

    def on_close(self):
        # cancel any scheduled watches
        if self.watch_job_id:
            try:
                self.root.after_cancel(self.watch_job_id)
            except:
                pass
        self.root.destroy()

# -------------------------
# Run the GUI
# -------------------------
def main():
    root = tk.Tk()
    app = FeedbackGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# %%




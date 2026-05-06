"""
Enhanced GUI - can search with just ONE identifier
"""
import customtkinter as ctk
import threading
from datetime import datetime
from core.osint_functions import search_all_platforms, download_instagram_posts
from database.history import save_search_result, get_search_history

class OSINTGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OSINT Pro Tool")
        self.geometry("800x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title = ctk.CTkLabel(self, text="🔍 OSINT Pro Tool", font=("Arial", 24, "bold"))
        title.grid(row=0, column=0, columnspan=3, padx=20, pady=(20,10), sticky="w")
        
        # Input Section
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        
        # Single input field - can be username, phone, or name
        ctk.CTkLabel(input_frame, text="Enter Username, Phone, or Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry = ctk.CTkEntry(input_frame, placeholder_text="e.g. @username, +98912..., John Doe", width=400)
        self.entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Auto-detect button
        detect_btn = ctk.CTkButton(input_frame, text="🔍 Auto Detect Type", command=self.auto_detect_type, width=120)
        detect_btn.grid(row=0, column=2, padx=10, pady=5)
        
        # Show detected type
        self.type_label = ctk.CTkLabel(input_frame, text="Type: Not detected", text_color="gray")
        self.type_label.grid(row=1, column=1, padx=10, pady=(0,10), sticky="w")
        
        # Platform Selection
        platform_frame = ctk.CTkFrame(self)
        platform_frame.grid(row=2, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(platform_frame, text="Select Platforms:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.platform_vars = {
            "telegram": ctk.BooleanVar(value=True),
            "instagram": ctk.BooleanVar(value=True),
            "soroush": ctk.BooleanVar(value=False),
            "bale": ctk.BooleanVar(value=False),
            "rubika": ctk.BooleanVar(value=False)
        }
        
        # Create checkboxes in two columns
        row = 1
        col = 0
        for i, (platform, var) in enumerate(self.platform_vars.items()):
            cb = ctk.CTkCheckBox(platform_frame, text=platform.capitalize(), variable=var)
            cb.grid(row=row, column=col, padx=10, pady=3, sticky="w")
            
            if i % 3 == 2:  # 3 items per column
                row += 1
                col = 0
            else:
                col += 1
        
        # Options
        options_frame = ctk.CTkFrame(self)
        options_frame.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        
        # Download Instagram posts
        self.download_var = ctk.BooleanVar(value=False)
        download_cb = ctk.CTkCheckBox(options_frame, text="Download Instagram Media (if public)", 
                                     variable=self.download_var)
        download_cb.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # Save to database
        self.save_var = ctk.BooleanVar(value=True)
        save_cb = ctk.CTkCheckBox(options_frame, text="Save to Search History", 
                                 variable=self.save_var)
        save_cb.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Action Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        
        self.search_btn = ctk.CTkButton(button_frame, text="🚀 Search All Platforms", 
                                       command=self.start_search, width=200, height=40)
        self.search_btn.grid(row=0, column=0, padx=10, pady=5)
        
        history_btn = ctk.CTkButton(button_frame, text="📜 View History", 
                                   command=self.show_history, width=120)
        history_btn.grid(row=0, column=1, padx=10, pady=5)
        
        clear_btn = ctk.CTkButton(button_frame, text="🗑️ Clear Results", 
                                 command=self.clear_results, width=120)
        clear_btn.grid(row=0, column=2, padx=10, pady=5)
        
        # Results Area
        ctk.CTkLabel(self, text="Results:", font=("Arial", 14, "bold")).grid(
            row=5, column=0, padx=20, pady=(20,5), sticky="w")
        
        # Use Textbox for better formatting
        self.results_text = ctk.CTkTextbox(self, width=760, height=400, 
                                          wrap="word", font=("Consolas", 12))
        self.results_text.grid(row=6, column=0, columnspan=3, padx=20, pady=(0,20), sticky="nsew")
        
        # Status bar
        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.status_label.grid(row=7, column=0, columnspan=3, padx=20, pady=(0,10), sticky="w")
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)
    
    def auto_detect_type(self):
        """Detect if input is username, phone, or name"""
        text = self.entry.get().strip()
        
        if not text:
            self.type_label.configure(text="Type: Empty", text_color="gray")
            return
        
        if text.startswith("+") or (text.replace(" ", "").isdigit() and len(text.replace(" ", "")) > 8):
            self.type_label.configure(text="Type: 📞 Phone Number", text_color="green")
        elif text.startswith("@") or (" " not in text and "." in text):
            self.type_label.configure(text="Type: 👤 Username", text_color="blue")
        else:
            self.type_label.configure(text="Type: 📛 Name", text_color="orange")
    
    def start_search(self):
        identifier = self.entry.get().strip()
        if not identifier:
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", "⚠️ Please enter something to search!")
            return
        
        # Get selected platforms
        platforms = [p for p, var in self.platform_vars.items() if var.get()]
        if not platforms:
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", "⚠️ Please select at least one platform!")
            return
        
        self.search_btn.configure(state="disabled", text="Searching...")
        self.status_label.configure(text=f"Searching '{identifier}' on {len(platforms)} platforms...")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", f"🔍 Searching: {identifier}\n{'='*50}\n\n")
        
        threading.Thread(target=self.run_search, args=(identifier, platforms), daemon=True).start()
    
    def run_search(self, identifier, platforms):
        from core.osint_functions import search_all_platforms
        
        # Run search
        results = search_all_platforms(identifier, platforms, identifier_type="auto")
        
        # Process results
        success_count = 0
        output_lines = []
        
        for result in results:
            output_lines.append(result["message"])
            if result["success"]:
                success_count += 1
            
            # Save to database if enabled
            if self.save_var.get():
                from database.history import save_search_result
                save_search_result(result)
            
            # Download Instagram posts if requested and successful
            if (result["success"] and result.get("data", {}).get("platform") == "instagram" 
                and self.download_var.get()):
                from core.osint_functions import download_instagram_posts
                download_result = download_instagram_posts(identifier)
                output_lines.append(f"   {download_result['message']}")
        
        # Update GUI
        self.after(0, self.display_results, results, output_lines, success_count)
    
    def display_results(self, results, output_lines, success_count):
        # Clear and display
        self.results_text.delete("1.0", "end")
        
        summary = f"📊 Search Complete: {success_count}/{len(results)} platforms found\n{'='*50}\n\n"
        self.results_text.insert("1.0", summary + "\n".join(output_lines))
        
        # Update status
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_label.configure(text=f"✅ Done at {timestamp} | Found: {success_count}")
        self.search_btn.configure(state="normal", text="🚀 Search All Platforms")
    
    def show_history(self):
        """Display search history"""
        from database.history import get_search_history
        
        history = get_search_history(limit=20)
        
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", "📜 Recent Searches:\n" + "="*50 + "\n\n")
        
        if not history:
            self.results_text.insert("end", "No search history yet.\n")
            return
        
        for record in history:
            timestamp = record[1]
            identifier = record[2]
            platform = record[3]
            success = "✅" if record[4] else "❌"
            message = record[5]
            
            self.results_text.insert("end", f"• {timestamp} | {identifier} | {platform} {success}\n")
            self.results_text.insert("end", f"  {message}\n\n")
    
    def clear_results(self):
        self.results_text.delete("1.0", "end")
        self.status_label.configure(text="Ready")

if __name__ == "__main__":
    app = OSINTGUI()
    app.mainloop()

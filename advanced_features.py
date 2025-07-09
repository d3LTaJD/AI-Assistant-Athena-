"""
Advanced Features: Image Generation, Code Generation, and Automated Tasks
"""
import os
import time
import threading
import json
from datetime import datetime, timedelta
from pathlib import Path

class AdvancedFeatures:
    def __init__(self, voice_handler, config):
        self.voice_handler = voice_handler
        self.config = config
        self.scheduled_tasks = []
        self.screenshot_timer = None
        self.is_taking_screenshots = False
        
    def handle_scheduled_screenshots(self, command):
        """Handle automated screenshot commands"""
        try:
            # Parse command: "take screenshot every X minutes/seconds and save to Y drive/folder"
            words = command.lower().split()
            
            # Extract interval
            interval_minutes = 2  # default
            save_location = "Screenshots"  # default
            
            if "every" in words:
                every_idx = words.index("every")
                if every_idx + 1 < len(words):
                    try:
                        interval_minutes = int(words[every_idx + 1])
                    except ValueError:
                        pass
            
            # Extract save location
            if "save to" in command:
                save_part = command.split("save to")[1].strip()
                if "drive" in save_part or ":" in save_part:
                    drive_letter = save_part.split()[0].upper()
                    # Handle both "D drive" and "D:" formats
                    if ":" in drive_letter:
                        save_location = f"{drive_letter}\\Screenshots"
                    else:
                        save_location = f"{drive_letter}:\\Screenshots"
                else:
                    save_location = save_part
            
            # Start automated screenshots
            self.start_automated_screenshots(interval_minutes, save_location)
            
            return f"✅ Started taking screenshots every {interval_minutes} minutes, saving to {save_location}"
            
        except Exception as e:
            return f"❌ Error setting up automated screenshots: {str(e)}"
    
    def start_automated_screenshots(self, interval_minutes, save_location):
        """Start automated screenshot capture"""
        if self.is_taking_screenshots:
            result = self.stop_automated_screenshots()
            self.voice_handler.speak(result)
        
        self.is_taking_screenshots = True
        
        # Create save directory
        Path(save_location).mkdir(parents=True, exist_ok=True)
        
        def screenshot_loop():
            count = 0
            while self.is_taking_screenshots:
                try:
                    # Take screenshot
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = Path(save_location) / f"auto_screenshot_{timestamp}.png"

                    try:
                        import pyautogui
                        screenshot = pyautogui.screenshot()
                        screenshot.save(filename)
                        count += 1
                        self.voice_handler.speak(f"Screenshot {count} saved to {save_location}")
                    except ImportError:
                        # Fallback for environments without pyautogui
                        print(f"Screenshot simulation: Would save to {filename}")
                        count += 1
                        self.voice_handler.speak(f"Screenshot {count} simulated")
                    
                    # Wait for next interval
                    time.sleep(interval_minutes * 60)
                    
                except Exception as e:
                    print(f"Screenshot error: {e}")
                    time.sleep(10)  # Wait before retrying
        
        # Start in background thread
        self.screenshot_thread = threading.Thread(target=screenshot_loop, daemon=True)
        self.screenshot_thread.start()
    
    def stop_automated_screenshots(self):
        """Stop automated screenshot capture"""
        self.is_taking_screenshots = False
        return "🛑 Stopped automated screenshots"
    
    def generate_image(self, prompt):
        """Generate AI image from text prompt"""
        try:
            # Check if we have OpenAI API access
            try:
                import openai
                have_openai = True
            except ImportError:
                have_openai = False
            
            self.voice_handler.speak("Generating your image, please wait...")
            
            if have_openai and 'openai' in sys.modules:
                try:
                    # Try to use actual OpenAI API if available
                    api_key = self.config.get_secure("api_keys.openai") if hasattr(self.config, "get_secure") else None
                    
                    if api_key:
                        openai.api_key = api_key
                        response = openai.Image.create(
                            prompt=prompt,
                            n=1,
                            size="1024x1024"
                        )
                        image_url = response["data"][0]["url"]
                        return f"""🎨 Image Generated Successfully!

Prompt: "{prompt}"
View your image at: {image_url}

Would you like me to:
1. Open the image in your browser
2. Generate a different image
3. Save the image to your computer"""
                    
                except Exception as e:
                    print(f"OpenAI API error: {e}")
            
            # Fallback to simulation if OpenAI not available
            # Simulate API call delay
            time.sleep(2)
            
            # Create a placeholder response
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"generated_image_{timestamp}.png"
            
            # Simulate image generation
            response = f"""🎨 Image Generation Simulated!

Prompt: "{prompt}"
Simulated File: {image_filename}
Resolution: 1024x1024
Style: Photorealistic

In a full installation with API keys configured, 
a real image would be generated based on your prompt.

Would you like me to:
1. Set up image generation with OpenAI
2. Try a different prompt
3. Learn more about image generation"""
            
            return response
            
        except Exception as e:
            return f"❌ Image generation error: {str(e)}"
    
    def generate_code(self, request):
        """Generate programming code based on request"""
        try:
            # Check if we have OpenAI API access for better code generation
            try:
                import openai
                have_openai = True
            except ImportError:
                have_openai = False
            
            language = self.detect_programming_language(request)
            task = self.extract_programming_task(request)

            self.voice_handler.speak(f"Generating {language} code for {task}")

            # Try to use OpenAI for code generation if available
            if have_openai and 'openai' in sys.modules:
                try:
                    api_key = self.config.get_secure("api_keys.openai") if hasattr(self.config, "get_secure") else None
                    
                    if api_key:
                        openai.api_key = api_key
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": f"You are a helpful assistant that generates {language} code."},
                                {"role": "user", "content": f"Write {language} code for {task}. Provide only the code with brief comments."}
                            ]
                        )
                        
                        generated_code = response["choices"][0]["message"]["content"]
                        
                        # Save to file
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"generated_code_{timestamp}.{self.get_file_extension(language)}"
                        
                        # Save to Documents/Generated_Code folder
                        code_dir = Path.home() / "Documents" / "Generated_Code"
                        code_dir.mkdir(parents=True, exist_ok=True)
                        
                        file_path = code_dir / filename
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(generated_code)
                        
                        return f"""💻 Code Generated with AI!

Language: {language.title()}
Task: {task}
File: {filename}
Location: {file_path}

The code has been saved and is ready to use!
Would you like me to:
1. Open the file in your default editor
2. Explain how the code works
3. Generate additional examples?"""
                except Exception as e:
                    print(f"OpenAI API error: {e}")
            
            # Code generation templates
            code_templates = {
                "python": {
                    "sort list": '''def sort_list(items, reverse=False):
    """
    Sort a list of items
    
    Args:
        items: List to sort
        reverse: Sort in descending order if True
    
    Returns:
        Sorted list
    """
    return sorted(items, reverse=reverse)

# Example usage:
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = sort_list(numbers)
print(f"Sorted: {sorted_numbers}")''',
                    
                    "todo app": '''class TodoApp:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, task):
        """Add a new task"""
        self.tasks.append({
            'id': len(self.tasks) + 1,
            'task': task,
            'completed': False,
            'created': datetime.now()
        })
        print(f"Task added: {task}")
    
    def complete_task(self, task_id):
        """Mark task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                print(f"Task {task_id} completed!")
                return
        print("Task not found")
    
    def list_tasks(self):
        """List all tasks"""
        for task in self.tasks:
            status = "✅" if task['completed'] else "⏳"
            print(f"{status} {task['id']}: {task['task']}")

# Example usage:
todo = TodoApp()
todo.add_task("Learn Python")
todo.add_task("Build AI assistant")
todo.list_tasks()''',
                },
                
                "javascript": {
                    "todo app": '''class TodoApp {
    constructor() {
        this.tasks = [];
        this.nextId = 1;
    }
    
    addTask(taskText) {
        const task = {
            id: this.nextId++,
            text: taskText,
            completed: false,
            createdAt: new Date()
        };
        this.tasks.push(task);
        this.renderTasks();
    }
    
    toggleTask(id) {
        const task = this.tasks.find(t => t.id === id);
        if (task) {
            task.completed = !task.completed;
            this.renderTasks();
        }
    }
    
    deleteTask(id) {
        this.tasks = this.tasks.filter(t => t.id !== id);
        this.renderTasks();
    }
    
    renderTasks() {
        const container = document.getElementById('tasks');
        container.innerHTML = '';
        
        this.tasks.forEach(task => {
            const taskElement = document.createElement('div');
            taskElement.className = `task ${task.completed ? 'completed' : ''}`;
            taskElement.innerHTML = `
                <span>${task.text}</span>
                <button onclick="todo.toggleTask(${task.id})">
                    ${task.completed ? 'Undo' : 'Complete'}
                </button>
                <button onclick="todo.deleteTask(${task.id})">Delete</button>
            `;
            container.appendChild(taskElement);
        });
    }
}

// Initialize
const todo = new TodoApp();''',
                },
                
                "html": {
                    "contact form": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Form</title>
    <style>
        .contact-form {
            max-width: 600px;
            margin: 50px auto;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            font-family: Arial, sans-serif;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        
        input, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input:focus, textarea:focus {
            outline: none;
            border-color: #4CAF50;
        }
        
        button {
            background-color: #4CAF50;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <form class="contact-form" onsubmit="handleSubmit(event)">
        <h2>Contact Us</h2>
        
        <div class="form-group">
            <label for="name">Full Name *</label>
            <input type="text" id="name" name="name" required>
        </div>
        
        <div class="form-group">
            <label for="email">Email Address *</label>
            <input type="email" id="email" name="email" required>
        </div>
        
        <div class="form-group">
            <label for="phone">Phone Number</label>
            <input type="tel" id="phone" name="phone">
        </div>
        
        <div class="form-group">
            <label for="subject">Subject *</label>
            <input type="text" id="subject" name="subject" required>
        </div>
        
        <div class="form-group">
            <label for="message">Message *</label>
            <textarea id="message" name="message" rows="5" required></textarea>
        </div>
        
        <button type="submit">Send Message</button>
    </form>
    
    <script>
        function handleSubmit(event) {
            event.preventDefault();
            
            // Get form data
            const formData = new FormData(event.target);
            const data = Object.fromEntries(formData.entries());
            
            // Here you would typically send to a server
            console.log('Form submitted:', data);
            alert('Thank you for your message! We will get back to you soon.');
            
            // Reset form
            event.target.reset();
        }
    </script>
</body>
</html>''',
                },
                
                "sql": {
                    "top customers": '''-- Find top 10 customers by total purchase amount
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order_value,
    MAX(o.order_date) as last_order_date
FROM 
    customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE 
    o.order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR)
    AND o.status = 'completed'
GROUP BY 
    c.customer_id, c.first_name, c.last_name, c.email
HAVING 
    total_spent > 1000
ORDER BY 
    total_spent DESC, total_orders DESC
LIMIT 10;

-- Alternative query for customer lifetime value
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
    c.email,
    DATEDIFF(CURRENT_DATE, MIN(o.order_date)) as days_as_customer,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(oi.quantity * oi.unit_price) as lifetime_value,
    SUM(oi.quantity * oi.unit_price) / COUNT(DISTINCT o.order_id) as avg_order_value
FROM 
    customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
WHERE 
    o.status IN ('completed', 'shipped')
GROUP BY 
    c.customer_id, c.first_name, c.last_name, c.email
ORDER BY 
    lifetime_value DESC
LIMIT 10;''',
                }
            }
            
            # Generate appropriate code
            code = self.get_code_template(language, task, code_templates)
            
            if code:
                # Save code to file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"generated_code_{timestamp}.{self.get_file_extension(language)}"
                
                # Save to Documents/Generated_Code folder
                code_dir = Path.home() / "Documents" / "Generated_Code"
                code_dir.mkdir(parents=True, exist_ok=True)
                
                file_path = code_dir / filename
                with open(file_path, 'w', encoding='utf-8') as f:
                    try:
                        f.write(code)
                    except Exception as write_error:
                        print(f"Error writing file: {write_error}")
                        # Create directory if it doesn't exist
                        code_dir.mkdir(parents=True, exist_ok=True)
                        # Try again
                        f.write(code)
                
                response = f"""💻 Code Generated Successfully!

Language: {language.title()}
Task: {task}
File: {filename}
Location: {file_path}

The code has been saved and is ready to use!
Would you like me to:
1. Open the file in your default editor
2. Explain how the code works
3. Generate additional examples?"""
                
                return response
            else:
                return f"❌ Sorry, I don't have a template for {language} {task} yet. But I can help you with:\n• Python: sorting, todo apps, data processing\n• JavaScript: web apps, DOM manipulation\n• HTML: forms, layouts, components\n• SQL: queries, database operations"
                
        except Exception as e:
            return f"❌ Code generation error: {str(e)}"
    
    def detect_programming_language(self, request):
        """Detect programming language from request"""
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['python', 'py', 'django', 'flask']):
            return 'python'
        elif any(word in request_lower for word in ['javascript', 'js', 'node', 'react', 'vue']):
            return 'javascript'
        elif any(word in request_lower for word in ['html', 'web page', 'website', 'form']):
            return 'html'
        elif any(word in request_lower for word in ['sql', 'database', 'query', 'mysql', 'postgres']):
            return 'sql'
        elif any(word in request_lower for word in ['java', 'spring']):
            return 'java'
        elif any(word in request_lower for word in ['c++', 'cpp']):
            return 'cpp'
        else:
            return 'python'  # default
    
    def extract_programming_task(self, request):
        """Extract the programming task from request"""
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['sort', 'sorting']):
            return 'sort list'
        elif any(word in request_lower for word in ['todo', 'task', 'reminder']):
            return 'todo app'
        elif any(word in request_lower for word in ['form', 'contact']):
            return 'contact form'
        elif any(word in request_lower for word in ['customer', 'top', 'best']):
            return 'top customers'
        elif any(word in request_lower for word in ['calculator', 'calculate']):
            return 'calculator'
        elif any(word in request_lower for word in ['game', 'tic tac toe']):
            return 'game'
        else:
            return 'general function'
    
    def get_code_template(self, language, task, templates):
        """Get appropriate code template"""
        if language in templates and task in templates[language]:
            return templates[language][task]
        return None
    
    def get_file_extension(self, language):
        """Get file extension for programming language"""
        extensions = {
            'python': 'py',
            'javascript': 'js',
            'html': 'html',
            'sql': 'sql',
            'java': 'java',
            'cpp': 'cpp',
            'css': 'css'
        }
        return extensions.get(language, 'txt')
    
    def handle_advanced_command(self, command):
        """Handle advanced feature commands"""
        command_lower = command.lower()

        # Import sys for OpenAI checks
        import sys
        
        # Screenshot automation
        if "screenshot every" in command_lower or "take screenshot every" in command_lower:
            return self.handle_scheduled_screenshots(command)
        elif "stop screenshot" in command_lower or "stop taking screenshot" in command_lower:
            return self.stop_automated_screenshots()
        
        # Image generation
        elif any(phrase in command_lower for phrase in ["generate image", "create image", "make image", "draw"]):
            prompt = command_lower.replace("generate image of", "").replace("create image of", "").replace("make image of", "").replace("draw", "").strip()
            return self.generate_image(prompt)
        
        # Code generation
        elif any(phrase in command_lower for phrase in ["write code", "generate code", "create function", "write program", "code for"]):
            return self.generate_code(command)
        
        # Advanced file operations
        elif "backup" in command_lower:
            return self.handle_backup_command(command)
        elif "sync" in command_lower:
            return self.handle_sync_command(command)
        
        return None
    
    def handle_backup_command(self, command):
        """Handle backup operations"""
        return "🔄 Backup feature coming soon! I'll help you backup your important files automatically."
    
    def handle_sync_command(self, command):
        """Handle file synchronization"""
        return "🔄 Sync feature coming soon! I'll help you sync files between different locations."
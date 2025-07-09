#!/usr/bin/env python3
"""
Complete Startup Platform Setup Script
This sets up the entire ecosystem for your startup platform
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class StartupPlatformSetup:
    def __init__(self):
        self.project_name = "startup-platform"
        self.base_dir = Path.cwd()
        self.errors = []
        self.warnings = []
        
    def create_project_structure(self):
        """Create the complete project directory structure"""
        print("📁 Creating project structure...")
        
        directories = [
            # Frontend
            "frontend/public",
            "frontend/src/components/Dashboard",
            "frontend/src/components/Website",
            "frontend/src/components/AppBuilder",
            "frontend/src/components/DataManagement",
            "frontend/src/components/AIModels",
            "frontend/src/components/Analytics",
            "frontend/src/pages",
            "frontend/src/services",
            "frontend/src/utils",
            "frontend/src/styles",
            
            # Backend
            "backend/api/auth",
            "backend/api/website",
            "backend/api/apps",
            "backend/api/data",
            "backend/api/ai",
            "backend/api/analytics",
            "backend/models",
            "backend/services",
            "backend/middleware",
            "backend/database",
            "backend/utils",
            
            # AI/ML Services
            "ai-services/models/nlp",
            "ai-services/models/computer-vision",
            "ai-services/models/recommendation",
            "ai-services/models/prediction",
            "ai-services/training",
            "ai-services/inference",
            "ai-services/data-processing",
            
            # Data Platform
            "data-platform/ingestion",
            "data-platform/processing",
            "data-platform/storage",
            "data-platform/analytics",
            "data-platform/visualization",
            
            # App Builder
            "app-builder/templates",
            "app-builder/components",
            "app-builder/builder-engine",
            "app-builder/deployment",
            "app-builder/marketplace",
            
            # Infrastructure
            "infrastructure/docker",
            "infrastructure/kubernetes",
            "infrastructure/terraform",
            "infrastructure/monitoring",
            
            # Documentation
            "docs/api",
            "docs/user-guide",
            "docs/developer",
            
            # Tests
            "tests/unit",
            "tests/integration",
            "tests/e2e",
            
            # Static files
            "static/css",
            "static/js",
            "static/images",
            "static/templates",
            
            # Uploads and data
            "uploads/datasets",
            "uploads/models",
            "uploads/media",
            
            # Logs
            "logs/app",
            "logs/ai",
            "logs/data",
        ]
        
        for directory in directories:
            dir_path = self.base_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create __init__.py for Python packages
            if any(part in directory for part in ['backend', 'ai-services', 'data-platform']):
                init_file = dir_path / "__init__.py"
                if not init_file.exists():
                    init_file.touch()
        
        print("✅ Project structure created successfully!")
        
    def create_configuration_files(self):
        """Create configuration files"""
        print("⚙️ Creating configuration files...")
        
        # Environment configuration
        env_content = """# Environment Configuration
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/startup_platform
REDIS_URL=redis://localhost:6379/0

# API Keys
OPENAI_API_KEY=your-openai-key
STRIPE_SECRET_KEY=your-stripe-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Cloud Storage
S3_BUCKET=your-s3-bucket
GCS_BUCKET=your-gcs-bucket

# Analytics
GOOGLE_ANALYTICS_ID=your-ga-id
MIXPANEL_TOKEN=your-mixpanel-token
"""
        
        with open(self.base_dir / ".env", "w") as f:
            f.write(env_content)
        
        # Docker configuration
        dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

COPY requirements_startup.txt .
RUN pip install -r requirements_startup.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "complete_startup_platform:app"]
"""
        
        with open(self.base_dir / "Dockerfile", "w") as f:
            f.write(dockerfile_content)
        
        # Docker Compose
        docker_compose_content = """version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/startup_platform
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: startup_platform
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery:
    build: .
    command: celery -A complete_startup_platform.celery worker --loglevel=info
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/startup_platform
      - REDIS_URL=redis://redis:6379/0

volumes:
  postgres_data:
"""
        
        with open(self.base_dir / "docker-compose.yml", "w") as f:
            f.write(docker_compose_content)
        
        # Package.json for frontend
        package_json_content = {
            "name": "startup-platform-frontend",
            "version": "1.0.0",
            "description": "Frontend for Startup Platform",
            "main": "index.js",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview",
                "test": "jest"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.15.0",
                "axios": "^1.5.0",
                "tailwindcss": "^3.3.0",
                "chart.js": "^4.4.0",
                "react-chartjs-2": "^5.2.0",
                "socket.io-client": "^4.7.2",
                "react-hook-form": "^7.45.4",
                "react-query": "^3.39.3"
            },
            "devDependencies": {
                "@vitejs/plugin-react": "^4.0.4",
                "vite": "^4.4.9",
                "jest": "^29.6.4",
                "@testing-library/react": "^13.4.0"
            }
        }
        
        frontend_dir = self.base_dir / "frontend"
        with open(frontend_dir / "package.json", "w") as f:
            json.dump(package_json_content, f, indent=2)
        
        print("✅ Configuration files created!")
    
    def install_python_dependencies(self):
        """Install Python dependencies"""
        print("📦 Installing Python dependencies...")
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements_startup.txt"
            ])
            print("✅ Python dependencies installed!")
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Failed to install Python dependencies: {e}")
    
    def install_frontend_dependencies(self):
        """Install frontend dependencies"""
        print("📦 Installing frontend dependencies...")
        
        frontend_dir = self.base_dir / "frontend"
        
        try:
            subprocess.check_call(["npm", "install"], cwd=frontend_dir)
            print("✅ Frontend dependencies installed!")
        except subprocess.CalledProcessError as e:
            self.warnings.append(f"Failed to install frontend dependencies: {e}")
            print("⚠️ Frontend dependencies failed - you can install them later with 'npm install' in the frontend directory")
    
    def create_sample_templates(self):
        """Create sample HTML templates"""
        print("🎨 Creating sample templates...")
        
        templates_dir = self.base_dir / "templates"
        templates_dir.mkdir(exist_ok=True)
        
        # Base template
        base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Startup Platform{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gray-100">
    <nav class="bg-blue-600 text-white p-4">
        <div class="container mx-auto flex justify-between items-center">
            <h1 class="text-xl font-bold">Startup Platform</h1>
            <div class="space-x-4">
                {% if current_user.is_authenticated %}
                    <a href="/dashboard" class="hover:underline">Dashboard</a>
                    <a href="/websites" class="hover:underline">Websites</a>
                    <a href="/apps" class="hover:underline">Apps</a>
                    <a href="/data" class="hover:underline">Data</a>
                    <a href="/ai" class="hover:underline">AI/ML</a>
                    <a href="/logout" class="hover:underline">Logout</a>
                {% else %}
                    <a href="/login" class="hover:underline">Login</a>
                    <a href="/register" class="hover:underline">Register</a>
                {% endif %}
            </div>
        </div>
    </nav>
    
    <main class="container mx-auto mt-8 px-4">
        {% block content %}{% endblock %}
    </main>
    
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>"""
        
        with open(templates_dir / "base.html", "w") as f:
            f.write(base_template)
        
        # Dashboard template
        dashboard_template = """{% extends "base.html" %}

{% block title %}Dashboard - Startup Platform{% endblock %}

{% block content %}
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
    <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold text-gray-700">Websites</h3>
        <p class="text-3xl font-bold text-blue-600">{{ stats.websites }}</p>
    </div>
    <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold text-gray-700">Apps</h3>
        <p class="text-3xl font-bold text-green-600">{{ stats.apps }}</p>
    </div>
    <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold text-gray-700">Datasets</h3>
        <p class="text-3xl font-bold text-purple-600">{{ stats.datasets }}</p>
    </div>
    <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold text-gray-700">AI Models</h3>
        <p class="text-3xl font-bold text-red-600">{{ stats.models }}</p>
    </div>
</div>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold mb-4">Quick Actions</h3>
        <div class="space-y-2">
            <a href="/websites/create" class="block bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Create Website</a>
            <a href="/apps/create" class="block bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">Build App</a>
            <a href="/data/upload" class="block bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600">Upload Data</a>
            <a href="/ai/create" class="block bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">Train AI Model</a>
        </div>
    </div>
    
    <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold mb-4">Recent Activity</h3>
        <div class="space-y-2 text-sm text-gray-600">
            <p>• Website "My Business" created</p>
            <p>• Dataset "customer_data.csv" uploaded</p>
            <p>• AI Model "sales_predictor" trained</p>
            <p>• App "Mobile Store" deployed</p>
        </div>
    </div>
</div>
{% endblock %}"""
        
        with open(templates_dir / "dashboard.html", "w") as f:
            f.write(dashboard_template)
        
        print("✅ Sample templates created!")
    
    def create_static_files(self):
        """Create static CSS and JS files"""
        print("🎨 Creating static files...")
        
        static_dir = self.base_dir / "static"
        
        # Main CSS
        css_content = """/* Custom styles for Startup Platform */
.hero-gradient {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-hover {
    transition: transform 0.2s ease-in-out;
}

.card-hover:hover {
    transform: translateY(-2px);
}

.btn-primary {
    @apply bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors;
}

.btn-secondary {
    @apply bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700 transition-colors;
}

.form-input {
    @apply w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500;
}
"""
        
        with open(static_dir / "css" / "main.css", "w") as f:
            f.write(css_content)
        
        # Main JavaScript
        js_content = """// Main JavaScript for Startup Platform

// API helper functions
const api = {
    async get(url) {
        const response = await fetch(url);
        return response.json();
    },
    
    async post(url, data) {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        return response.json();
    }
};

// Dashboard functionality
if (window.location.pathname === '/dashboard') {
    // Load real-time stats
    async function loadStats() {
        try {
            const stats = await api.get('/api/stats');
            updateStatsDisplay(stats);
        } catch (error) {
            console.error('Failed to load stats:', error);
        }
    }
    
    function updateStatsDisplay(stats) {
        // Update dashboard stats display
        console.log('Stats updated:', stats);
    }
    
    // Load stats on page load
    document.addEventListener('DOMContentLoaded', loadStats);
    
    // Refresh stats every 30 seconds
    setInterval(loadStats, 30000);
}

// Form handling
document.addEventListener('DOMContentLoaded', function() {
    // Handle all forms with class 'ajax-form'
    document.querySelectorAll('.ajax-form').forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            try {
                const result = await api.post(form.action, data);
                if (result.success) {
                    if (result.redirect) {
                        window.location.href = result.redirect;
                    } else {
                        showNotification('Success!', 'success');
                    }
                } else {
                    showNotification(result.error || 'An error occurred', 'error');
                }
            } catch (error) {
                showNotification('Network error occurred', 'error');
            }
        });
    });
});

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-md text-white z-50 ${
        type === 'success' ? 'bg-green-500' : 
        type === 'error' ? 'bg-red-500' : 
        'bg-blue-500'
    }`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}
"""
        
        with open(static_dir / "js" / "main.js", "w") as f:
            f.write(js_content)
        
        print("✅ Static files created!")
    
    def display_summary(self):
        """Display setup summary"""
        print("\n" + "="*60)
        print("🚀 STARTUP PLATFORM SETUP COMPLETE!")
        print("="*60)
        
        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print("\n⚠️ WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.errors:
            print("\n✅ Setup completed successfully!")
            print("\n📋 NEXT STEPS:")
            print("1. Configure your environment variables in .env")
            print("2. Set up your database (PostgreSQL recommended)")
            print("3. Configure your API keys (OpenAI, Stripe, etc.)")
            print("4. Run the application:")
            print("   python complete_startup_platform.py")
            print("\n🌟 FEATURES AVAILABLE:")
            print("• Website Builder - Create professional websites")
            print("• App Development Platform - Build web and mobile apps")
            print("• Data Management System - Upload and process datasets")
            print("• AI/ML Platform - Train and deploy AI models")
            print("• Analytics Dashboard - Monitor your business")
            print("• User Management - Authentication and subscriptions")
            
            print("\n🔗 ACCESS URLS:")
            print("• Main Application: http://localhost:5000")
            print("• Dashboard: http://localhost:5000/dashboard")
            print("• API Documentation: http://localhost:5000/api/docs")
            
            print("\n💡 DEVELOPMENT:")
            print("• Frontend: cd frontend && npm run dev")
            print("• Backend: python complete_startup_platform.py")
            print("• Database: docker-compose up db")
            print("• Full Stack: docker-compose up")
        else:
            print("\n❌ Setup failed. Please resolve the errors above.")
        
        print("="*60)
    
    def run_setup(self):
        """Run the complete setup process"""
        print("🚀 Starting Comprehensive Startup Platform Setup...")
        print("="*60)
        
        steps = [
            ("Project Structure", self.create_project_structure),
            ("Configuration Files", self.create_configuration_files),
            ("Python Dependencies", self.install_python_dependencies),
            ("Frontend Dependencies", self.install_frontend_dependencies),
            ("Sample Templates", self.create_sample_templates),
            ("Static Files", self.create_static_files)
        ]
        
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}...")
            try:
                step_func()
            except Exception as e:
                self.errors.append(f"{step_name} failed: {str(e)}")
                print(f"❌ {step_name} failed: {e}")
        
        self.display_summary()

def main():
    """Main setup entry point"""
    setup = StartupPlatformSetup()
    setup.run_setup()

if __name__ == "__main__":
    main()
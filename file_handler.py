"""
Smart file and folder handler
"""
import os
import glob
from pathlib import Path

class FileHandler:
    def __init__(self):
        self.system = os.name  # 'nt' for Windows, 'posix' for Unix/Linux/Mac
        self.drives = self.get_available_drives()
    
    def get_available_drives(self):
        """Get all available drives"""
        drives = []
        if self.system == 'nt':  # Windows
            for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    drives.append(drive)
        else:  # Unix-like systems
            drives = ['/']
        return drives
    
    def parse_file_command(self, command, user_id):
        """Parse file/folder command and extract path components"""
        command = command.lower().strip()
        
        # Get user's file aliases
        aliases = {}  # In a real app, this would come from the database
        
        # Check for aliases first
        for alias, path in aliases.items():
            if alias in command:
                return self.handle_alias_command(command, alias, path)
        
        # Parse drive, folder, and file from command
        drive = None
        folder = None
        filename = None
        
        # Extract drive (C drive, D drive, etc.)
        for d in self.drives:
            drive_letter = d[0].lower() if self.system == 'nt' else None
            if drive_letter and f"{drive_letter} drive" in command:
                drive = d
                break
        
        # Extract common folder names
        folder_keywords = ['downloads', 'documents', 'desktop', 'music', 'videos', 'pictures', 'folder']
        for keyword in folder_keywords:
            if keyword in command:
                folder = keyword
                break
        
        # Extract filename (look for file extensions or specific patterns)
        words = command.split()
        for word in words:
            if '.' in word and len(word.split('.')[-1]) <= 4:  # Likely a file
                filename = word
                break
        
        return self.find_and_open_file(drive, folder, filename, command)
    
    def handle_alias_command(self, command, alias, base_path):
        """Handle commands with aliases"""
        if not os.path.exists(base_path):
            return f"Path for '{alias}' not found: {base_path}"
        
        # If just opening the alias folder
        if command.strip() == f"open {alias}" or command.strip() == alias:
            return self.open_path(base_path)
        
        # Look for specific file in alias folder
        words = command.replace(alias, '').strip().split()
        if words:
            search_term = ' '.join(words)
            return self.search_in_directory(base_path, search_term)
        
        return self.open_path(base_path)
    
    def find_and_open_file(self, drive, folder, filename, original_command):
        """Find and open file/folder based on parsed components"""
        search_paths = []
        
        # Build search paths
        if drive and folder:
            search_paths.append(os.path.join(drive, folder))
        elif drive:
            search_paths.append(drive)
        elif folder:
            # Search in common locations
            home = str(Path.home())
            common_folders = {
                'downloads': os.path.join(home, 'Downloads'),
                'documents': os.path.join(home, 'Documents'),
                'desktop': os.path.join(home, 'Desktop'),
                'music': os.path.join(home, 'Music'),
                'videos': os.path.join(home, 'Videos'),
                'pictures': os.path.join(home, 'Pictures')
            }
            
            if folder in common_folders:
                search_paths.append(common_folders[folder])
            else:
                # Search in all common folders
                search_paths.extend(common_folders.values())
        else:
            # Search in home directory
            search_paths = [str(Path.home())]
        
        # Search for the file/folder
        results = []
        for search_path in search_paths:
            if os.path.exists(search_path):
                if filename:
                    results.extend(self.search_for_file(search_path, filename))
                else:
                    # Search for any relevant files based on command
                    results.extend(self.search_by_keywords(search_path, original_command))
        
        return self.handle_search_results(results, original_command)
    
    def search_for_file(self, base_path, filename):
        """Search for a specific file"""
        results = []
        
        try:
            # Direct search with glob
            patterns = [
                f"**/{filename}",
                f"**/*{filename}*",
                f"**/{filename}.*",
                f"**/*{filename.split('.')[0]}*" if '.' in filename else f"**/*{filename}*"
            ]
            
            for pattern in patterns:
                matches = glob.glob(os.path.join(base_path, pattern), recursive=True)
                for match in matches:
                    if os.path.isfile(match) or os.path.isdir(match):
                        results.append(match)
                
                if results:  # Stop at first successful pattern
                    break
        
        except Exception as e:
            print(f"Search error: {e}")
        
        return list(set(results))  # Remove duplicates
    
    def search_by_keywords(self, base_path, command):
        """Search files by keywords in command"""
        results = []
        keywords = command.split()
        
        try:
            for root, dirs, files in os.walk(base_path):
                # Limit search depth
                depth = len(os.path.relpath(root, base_path).split(os.sep))
                if depth > 3:  # Limit depth to prevent deep searches
                    continue
                
                # Search in filenames and folder names
                all_items = files + dirs
                for item in all_items:
                    item_lower = item.lower()
                    if any(keyword.lower() in item_lower for keyword in keywords):
                        full_path = os.path.join(root, item)
                        results.append(full_path)
                        
                        if len(results) >= 20:  # Limit results
                            break
                
                if len(results) >= 20:
                    break
        
        except Exception as e:
            print(f"Keyword search error: {e}")
        
        return results
    
    def search_in_directory(self, directory, search_term):
        """Search for files in a specific directory"""
        if not os.path.exists(directory):
            return f"Directory not found: {directory}"
        
        results = self.search_for_file(directory, search_term)
        if not results:
            results = self.search_by_keywords(directory, search_term)
        
        return self.handle_search_results(results, search_term)
    
    def handle_search_results(self, results, original_command):
        """Handle search results - open if single result, ask user if multiple"""
        if not results:
            return f"No files found for: {original_command}"
        
        if len(results) == 1:
            return self.open_path(results[0])
        
        # Multiple results - return list for user to choose
        return {
            'type': 'multiple_results',
            'message': f"Found {len(results)} matches for '{original_command}':",
            'results': results[:10]  # Limit to 10 results
        }
    
    def open_path(self, path):
        """Open file or folder using system default application"""
        try:
            if not os.path.exists(path):
                return f"Path not found: {path}"
            
            # In a real app, this would open the file/folder
            # For this simulation, we'll just return a success message
            return f"Opened: {os.path.basename(path)}"
        
        except Exception as e:
            return f"Error opening {path}: {str(e)}"
    
    def open_by_index(self, results, index):
        """Open file by index from multiple results"""
        try:
            if 0 <= index < len(results):
                return self.open_path(results[index])
            else:
                return "Invalid selection number"
        except Exception as e:
            return f"Error: {str(e)}"

# Global file handler instance
file_handler = FileHandler()
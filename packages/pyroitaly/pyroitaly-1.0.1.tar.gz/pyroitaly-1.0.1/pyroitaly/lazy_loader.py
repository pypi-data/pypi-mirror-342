#  PyroItaly - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present ItalyMusic <https://github.com/ItalyMusic>
#  Copyright (C) 2025-present ItalyMusic <https://github.com/ItalyMusic>
#
#  This file is part of PyroItaly.
#
#  PyroItaly is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyroItaly is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with PyroItaly.  If not, see <http://www.gnu.org/licenses/>.

import importlib
import sys
from types import ModuleType
from typing import Dict, List, Optional, Set, Any


class LazyLoader:
    """Lazy module loader to improve startup time and memory usage
    
    This class implements lazy loading of modules, which means modules
    are only imported when they are actually used, reducing memory usage
    and improving startup time.
    """
    
    def __init__(self):
        self._cached_modules: Dict[str, ModuleType] = {}
        self._pending_imports: Set[str] = set()
    
    def __call__(self, name: str) -> Any:
        """Lazily import a module or attribute
        
        Args:
            name: Full module path or module.attribute path
            
        Returns:
            The imported module or attribute
        """
        if name in self._cached_modules:
            return self._cached_modules[name]
        
        if name in self._pending_imports:
            # Avoid circular imports
            raise ImportError(f"Circular import detected for {name}")
        
        self._pending_imports.add(name)
        
        try:
            if "." in name:
                # Handle module.attribute format
                module_name, attribute = name.rsplit(".", 1)
                module = self(module_name)
                result = getattr(module, attribute)
            else:
                # Handle full module import
                result = importlib.import_module(name)
            
            self._cached_modules[name] = result
            return result
        finally:
            self._pending_imports.remove(name)
    
    def preload(self, modules: List[str]) -> None:
        """Preload a list of modules
        
        Args:
            modules: List of module names to preload
        """
        for module in modules:
            self(module)
    
    def clear_cache(self) -> None:
        """Clear the module cache"""
        self._cached_modules.clear()


# Create a global instance of the lazy loader
lazy_import = LazyLoader()


class LazyObject:
    """A descriptor for lazily loaded objects
    
    This class allows for lazy loading of objects within a module,
    which are only initialized when accessed.
    """
    
    def __init__(self, import_path: str):
        """Initialize the lazy object
        
        Args:
            import_path: Import path to the object
        """
        self.import_path = import_path
        self._obj = None
    
    def __get__(self, instance, owner):
        if self._obj is None:
            module_path, attr = self.import_path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            self._obj = getattr(module, attr)
        return self._obj

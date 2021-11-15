import glob
import os
from dataclasses import dataclass

@dataclass
class CacheRemover:
    """Remove all cache files of the specified directory"""

    def __init__(self) -> None:
        """Contructor for CacheRemover"""
        
        self.cache_files = []
        self.cache_folders = []
        
    def removecache(self) -> None:
        """Remove all cache from root folder"""
        
        self._removeall_cachefiles()
        self._removeall_cachefolders()

    def collect_cache_files(self, root_dir) -> None:
        """Collect all files and folders from root directory"""

        self.root_dir = os.path.join(root_dir, '**')
        self.cache_files = glob.glob(os.path.join(self.root_dir, '*.pyc'), recursive=True)
        self.cache_files = [os.path.abspath(file) for file in sorted(list(set(self.cache_files)))]
        self.cache_folders = self._get_cache_folders(cachefiles=self.cache_files)

    def _get_cache_folders(self, cachefiles: list) -> list:
        """Get all cache folders for the given cache files"""

        cachefolders = []
        for file in cachefiles:
            cachefolders.append(os.path.dirname(file))

        return sorted(list(set(cachefolders)))

    def _removeall_cachefiles(self) -> None:
        """Remove all cache files"""

        cache = []
        for file in self.cache_files:
            if file.endswith('.pyc'):
                cache.append(file)
                os.remove(file)

        if cache:
            print('Cache Files Removed:')
            for file in cache:
                print(file)
        else:
            print('No cache files found')

    def _removeall_cachefolders(self) -> None:
        """Remove all cache folders"""

        cache = []
        for folder in self.cache_folders:
            if folder.endswith('__pycache__') and os.listdir(folder) == []:
                cache.append(folder)
                os.rmdir(folder)

        if cache:
            print('Cache Folders Removed:')
            for folder in cache:
                print(folder)
        else:
            print('No cache folders found')

import glob
import os
from dataclasses import dataclass

@dataclass
class CacheRemover:
    """Remove all cache files of the specified directory"""

    def __init__(self, root_dir) -> None:
        """Contructor for CacheRemover"""
        
        self.files = []
        self.folders = []
        self.root_dir = os.path.join(root_dir, '**')

    def removecache(self) -> None:
        """Remove all cache from root folder"""
        
        self._collect_cache_files()
        self._removeall_cachefiles()
        self._removeall_cachefolders()

    def _collect_cache_files(self) -> None:
        """Collect all files and folders from root directory"""

        self.cache_files = glob.glob(os.path.join(self.root_dir, '*.pyc'), recursive=True)
        self.cache_files = sorted(list(set(self.cache_files)))
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
            print('Cache Files Removed:')
            for folder in cache:
                print(folder)
        else:
            print('No cache folders found')
            

path = 'F:\\My_Projects\\Python\\Design pattern\\Plugin Architecture\\**'

cache_remover = CacheRemover(root_dir = path)
cache_remover.removecache()

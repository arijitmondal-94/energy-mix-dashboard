from PIL import Image
from pathlib import Path
class GeneratePoster(object):
    
    def __init__(self) -> None:
        pass
    
    def load_blank_poster(self, path: Path) -> None:
        
        if path.exists():
            return Image.open(path)
        else:
            raise ValueError(f'Invalid Path: {path}')
        
    def prepare_information():
        pass
    
    def generate_poster(self) -> bool:
        path = Path('images/gridimp_poster.png')
        image = self.load_blank_poster(path)
        image
        
        return True
    
    
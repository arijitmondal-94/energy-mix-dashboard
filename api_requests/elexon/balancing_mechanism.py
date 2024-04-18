class Elexon(object):
    """
    Base Elexon API class with endpoint URL
    """
    
    def __init__(self) -> None:
        self.headers = {
            "Accept": "test/plain"
        }
        self.base_url: str = "https://data.elexon.co.uk/bmrs/api/v1"
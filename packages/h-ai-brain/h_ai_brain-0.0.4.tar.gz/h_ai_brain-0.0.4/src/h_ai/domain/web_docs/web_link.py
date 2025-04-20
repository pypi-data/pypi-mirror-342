class WebLink:
    def __init__(self, url: str, title: str):
        self.url = url
        self.title = title

    def to_dict(self):
        """Convert this WebLink instance to a serializable dictionary"""
        return {
            'url': self.url,
            'title': self.title
        }

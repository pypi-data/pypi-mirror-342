from github_projectv2.base import Base
from github_projectv2.repository import Repository

class ItemTemplate(Base):
    def __init__(self, node=None):
        """Initialize the item template object"""

        super().__init__()

        self.filename = ""
        self.body = ""
        self.repository = Repository()

    def get(self, org: str, repo: str, filename: str):
        """Fetch the item template data"""
        self.filename = filename

        # Get the template from the repository
        

    def render(data):
        """Render the item template"""
        print("RENDERING")
        print(data)
        # return self.jinja.get_template("item_template.md").render(data)
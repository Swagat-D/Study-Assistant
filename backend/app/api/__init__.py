# Import all API router modules
from app.api import auth
from app.api import documents
from app.api import chat
from app.api import study_tools

# Create a list of all routers for easy inclusion in the main app
router_list = [
    auth.router,
    documents.router,
    chat.router,
    study_tools.router,
]
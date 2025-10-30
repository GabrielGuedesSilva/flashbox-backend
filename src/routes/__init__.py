from src.routes.auth import AuthRouter
from src.routes.flashcard import FlashcardRouter
from src.routes.flashcard_stack import FlashcardStackRouter
from src.routes.users import UserRouter

routers_class = [UserRouter, FlashcardRouter, FlashcardStackRouter, AuthRouter]

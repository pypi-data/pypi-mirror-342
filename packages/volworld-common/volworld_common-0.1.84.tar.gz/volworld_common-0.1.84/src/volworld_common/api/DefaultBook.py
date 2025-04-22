from typing import Final

class Ngsl:
    class Book1:
        TITLE: Final[str] = "NGSL Book 1 of 4 (New General Service List v1.01)"
        UUID: Final[str] = "b7091029-cc77-4616-990f-a21f142a5590"
    class Book2:
        TITLE: Final[str] = "NGSL Book 2 of 4 (New General Service List v1.01)"
        UUID: Final[str] = "eda14e15-86f9-4f30-b77b-a307e2a9a7e4"
    class Book3:
        TITLE: Final[str] = "NGSL Book 3 of 4 (New General Service List v1.01)"
        UUID: Final[str] = "61a33310-a0e6-4ac2-a2f2-099a864c0dc4"
    class Book4:
        TITLE: Final[str] = "NGSL Book 4 of 4 (New General Service List v1.01)"
        UUID: Final[str] = "9a8601a6-caa1-484c-8111-e890634997c0"

class NgslSpoken:
    TITLE: Final[str] = "NGSL-Spoken v1.2 (New General Service List-Spoken)"
    UUID: Final[str] = "5849035d-a37a-4dec-9498-677885e5d43f"

AllDefaultBooks = [NgslSpoken, Ngsl.Book1, Ngsl.Book2, Ngsl.Book3, Ngsl.Book4]


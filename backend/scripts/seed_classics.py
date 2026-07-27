import asyncio
import logging
from sqlalchemy import select
from app.db.database import AsyncSessionLocal, init_db
from app.db.models import ClassicBook, ClassicChapter

logger = logging.getLogger("seed_classics")

CLASSIC_BOOKS = [
    {
        "title": "Alice's Adventures in Wonderland",
        "author": "Lewis Carroll",
        "cover_image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=600&q=80",
        "description": "Alice tumbles down a rabbit hole into a whimsical, surreal world inhabited by peculiar creatures, a talking White Rabbit, and the tyrannical Queen of Hearts.",
        "genres": ["Fantasy", "Classics", "Adventure"],
        "publication_year": 1865,
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Down the Rabbit-Hole",
                "content": (
                    "Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: "
                    "once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, "
                    "'and what is the use of a book,' thought Alice 'without pictures or conversations?'\n\n"
                    "So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), "
                    "whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, "
                    "when suddenly a White Rabbit with pink eyes ran close by her.\n\n"
                    "There was nothing so VERY remarkable in that; nor did Alice think it so VERY much out of the way to hear the Rabbit say to itself, "
                    "'Oh dear! Oh dear! I shall be late!' (when she thought it over afterwards, it occurred to her that she ought to have wondered at this, "
                    "but at the time it all seemed quite natural); but when the Rabbit actually TOOK A WATCH OUT OF ITS WASTECOAT-POCKET, and looked at it, "
                    "and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, "
                    "or a watch to take out of it, and burning with curiosity, she ran across the field after it, and fortunately was just in time to see it pop down a large rabbit-hole under the hedge."
                )
            },
            {
                "chapter_number": 2,
                "title": "The Pool of Tears",
                "content": (
                    "'Curiouser and curiouser!' cried Alice (she was so much surprised, that for the moment she quite forgot how to speak good English); "
                    "'now I'm opening out like the largest telescope that ever was! Good-bye, feet!' (for when she looked down at her feet, they seemed to be almost out of sight, "
                    "they were getting so far off). 'Oh, my poor little feet, I wonder who will put on your shoes and stockings for you now, dears?'"
                )
            }
        ]
    },
    {
        "title": "The Time Machine",
        "author": "H.G. Wells",
        "cover_image": "https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?auto=format&fit=crop&w=600&q=80",
        "description": "A Victorian scientist constructs a machine capable of traveling through time, journeying to the year 802,171 AD where he encounters the gentle Eloi and the sinister underground Morlocks.",
        "genres": ["Sci-Fi", "Classics", "Time Travel"],
        "publication_year": 1895,
        "chapters": [
            {
                "chapter_number": 1,
                "title": "The Inventor's Dilemma",
                "content": (
                    "The Time Traveller (for so it will be convenient to call him) was expounding a recondite matter to us. "
                    "His grey eyes shone and twinkled, and his usually pale face was flushed and animated. "
                    "The fire burned brightly, and the soft radiance of the incandescent lights in the lilies of silver caught the bubbles that flashed and passed in our glasses.\n\n"
                    "'You must follow me carefully. I shall have to controvert one or two ideas that are almost universally accepted. "
                    "The geometry, for instance, they taught you at school is founded on a misconception. "
                    "Can a cube that does not last for any length of time have a real existence?'"
                )
            }
        ]
    },
    {
        "title": "The Adventures of Sherlock Holmes",
        "author": "Arthur Conan Doyle",
        "cover_image": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?auto=format&fit=crop&w=600&q=80",
        "description": "The legendary consulting detective Sherlock Holmes and Dr. John Watson solve mysterious crimes across Victorian London using keen observation and deductive reasoning.",
        "genres": ["Mystery", "Classics", "Detective"],
        "publication_year": 1892,
        "chapters": [
            {
                "chapter_number": 1,
                "title": "A Scandal in Bohemia",
                "content": (
                    "To Sherlock Holmes she is always THE woman. I have seldom heard him mention her under any other name. "
                    "In his eyes she eclipses and mecovers the whole of her sex. It was not that he felt any emotion akin to love for Irene Adler. "
                    "All emotions, and that one particularly, were abhorrent to his cold, precise but admirably balanced mind.\n\n"
                    "One night—it was on the twentieth of March, 1888—I was returning from a journey to a patient (for I had now returned to civil practice), "
                    "when my way led me through Baker Street. As I passed the well-remembered door, which must always be associated in my mind with my wooing, "
                    "and with the dark incidents of the Study in Scarlet, I was seized with a keen desire to see Holmes again."
                )
            }
        ]
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "cover_image": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?auto=format&fit=crop&w=600&q=80",
        "description": "Elizabeth Bennet navigates issues of manners, upbringing, morality, education, and marriage in the society of the landed gentry of early 19th-century England.",
        "genres": ["Romance", "Classics", "Drama"],
        "publication_year": 1813,
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Chapter I",
                "content": (
                    "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.\n\n"
                    "However little known the feelings or views of such a man may be on his first entering a neighbourhood, "
                    "this truth is so well fixed in the minds of the surrounding families, that he is considered the rightful property of some one or other of their daughters."
                )
            }
        ]
    }
]

async def seed():
    await init_db()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(ClassicBook))
        existing = result.scalars().all()
        if existing:
            print("Classic books already seeded.")
            return

        for book_data in CLASSIC_BOOKS:
            ch_data = book_data.pop("chapters")
            book = ClassicBook(**book_data, chapters_count=len(ch_data))
            session.add(book)
            await session.flush()

            for c in ch_data:
                ch = ClassicChapter(
                    classic_book_id=book.id,
                    chapter_number=c["chapter_number"],
                    title=c["title"],
                    content=c["content"],
                    word_count=len(c["content"].split())
                )
                session.add(ch)

        await session.commit()
        print("Classic books successfully seeded!")

if __name__ == "__main__":
    asyncio.run(seed())

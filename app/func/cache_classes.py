from typing import List, Tuple, Iterator

from db_models import Memes, Ratings
from objects import database_handler
from func.essentials import prep4post


class TopMemesCache:
    def __init__(self):

        self.top_memes: List[Tuple[int, int]] = []

    def update_top_memes(self) -> None:
        temp_raiting: dict = {}
        all_likes: list = database_handler.session.query(Ratings).all()
        for rating in all_likes:
            if rating.meme_id in temp_raiting:
                temp_raiting[rating.meme_id] += rating.rate
            else:
                temp_raiting[rating.meme_id] = rating.rate
        sorted_d = sorted((key, value) for (key, value) in temp_raiting.items())
        print(sorted_d)
        self.top_memes = sorted_d[:10]

    def get_top_memes(self) -> Iterator:
        return_query: List[Memes] = database_handler.session.query(Memes).filter(Memes.id in self.top_memes).all()
        for meme in return_query:
            yield prep4post(meme)

    def updated_rating(self, meme_id: int, rating: int) -> None:
        memes: Memes = database_handler.session.query(Memes).filter_by(id=meme_id).first()
        if memes is None:
            return

        if rating > self.top_memes[-1][1]:
            for count, meme in enumerate(self.top_memes):
                if meme[1] < rating:
                    self.top_memes.insert(count, (memes.id, rating))
                    break

        self.top_memes = self.top_memes[:10]


top_meme_cached_query: TopMemesCache = TopMemesCache()
top_meme_cached_query.update_top_memes()

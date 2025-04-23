from dataclasses import dataclass

import tgedr.ds.sources.reddit as sre
from tgedr.ds.sources.reddit import RedditSrc


@dataclass
class MockSubmission:
    title: str
    created_utc: float
    url: str
    selftext: str
    is_self: bool


class MockSubreddit:
    def search(self, qs, sort, time_filter):
        return [
            MockSubmission(
                title="oi",
                created_utc=1745365939.0,
                url="https://www.reddit.com/r/comments/how/",
                selftext=".......",
                is_self=True,
            ),
            MockSubmission(
                title="oi",
                created_utc=1745365939.0,
                url="https://www.reddit.com/r/Semaglutide/did/",
                selftext=".......",
                is_self=False,
            ),
        ]


class MockReddit:
    def __init__(self, client_id, client_secret, password, user_agent, username):
        pass

    def subreddit(self, sr: str):
        return MockSubreddit()


def test_get(monkeypatch, reddit_env):
    monkeypatch.setattr(sre, "Reddit", MockReddit)
    o = RedditSrc({})

    expected = [
        {
            "title": "oi",
            "created": "2025-04-22 23:52:19",
            "url": "https://www.reddit.com/r/comments/how/",
            "text": ".......",
        }
    ]

    actual = o.get(
        {
            "REDDIT_PSWD": "REDDIT_PSWD",
            "REDDIT_USER": "REDDIT_USER",
            "QUERY_STRING": "semaglutide",
            "QUERY_FILTER": "hour",
            "QUERY_SORT": "relevance",
            "RETRIEVE_TEXT": "true",
        }
    )
    assert actual == expected

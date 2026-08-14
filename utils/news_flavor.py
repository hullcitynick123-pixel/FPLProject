"""Generates randomized tabloid-style flourishes for the transfer news feed."""

import hashlib
import random

HEADLINE_TAGS = [
    "BREAKING",
    "TRANSFER NEWS",
    "JUST IN",
    "DEADLINE DAY DRAMA",
    "EXCLUSIVE",
    "SHOCK MOVE",
    "here we go",
    "MEDICAL BOOKED",
]

FEE_TEMPLATES = [
    "£{fee}m",
    "£{fee}m + add-ons",
    "an undisclosed fee (believed to be £{fee}m)",
    "£{fee}m, add-ons could rise to £{fee_high}m",
]

MANAGER_QUOTES = [
    "\"This is exactly the business we needed to do,\" said {manager}.",
    "\"I'm buzzing, this could win us the league,\" beamed {manager}.",
    "\"No regrets, this squad is stacked,\" claimed {manager}.",
    "\"My rivals should be worried,\" warned {manager}.",
    "\"Slept on this one all week, glad it's done,\" admitted {manager}.",
    "\"Absolute steal at that price,\" grinned {manager}.",
]

PLAYER_QUOTES = [
    "\"Buzzing to be part of this project,\" the new signing said.",
    "\"Time for a new chapter,\" the departing player posted online.",
    "\"I've always wanted to play under this manager,\" said the incoming star.",
    "\"Sad to go but it's the right move for my career,\" said the outgoing player.",
    "\"Let's get this bread,\" the signing tweeted minutes after the deal.",
]

CROWD_REACTIONS = [
    "Rival managers were seen frantically refreshing the group chat.",
    "The WhatsApp group has not stopped buzzing since the news broke.",
    "Bookmakers have already slashed the odds on a title charge.",
    "Fans are already debating if this is a top-6 finish move.",
    "Pundits on the group chat called it 'business as usual'.",
]


def _seeded_random(seed_text: str) -> random.Random:
    """Return a Random instance seeded deterministically from the given text."""
    digest = hashlib.md5(seed_text.encode("utf-8")).hexdigest()
    return random.Random(int(digest, 16))


def flavor_transfer(transfer_text: str, manager_name: str, seed_text: str = None) -> str:
    """Wrap a raw transfer entry with a randomized tabloid-style headline, fee and quote."""
    rng = _seeded_random(seed_text if seed_text is not None else transfer_text)

    tag = rng.choice(HEADLINE_TAGS)
    fee = rng.randint(1, 120)
    fee_template = rng.choice(FEE_TEMPLATES)
    fee_text = fee_template.format(fee=fee, fee_high=min(fee + rng.randint(5, 20), 150))

    quote = rng.choice(MANAGER_QUOTES + PLAYER_QUOTES).format(manager=manager_name)
    reaction = rng.choice(CROWD_REACTIONS)

    return f"{tag}! {transfer_text} for {fee_text}. {quote} {reaction}"


def build_dynamic_feed(transfers: list, gameweek_id: int = 0) -> list:
    """Turn raw 'Manager: transfer' strings into randomized news-style headlines."""
    feed = []
    for entry in transfers:
        manager_name, _, transfer_text = entry.partition(":")
        manager_name = manager_name.strip()
        transfer_text = transfer_text.strip() or entry

        # Seed on the gameweek too so flavor varies week to week for the same transfer text,
        # without leaking the seed suffix into the displayed headline.
        headline = flavor_transfer(transfer_text, manager_name, seed_text=f"{transfer_text}|{gameweek_id}")
        feed.append(headline)

    return feed

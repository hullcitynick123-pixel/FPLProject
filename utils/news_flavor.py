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
    "MEDICAL BOOKED",
]

FEE_TEMPLATES = [
    "£{fee}m",
    "£{fee}m + add-ons",
    "an undisclosed fee (believed to be £{fee}m)",
    "£{fee}m, add-ons could rise to £{fee_high}m",
]

MANAGER_QUOTES = [
"\"I didn't even ask for him, but the board said he was on sale so here we are,\" said {manager}.",
"\"If he plays more than 20 minutes without pulling a hamstring, I'll call it a success,\" admitted {manager}.",
"\"I haven't actually spoken to him yet, but his YouTube compilation looked decent,\" confessed {manager}.",
"\"He's got great character, which is manager-speak for 'he can't kick a ball,'\" joked {manager}.",
"\"Honestly, I just needed someone tall enough to defend back-post corners,\" stated {manager}.",
"\"My tactical plan is simple: pass him the ball and pray to God,\" revealed {manager}.",
"\"We spent the entire transfer budget on his wages, so we're playing with ten men and a dream,\" sighed {manager}.",
"\"I offered his previous club a packet of crisps and a spare match ball, and surprisingly they took it,\" grinned {manager}.",
"\"He failed three medicals, but his agent gave us a really nice pen so we signed anyway,\" claimed {manager}.",
"\"I told the board I needed a world-class striker and they brought me a backup left-back,\" grumbled {manager}.",
"\"He's got a terrible attitude, but so do I, so we're going to get along great,\" said {manager}.",
"\"I don't know where he fits in the formation, we'll just figure it out during the warm-up,\" admitted {manager}.",
"\"His stats on Football Manager were incredible, so I didn't see the need to scout him in person,\" explained {manager}.",
"\"If this transfer backfires, I'm blaming the sporting director and turning off my phone,\" warned {manager}.",
"\"We had to promise him he could skip Monday morning fitness sessions just to get the deal over the line,\" revealed {manager}.",
"\"I'm not saying he's lazy, but I've seen statues move with more urgency,\" noted {manager}.",
"\"He cost more than our entire stadium, so no pressure on the lad,\" laughed {manager}.",
"\"I'm fully expecting him to get sent off on his debut, and frankly, I respect it,\" said {manager}.",
"\"He doesn't speak the language, I don't speak his language, but we both hate the referee so we'll be fine,\" declared {manager}.",
"\"I told him if he scores ten goals this season I'll let him pick the pre-match playlist,\" promised {manager}.",
]

PLAYER_QUOTES = [
"\"Honestly, I just Googled the city yesterday and it looks decent,\" the new signing admitted.",
"\"I didn't even want to leave, but my agent told me we were going on a surprise holiday and we landed here,\" posted the confused player.",
"\"The manager sent me a two-minute voice note on WhatsApp and I was sold,\" declared the record signing.",
"\"I'm here to build a dynasty, or at least fulfill the remaining three years of my tax obligation,\" stated the incoming player.",
"\"To the fans who burned my shirt: I get it, but orange was never my color anyway,\" tweeted the player.",
"\"I was just looking for a decent Nando's and accidentally signed a five-year deal,\" explained the new signing.",
"\"The vibes in the dressing room were ruined, so I had to pack my bags,\" said the outgoing playmaker.",
"\"I haven't slept in 72 hours and I don't actually know what league we're in, but let's go,\" said the deadline-day arrival.",
"\"My dog liked the green grass at the training ground, so the decision was easy,\" revealed the player.",
"\"Thank you to the board for meeting my absurd wage requests,\" posted the player alongside a jet emoji.",
"\"I came here to play Europa League football, so imagine my surprise when I checked the table,\" admitted the summer signing.",
"\"The gaffer promised me I could take all the penalties and select the pre-match playlist,\" claimed the incoming star.",
"\"I will miss the local takeaway most of all. Farewell to a legendary kebab shop,\" wrote the departing signing.",
"\"Unfollowing the old team on Instagram as we speak. No hard feelings,\" tweeted the fresh arrival.",
"\"I signed the contract on the hood of a rental car, so you know the passion is real,\" said the young prospect.",
"\"To the three fans who supported me through my five total appearances: thank you,\" shared the fringe player.",
"\"My agent said if I didn't take this move he'd leak my group chats, so here I am,\" admitted the player.",
"\"Can't wait to sit on the bench in a slightly warmer stadium,\" posted the bloke.",
"\"I've been a lifelong fan of this club since approximately 9:00 AM this morning,\" announced the marquee signing.",
"\"I'm only here because the weather is statistically 2% better,\" confessed the new signing."
]

CROWD_REACTIONS = [
"Supporters were seen setting up a GoFundMe to cover the player's Uber to the airport.",
"Rival fans immediately began editing together a 10-minute compilation of his worst touches.",
"Local kebab shops reported an unprecedented spike in 'emotional support shawarmas' following the news.",
"The club's official shop ran out of the letter 'X' within twelve minutes of the announcement.",
"Pundits in the group chat are currently arguing over whether this transfer constitutes a war crime.",
"Fan forums crashed after three separate users claimed to have spotted the player at a motorway service station.",
"A local man has already tattooed the signing's face over his own daughter's portrait.",
"Rival managers were seen frantically deleting old tweets praising the player's tactical discipline.",
"The fanbase has collectively decided to forgive four years of terrible performances because he posted a cool video.",
"A vocal minority on Twitter is already demanding the chairman's resignation despite the window opening two hours ago.",
"Tracking the player's private jet flight became the most-watched livestream in the country.",
"Season ticket holders are currently arguing if a 0.2 mph speed increase makes him 'world class'.",
"An elderly supporter was spotted burning a shirt in his front garden while playing sad violin music on a Bluetooth speaker.",
"The local council was forced to issue a noise complaint against a WhatsApp group.",
"Tactical YouTubers have already uploaded three-hour documentary videos analyzing his throw-in technique.",
"Rival supporters insist he only joined because the club's training ground has a slightly better coffee machine.",
"Pundits are claiming this $80m signing was actually a 'bargain' because of inflation.",
"The player's Wikipedia page was edited 400 times in five minutes to state he is the king of the city.",
"A petition to rename the local stadium after his agent has already gathered 10,000 signatures.",
"Fans are already debating whether a 14th-place finish would be an underachievement with this roster."
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

    manager_label = f"{manager_name}: " if manager_name else ""
    return f"{tag}! {manager_label}{transfer_text} for {fee_text}. {quote} {reaction}"


def build_dynamic_feed(transfers: list, gameweek_id: int = 0) -> list:
    """Turn raw 'Manager: transfer' strings into randomized news-style headlines.

    Returns a list of (headline, transfer_text) tuples so callers can style the
    raw "Player OUT / Player IN" segment differently from the surrounding flavor text.
    """
    feed = []
    for entry in transfers:
        manager_name, _, transfer_text = entry.partition(":")
        manager_name = manager_name.strip()
        transfer_text = transfer_text.strip() or entry

        # Seed on the gameweek too so flavor varies week to week for the same transfer text,
        # without leaking the seed suffix into the displayed headline.
        headline = flavor_transfer(transfer_text, manager_name, seed_text=f"{transfer_text}|{gameweek_id}")
        feed.append((headline, transfer_text))

    return feed

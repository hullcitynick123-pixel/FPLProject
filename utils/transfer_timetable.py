"""Compute the current transfer pick slot for the transfer window timetable."""

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from fpl_constants import TRANSFER_PICK_ORDER

LONDON_TZ = ZoneInfo("Europe/London")

# (label, pick number or None for the catch-all slot, day offset, start time, end time)
# day offset 0 = "two days before kickoff", day offset 1 = "the day before kickoff".
# The Overnight slot spans from day 0 19:00 through to day 1 09:00.
_SLOT_DEFINITIONS = [
    ("1st Pick", 1, 0, time(9, 0), time(11, 0)),
    ("2nd Pick", 2, 0, time(11, 0), time(13, 0)),
    ("3rd Pick", 3, 0, time(13, 0), time(15, 0)),
    ("4th Pick", 4, 0, time(15, 0), time(17, 0)),
    ("5th Pick", 5, 0, time(17, 0), time(19, 0)),
    ("Overnight Slot", 6, 0, time(19, 0), time(9, 0)),  # end time falls on day offset + 1
    ("7th Pick", 7, 1, time(9, 0), time(11, 0)),
    ("8th Pick", 8, 1, time(11, 0), time(13, 0)),
    ("9th Pick", 9, 1, time(13, 0), time(15, 0)),
    ("10th Pick", 10, 1, time(15, 0), time(17, 0)),
    ("AfterThought Slot", None, 1, time(17, 0), time(23, 59, 59)),
]


def get_pick_order(gameweek_id: int) -> list[str]:
    """Return the manager pick order for a gameweek, rotating the fixed sheet order."""
    start_index = (gameweek_id - 1) % len(TRANSFER_PICK_ORDER)
    return TRANSFER_PICK_ORDER[start_index:] + TRANSFER_PICK_ORDER[:start_index]


def build_transfer_slots(gameweek_id: int, first_kickoff: datetime) -> list[dict]:
    """Build the ordered list of transfer slots (with manager & time window) for a gameweek."""
    pick_order = get_pick_order(gameweek_id)
    window_start_date = first_kickoff.astimezone(LONDON_TZ).date() - timedelta(days=2)

    slots = []
    for label, pick_number, day_offset, start_t, end_t in _SLOT_DEFINITIONS:
        slot_date = window_start_date + timedelta(days=day_offset)
        start_dt = datetime.combine(slot_date, start_t, tzinfo=LONDON_TZ)

        end_date = slot_date + timedelta(days=1) if end_t <= start_t else slot_date
        end_dt = datetime.combine(end_date, end_t, tzinfo=LONDON_TZ)

        manager = pick_order[pick_number - 1] if pick_number else None
        slots.append({
            "label": label,
            "manager": manager,
            "start": start_dt,
            "end": end_dt,
        })

    return slots


def get_current_transfer_slot(gameweek_id: int, first_kickoff: datetime | None, now: datetime | None = None) -> dict | None:
    """Return the currently active transfer slot for a gameweek, or None if outside the window."""
    if first_kickoff is None:
        return None

    now = (now or datetime.now(tz=LONDON_TZ)).astimezone(LONDON_TZ)
    slots = build_transfer_slots(gameweek_id, first_kickoff)

    for slot in slots:
        if slot["start"] <= now < slot["end"]:
            return slot

    return None

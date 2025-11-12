from datetime import datetime, timedelta

PRIORITY_SPEEDS = {
    "standard": 400,
    "express": 650,
    "overnight": 1200
}

def _ceil_days(x: float) -> int:
    i = int(x)
    return i if abs(x - i) < 1e-9 else i + 1

def calculate_eta(distance_km: float, priority: str = "standard"):
    priority = (priority or "standard").lower()
    speed = PRIORITY_SPEEDS.get(priority, PRIORITY_SPEEDS["standard"])

    days = distance_km / speed
    days = _ceil_days(days)

    weather_delay = 0
    if distance_km > 1500:
        weather_delay = 2
    elif distance_km > 700:
        weather_delay = 1

    days += weather_delay

    eta_date = datetime.now() + timedelta(days=days)

    weekend_pushed = False
    if eta_date.weekday() == 6:
        eta_date += timedelta(days=1)
        weekend_pushed = True
        days += 1

    return eta_date.strftime("%Y-%m-%d"), days, {
        "priority": priority,
        "weather_delay_days": weather_delay,
        "weekend_pushed": weekend_pushed
    }
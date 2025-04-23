from datetime import time, datetime
from zoneinfo import ZoneInfo

def time_zone():
    return 'Australia/Sydney'

tariffs = {
    'EA010': {
        'name': 'Residential flat',
        'periods': [
            ('Anytime', time(0, 0), time(23, 59), 10.8007)
        ]
    },
    'EA025': {
        'name': 'Residential ToU',
        'periods': [
            ('Peak', time(15, 0), time(21, 0), 26.8969),
            ('Off-peak', time(21, 0), time(15, 0), 4.6503)
        ],
        'peak_months': [11, 12, 1, 2, 3, 6, 7, 8]  # November–March and June–August
    },
    'EA111': {
        'name': 'Residential demand (introductory)',
        'periods': [
            ('Anytime', time(0, 0), time(23, 59), 10.7805)
        ]
    },
    'EA116': {
        'name': 'Residential demand',
        'periods': [
            ('Anytime', time(0, 0), time(23, 59), 2.3370)
        ]
    },
    'EA225': {
        'name': 'Small Business ToU',
        'periods': [
            ('Peak', time(15, 0), time(21, 0), 33.0130),
            ('Off-peak', time(21, 0), time(15, 0), 5.2507)
        ],
        'peak_months': [11, 12, 1, 2, 3, 6, 7, 8]  # November–March and June–August
    }
}

def get_periods(tariff_code: str):
    tariff = tariffs.get(tariff_code)
    if not tariff:
        raise ValueError(f"Unknown tariff code: {tariff_code}")
    return tariff['periods']

def convert_feed_in_tariff(interval_datetime: datetime, tariff_code: str, rrp: float):
    rrp_c_kwh = rrp / 10
    return rrp_c_kwh

def convert(interval_datetime: datetime, tariff_code: str, rrp: float):
    interval_time = interval_datetime.astimezone(ZoneInfo(time_zone())).time()
    rrp_c_kwh = rrp / 10
    tariff = tariffs.get(tariff_code)

    if not tariff:
        raise ValueError(f"Unknown tariff code: {tariff_code}")

    current_month = interval_datetime.month

    # Determine if current month is within peak months
    is_peak_month = 'peak_months' in tariff and current_month in tariff['peak_months']

    for period_name, start, end, rate in tariff['periods']:
        if period_name == 'Peak' and not is_peak_month:
            continue  # Skip peak period if not in peak months

        if start <= end:
            if start <= interval_time < end:
                return rrp_c_kwh + rate
        else:
            # Over midnight
            if interval_time >= start or interval_time < end:
                return rrp_c_kwh + rate

    # If no period matches, apply default approximation
    slope = 1.037869032618134
    intercept = 5.586606750833143
    return rrp_c_kwh * slope + intercept

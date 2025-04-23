# aemo_to_tariff/sapower.py
from datetime import time, datetime
from zoneinfo import ZoneInfo

def time_zone():
    return 'Australia/Adelaide'


feed_in_tariffs = {
    'RELE2W': {
        'name': 'Residential Electrify',
        'periods': [
            ('Peak', time(15, 0), time(20, 0), 12.36),
            ('Peak', time(6, 0), time(10, 0), 12.36),
            ('Off-peak', time(20, 0), time(6, 0), 0),
            ('Solar Sponge', time(10, 0), time(15, 0), -1)
        ]
    }
}

tariffs = {
    'RSR': {
        'name': 'Residential Single Rate',
        'periods': [
            ('Anytime', time(0, 0), time(23, 59), 15.04)
        ]
    },
    'RTOU': {
        'name': 'Residential Time of Use',
        'periods': [
            ('Peak', time(15, 0), time(20, 0), 20.669),
            ('Peak', time(6, 0), time(10, 0), 20.669),
            ('Off-peak', time(20, 0), time(6, 0), 8.316),
            ('Solar Sponge', time(10, 0), time(15, 0), 4.191)
        ]
    },
    'RPRO': {
        'name': 'Residential Prosumer',
        'periods': [
            ('Peak', time(15, 0), time(20, 0), 20.669),
            ('Peak', time(6, 0), time(10, 0), 20.669),
            ('Off-peak', time(20, 0), time(6, 0), 8.316),
            ('Solar Sponge', time(10, 0), time(15, 0), 4.191)
        ]
    },
    'RELE': {
        'name': 'Residential Electrify',
        'periods': [
            ('Peak', time(15, 0), time(20, 0), 33.09),
            ('Peak', time(6, 0), time(10, 0), 20.669),
            ('Off-peak', time(20, 0), time(6, 0), 9.78),
            ('Solar Sponge', time(10, 0), time(15, 0), 3.01)
        ]
    },
    'RELE2W': {
        'name': 'Residential Electrify',
        'periods': [
            ('Peak', time(15, 0), time(20, 0), 33.09),
            ('Peak', time(6, 0), time(10, 0), 33.09),
            ('Off-peak', time(20, 0), time(6, 0), 9.78),
            ('Solar Sponge', time(10, 0), time(15, 0), 3.01)
        ]
    },
    'SBTOU': {
        'name': 'Small Business Time of Use',
        'periods': [
            ('Peak', time(7, 0), time(21, 0), 25.68),
            ('Off-peak', time(21, 0), time(7, 0), 9.69)
        ]
    },
    'SBTOUE': {
        'name': 'Small Business Time of Use Electrify',
        'periods': [
            ('Peak', time(7, 0), time(21, 0), 32.57),
            ('Off-peak', time(21, 0), time(7, 0), 9.60)
        ]
    }
}

daily_fees = {
    'RSR': 57.53,
    'RTOU': 57.53,
    'RPRO': 57.53,
    'RELE': 57.53,
    'SBTOU': 72.59,
    'SBTOUE': 72.59
}

demand_charges = {
    'RPRO': 83.39,  # $/kW/day
    'SBTOUD': 8.42  # $/kW/day
}


def get_periods(tariff_code: str):
    tariff = tariffs.get(tariff_code)
    if not tariff:
        raise ValueError(f"Unknown tariff code: {tariff_code}")

    return tariff['periods']

def convert_feed_in_tariff(interval_datetime: datetime, tariff_code: str, rrp: float):
    """
    Convert RRP from $/MWh to c/kWh for SA Power Networks.

    Parameters:
    - interval_datetime (datetime): The interval datetime.
    - tariff_code (str): The tariff code.
    - rrp (float): The Regional Reference Price in $/MWh.

    Returns:
    - float: The price in c/kWh.
    """
    interval_time = interval_datetime.astimezone(ZoneInfo(time_zone())).time()
    rrp_c_kwh = rrp / 10
    
    feed_in_tariff = feed_in_tariffs.get(tariff_code)
    if not feed_in_tariff:
        return rrp_c_kwh
    
    for period, start, end, rate in feed_in_tariff['periods']:
        if start <= interval_time < end or (start > end and (interval_time >= start or interval_time < end)):
            total_price = rrp_c_kwh + rate
            return total_price

    return rrp_c_kwh

def convert(interval_datetime: datetime, tariff_code: str, rrp: float):
    """
    Convert RRP from $/MWh to c/kWh for SA Power Networks.

    Parameters:
    - interval_datetime (datetime): The interval datetime.
    - tariff_code (str): The tariff code.
    - rrp (float): The Regional Reference Price in $/MWh.

    Returns:
    - float: The price in c/kWh.
    """
    interval_time = interval_datetime.astimezone(ZoneInfo(time_zone())).time()
    rrp_c_kwh = rrp / 10

    tariff = tariffs.get(tariff_code)

    if not tariff:
        # Handle unknown tariff codes
        slope = 1.037869032618134
        intercept = 5.586606750833143
        return rrp_c_kwh * slope + intercept

    # Find the applicable period and rate
    for period, start, end, rate in tariff['periods']:
        if start <= interval_time < end or (start > end and (interval_time >= start or interval_time < end)):
            total_price = rrp_c_kwh + rate
            return total_price

    # If no period is found, use the first rate as default
    return rrp_c_kwh + tariff['periods'][0][3]

def get_daily_fee(tariff_code: str):
    """
    Get the daily fee for a given tariff code.

    Parameters:
    - tariff_code (str): The tariff code.

    Returns:
    - float: The daily fee in dollars.
    """
    return daily_fees.get(tariff_code, 0.0)

def calculate_demand_fee(tariff_code: str, demand_kw: float, days: int = 30):
    """
    Calculate the demand fee for a given tariff code, demand amount, and time period.

    Parameters:
    - tariff_code (str): The tariff code.
    - demand_kw (float): The maximum demand in kW.
    - days (int): The number of days for the billing period (default is 30).

    Returns:
    - float: The demand fee in dollars.
    """
    daily_charge = demand_charges.get(tariff_code, 0.0)
    return daily_charge * demand_kw * days

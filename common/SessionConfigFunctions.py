from datetime import datetime

from otree.api import Currency as cu
from otree.models import Session
import numpy as np
from  copy import deepcopy

SK_INTEREST_RATE = 'interest_rate'
SK_DIV_AMOUNT = 'div_amount'
SK_DIV_DIST = 'div_dist'
SK_MARGIN_RATIO = 'margin_ratio'
SK_MARGIN_PREMIUM = 'margin_premium'
SK_MARGIN_TARGET_RATIO = 'margin_target_ratio'
SK_INITIAL_PRICE = 'initial_price'
SK_SESSION_NAME = 'name'
SK_RANDOMIZE_HISTORY = 'random_hist'
SK_BONUS_CAP = 'bonus_cap'
SK_AUTO_TRANS_DELAY = 'auto_trans_delay'
SK_FLOAT_RATIO_CAP = 'float_ratio_cap'
SK_FORECAST_THOLD = 'forecast_thold'
SK_FORECAST_REWARD = 'forecast_reward'
SK_FORECAST_RANGE = 'forecast_range'
SK_FORECAST_PERIODS='forecast_periods'
SK_QUIZ_REWARD='quiz_reward'
SK_MARKET_TIME = 'market_time'
SK_FIXATE_TIME = 'fixate_time'
SK_RISK_ELIC_TIME = 'risk_elic_time'
SK_PRACTICE_TIME = 'practice_time'
SK_PRACTICE_END_TIME = 'practice_end_time'
SK_FINAL_RESULTS_TIME = 'final_results_time'
SK_FORECAST_TIME = 'forecast_time'
SK_SUMMARY_TIME = 'summary_time'
SK_ENDOW_STOCK = 'endow_stock'
SK_ENDOW_WORTH = 'endow_worth'
SK_SHOW_NEXT = 'show_next'
SK_CONVERSION_RATE = 'real_world_currency_per_point'
SK_IS_PROLIFIC = 'is_prolific'
SK_IS_MTURK = 'is_mturk'
SK_IS_PILOT = 'is_pilot'
SK_EXP_TIME_PILOT = 'expected_time_pilot'
SK_EXP_TIME_LIVE = 'expected_time_live'
SK_START_TIME = 'start_time'
SK_DEFAULT_URL = 'default_url'

WHOLE_NUMBER_PERCENT = "{:.0%}"


def ensure_config(obj):
    if type(obj) == dict:
        return obj
    elif type(obj) == Session:
        return deepcopy(obj.config)
    else:
        return deepcopy(obj.session.config)


def ensure_group(obj):
    """Helper function to get group from various object types"""
    if hasattr(obj, 'group'):
        return obj.group
    elif hasattr(obj, 'subsession'):
        return obj.subsession.group
    return obj


def get_item_as_int(config, key, default=0, return_none=False):
    raw_value = config.get(key)
    if raw_value:
        return int(raw_value)
    elif raw_value is None and return_none:
        return None
    else:
        return default


def get_item_as_float(config, key, default=0.0, return_none=False):
    raw_value = config.get(key)
    if raw_value:
        return float(raw_value)
    elif raw_value is None and return_none:
        return None
    else:
        return default


def get_item_as_currency(config, key, default=0):
    raw_value = config.get(key)
    if raw_value:
        return cu(raw_value)
    else:
        return cu(default)


def get_item_as_bool(config, key, default=False):
    raw_value = config.get(key)
    if raw_value:
        return bool(raw_value)
    else:
        return default


def get_init_price(obj):
    config = ensure_config(obj)
    return get_item_as_float(config, SK_INITIAL_PRICE, return_none=True)


def get_session_name(obj):
    config = ensure_config(obj)
    return config.get(SK_SESSION_NAME)


def as_wnp(x):
    return WHOLE_NUMBER_PERCENT.format(x)


def get_margin_ratio(obj, wnp=False):
    config = ensure_config(obj)
    if wnp:
        return as_wnp(config.get(SK_MARGIN_RATIO))
    else:
        return get_item_as_float(config, SK_MARGIN_RATIO)


def get_margin_target_ratio(obj, wnp=False):
    config = ensure_config(obj)
    if wnp:
        return as_wnp(config.get(SK_MARGIN_TARGET_RATIO))
    else:
        return get_item_as_float(config, SK_MARGIN_TARGET_RATIO)


def get_margin_premium(obj, wnp=False):
    config = ensure_config(obj)
    if wnp:
        return as_wnp(config.get(SK_MARGIN_PREMIUM))
    else:
        return get_item_as_float(config, SK_MARGIN_PREMIUM)


def get_round_specific_value(value_str, obj):
    """Helper function to get round-specific values from semicolon-separated strings"""
    if not isinstance(value_str, str):
        return str(value_str)
        
    values = value_str.split(';')
    if len(values) == 1:
        return value_str
        
    # Get round number from group
    round_number = 1
    if hasattr(obj, 'round_number'):
        round_number = obj.round_number
    elif hasattr(obj, 'group') and hasattr(obj.group, 'round_number'):
        round_number = obj.group.round_number
    elif isinstance(obj, dict) and 'round_number' in obj:
        round_number = obj['round_number']
    
    # If round number exceeds available values, use the last value
    index = min(round_number - 1, len(values) - 1)
    if index < 0:
        index = 0
    return values[index]


def get_interest_rate(obj):
    config = ensure_config(obj)
    value = config.get(SK_INTEREST_RATE)
    round_value = get_round_specific_value(str(value), obj)
    return float(round_value)


def get_dividend_amount(obj):
    config = ensure_config(obj)
    value = config.get(SK_DIV_AMOUNT)
    return get_round_specific_value(str(value), obj)


def get_dividend_dist(obj):
    config = ensure_config(obj)
    value = config.get(SK_DIV_DIST)
    return get_round_specific_value(str(value), obj)


def get_dividend_probabilities(obj):
    return np.array([float(x) for x in get_dividend_dist(obj).split()])


def get_dividend_amounts(obj):
    return np.array([float(x) for x in get_dividend_amount(obj).split()])


def get_fundamental_value(obj):
    config = ensure_config(obj)

    dist = get_dividend_probabilities(config)
    div_amounts = get_dividend_amounts(config)
    exp = dist.dot(div_amounts)
    r = get_interest_rate(config)

    if r == 0:
        return 0

    return cu(exp / r)
    # return 14


def is_random_hist(obj):
    config = ensure_config(obj)
    return get_item_as_bool(config, SK_RANDOMIZE_HISTORY)


def get_bonus_cap(obj):
    config = ensure_config(obj)
    return get_item_as_currency(config, SK_BONUS_CAP, default=9999999999)


def get_auto_trans_delay(obj):
    config = ensure_config(obj)
    return get_item_as_int(config, SK_AUTO_TRANS_DELAY)


def get_float_ratio_cap(obj):
    """
    Return the short cap ratio if set, otherwise None.
    @param obj:
    @return: the short cap ratio if set, otherwise None.
    """
    config = ensure_config(obj)
    return get_item_as_float(config, SK_FLOAT_RATIO_CAP, return_none=True)


def get_forecast_thold(obj):
    config = ensure_config(obj)
    return get_item_as_int(config, SK_FORECAST_THOLD)


def get_forecast_reward(obj):
    config = ensure_config(obj)
    return get_item_as_float(config, SK_FORECAST_REWARD)


def get_forecast_range(obj):
    config = ensure_config(obj)
    return get_item_as_int(config, SK_FORECAST_RANGE)

def get_forecast_periods(obj):
    config = ensure_config(obj)
    p = config.get(SK_FORECAST_PERIODS)
    return [int(x) for x in p.split(',')]


def get_quiz_reward(obj):
    config = ensure_config(obj)
    return get_item_as_float(config, SK_QUIZ_REWARD)


def get_market_time(obj):
    config = ensure_config(obj)
    return get_item_as_int(config, SK_MARKET_TIME, return_none=True)


def get_fixate_time(obj):
    config = ensure_config(obj)
    return get_item_as_int(config, SK_FIXATE_TIME, return_none=True)


def get_risk_elic_time(obj):
    config = ensure_config(obj)
    return get_item_as_int(config, SK_RISK_ELIC_TIME, return_none=True)


def get_forecast_time(obj):
    config = ensure_config(obj)
    return get_item_as_int(config, SK_FORECAST_TIME, return_none=True)


def get_summary_time(obj):
    config = ensure_config(obj)
    return get_item_as_int(config, SK_SUMMARY_TIME, return_none=True)


def get_practice_time(obj):
    config = ensure_config(obj)
    return get_item_as_int(config, SK_PRACTICE_TIME, return_none=True)


def get_practice_end_time(obj):
    config = ensure_config(obj)
    return get_item_as_int(config, SK_PRACTICE_END_TIME, return_none=True)

def get_final_results_time(obj):
    print(obj)
    config = ensure_config(obj)
    print(config)
    return get_item_as_int(config, SK_FINAL_RESULTS_TIME, return_none=True)


def get_endow_stock(obj):
    config = ensure_config(obj)
    return config.get(SK_ENDOW_STOCK)


def get_endow_stocks(obj):
    return [int(x) for x in get_endow_stock(obj).split()]


def get_endow_worth(obj):
    config = ensure_config(obj)
    return get_item_as_int(config, SK_ENDOW_WORTH)


def show_next_button(obj):
    config = ensure_config(obj)
    return get_item_as_bool(config, SK_SHOW_NEXT)


def get_conversion_rate(obj):
    config = ensure_config(obj)
    return get_item_as_float(config, SK_CONVERSION_RATE)


def is_prolific(obj):
    config = ensure_config(obj)
    return get_item_as_bool(config, SK_IS_PROLIFIC)


def is_mturk(obj):
    config = ensure_config(obj)
    return get_item_as_bool(config, SK_IS_MTURK)


def is_online(obj):
    return is_prolific(obj) or is_mturk(obj)


def is_pilot(obj):
    config = ensure_config(obj)
    return get_item_as_bool(config, SK_IS_PILOT)


def get_exp_time_pilot(obj):
    config = ensure_config(obj)
    return get_item_as_int(config, SK_EXP_TIME_PILOT)


def get_exp_time_live(obj):
    config = ensure_config(obj)
    return get_item_as_int(config, SK_EXP_TIME_LIVE)


def get_expected_time(obj):
    if is_pilot(obj):
        return get_exp_time_pilot(obj)
    else:
        return get_exp_time_live(obj)


def get_start_time(obj):
    config = ensure_config(obj)
    raw_st = config.get(SK_START_TIME)
    # allow this to raise an exception
    # this should fail fast
    dt = datetime.strptime(raw_st, '%Y%m%d%H%M')
    return dt


def get_default_url(obj):
    config = ensure_config(obj)
    return config.get(SK_DEFAULT_URL)

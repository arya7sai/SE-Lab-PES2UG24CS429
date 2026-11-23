import pytest
from bike_share_rental import ride_cost, dock_status, can_unlock


# Example test cases:
def test_standard_ride():
    assert ride_cost("standard", 45, False, False) == 40

def test_dock_available():
    assert dock_status(5, 10) == "available"


# ========== ride_cost tests ==========

def test_ride_cost_unknown_bike_type_raises():
    with pytest.raises(ValueError, match="unknown bike type"):
        ride_cost("tandem", 30, False, False)

def test_ride_cost_invalid_duration_zero_raises():
    with pytest.raises(ValueError, match="invalid duration"):
        ride_cost("standard", 0, False, False)

def test_ride_cost_invalid_duration_negative_raises():
    with pytest.raises(ValueError, match="invalid duration"):
        ride_cost("standard", -10, False, False)

# Non-subscriber, non-peak
def test_ride_cost_standard_30min_non_sub_non_peak():
    # 1 block * 20 = 20
    assert ride_cost("standard", 30, False, False) == 20

def test_ride_cost_standard_45min_non_sub_non_peak():
    # 2 blocks * 20 = 40
    assert ride_cost("standard", 45, False, False) == 40

def test_ride_cost_electric_30min_non_sub_non_peak():
    # 1 block * 35 = 35
    assert ride_cost("electric", 30, False, False) == 35

def test_ride_cost_cargo_30min_non_sub_non_peak():
    # 1 block * 50 = 50
    assert ride_cost("cargo", 30, False, False) == 50

# Subscriber (first block free)
def test_ride_cost_standard_30min_subscriber_non_peak():
    # 1 block - 1 free = 0 blocks = 0 cost
    assert ride_cost("standard", 30, True, False) == 0

def test_ride_cost_standard_45min_subscriber_non_peak():
    # 2 blocks - 1 free = 1 block * 20 = 20
    assert ride_cost("standard", 45, True, False) == 20

def test_ride_cost_standard_15min_subscriber_non_peak():
    # 1 block - 1 free = 0 blocks = 0 cost
    assert ride_cost("standard", 15, True, False) == 0

def test_ride_cost_electric_60min_subscriber_non_peak():
    # 2 blocks - 1 free = 1 block * 35 = 35
    assert ride_cost("electric", 60, True, False) == 35

# Peak pricing (non-cargo)
def test_ride_cost_standard_30min_non_sub_peak():
    # 1 block * 20 + 15 peak = 35
    assert ride_cost("standard", 30, False, True) == 35

def test_ride_cost_electric_30min_non_sub_peak():
    # 1 block * 35 + 15 peak = 50
    assert ride_cost("electric", 30, False, True) == 50

def test_ride_cost_standard_45min_subscriber_peak():
    # 2 blocks - 1 free = 1 * 20 + 15 peak = 35
    assert ride_cost("standard", 45, True, True) == 35

# Peak pricing - cargo (no peak surcharge)
def test_ride_cost_cargo_30min_non_sub_peak():
    # 1 block * 50, no peak surcharge for cargo = 50
    assert ride_cost("cargo", 30, False, True) == 50

def test_ride_cost_cargo_45min_subscriber_peak():
    # 2 blocks - 1 free = 1 * 50, no peak surcharge = 50
    assert ride_cost("cargo", 45, True, True) == 50

# Long ride surcharge (> 180 minutes)
def test_ride_cost_standard_200min_non_sub_non_peak():
    # 7 blocks * 20 + 100 = 240
    assert ride_cost("standard", 200, False, False) == 240

def test_ride_cost_electric_181min_subscriber_peak():
    # 7 blocks - 1 = 6 * 35 + 15 + 100 = 325
    assert ride_cost("electric", 181, True, True) == 325

def test_ride_cost_cargo_180min_exact_boundary():
    # 6 blocks * 50 = 300 (no surcharge at exactly 180)
    assert ride_cost("cargo", 180, False, False) == 300

def test_ride_cost_cargo_181min_surcharge():
    # 7 blocks * 50 + 100 = 450
    assert ride_cost("cargo", 181, False, False) == 450


# ========== dock_status tests ==========

def test_dock_status_invalid_capacity_zero_raises():
    with pytest.raises(ValueError, match="invalid capacity"):
        dock_status(5, 0)

def test_dock_status_invalid_capacity_negative_raises():
    with pytest.raises(ValueError, match="invalid capacity"):
        dock_status(5, -1)

def test_dock_status_invalid_bike_count_negative_raises():
    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(-1, 10)

def test_dock_status_invalid_bike_count_exceeds_capacity_raises():
    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(11, 10)

def test_dock_status_empty():
    assert dock_status(0, 10) == "empty"

def test_dock_status_full():
    assert dock_status(10, 10) == "full"

def test_dock_status_few_bikes_one():
    assert dock_status(1, 10) == "few bikes"

def test_dock_status_few_bikes_two():
    assert dock_status(2, 10) == "few bikes"

def test_dock_status_few_bikes_three_not_few():
    # 3 bikes is not <= 2, so not "few bikes"
    # 7 free slots > 2, so not "few slots"
    assert dock_status(3, 10) == "available"

def test_dock_status_few_slots_one():
    # 9 bikes docked, 1 free slot
    assert dock_status(9, 10) == "few slots"

def test_dock_status_few_slots_two():
    # 8 bikes docked, 2 free slots
    assert dock_status(8, 10) == "few slots"

def test_dock_status_few_slots_three_not_few():
    # 7 bikes docked, 3 free slots
    assert dock_status(7, 10) == "available"

def test_dock_status_available():
    assert dock_status(5, 10) == "available"

# Edge cases with small capacity
def test_dock_status_capacity_1_empty():
    assert dock_status(0, 1) == "empty"

def test_dock_status_capacity_1_full():
    assert dock_status(1, 1) == "full"

def test_dock_status_capacity_2_few_bikes():
    assert dock_status(1, 2) == "few bikes"

def test_dock_status_capacity_2_few_slots():
    assert dock_status(1, 2) == "few bikes"  # Also few bikes when 1 docked


# ========== can_unlock tests ==========

# Has active ride -> False
def test_can_unlock_has_active_ride_false():
    assert can_unlock(200, True, 25) == False

def test_can_unlock_has_active_ride_false_low_balance():
    assert can_unlock(0, True, 25) == False

# Age < 16 -> False
def test_can_unlock_age_15_false():
    assert can_unlock(200, False, 15) == False

def test_can_unlock_age_0_false():
    assert can_unlock(200, False, 0) == False

# Age 16-17 (need >= 100 balance)
def test_can_unlock_age_16_balance_100_true():
    assert can_unlock(100, False, 16) == True

def test_can_unlock_age_16_balance_99_false():
    assert can_unlock(99, False, 16) == False

def test_can_unlock_age_17_balance_150_true():
    assert can_unlock(150, False, 17) == True

def test_can_unlock_age_17_balance_50_false():
    assert can_unlock(50, False, 17) == False

# Age 18+ (need >= 50 balance)
def test_can_unlock_age_18_balance_50_true():
    assert can_unlock(50, False, 18) == True

def test_can_unlock_age_18_balance_49_false():
    assert can_unlock(49, False, 18) == False

def test_can_unlock_age_25_balance_100_true():
    assert can_unlock(100, False, 25) == True

def test_can_unlock_age_60_balance_0_false():
    assert can_unlock(0, False, 60) == False

# Boundary: age 18 exactly
def test_can_unlock_age_18_balance_100_true():
    assert can_unlock(100, False, 18) == True

# Combined: active ride overrides age/balance
def test_can_unlock_active_ride_overrides_high_balance():
    assert can_unlock(1000, True, 25) == False

def test_can_unlock_active_ride_overrides_adult():
    assert can_unlock(100, True, 18) == False

def test_can_unlock_active_ride_overrides_teen():
    assert can_unlock(200, True, 17) == False
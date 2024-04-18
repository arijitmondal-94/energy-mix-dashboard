from datetime import time

from utils.datetime_helper import time_to_isp


def test_time_to_isp_00_00() -> None:
    assert time_to_isp(time(0, 0)) == 48

def test_time_to_isp_00_30() -> None:
    assert time_to_isp(time(0, 30)) == 1

def test_time_to_isp_01_30() -> None:
    assert time_to_isp(time(1, 30)) == 3

def test_time_to_isp_10_30() -> None:
    assert time_to_isp(time(10, 30)) == 21
    
def test_time_to_isp_20_00() -> None:
    assert time_to_isp(time(20, 0)) == 40

def test_time_to_isp_23_30() -> None:
    assert time_to_isp(time(23, 30)) == 47
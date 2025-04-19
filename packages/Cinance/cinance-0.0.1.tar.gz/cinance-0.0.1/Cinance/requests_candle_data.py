# ! py
# copyright by Chinh

import requests, datetime, json 

# [1]
"""
    Lấy dữ liệu nến từ Binance cho coin theo phút.
    Args:
        symbol (str): mã coin (ví dụ: 'BTC').
        interval (str): khoảng thời gian (ví dụ: '1m', '5m').
        limit (int): số lượng nến cần lấy.
    Returns:
        list[dict]: danh sách nến với open, high, low, close, volume.
    Raises:
        ValueError: nếu tham số sai kiểu.
        RuntimeError: nếu gọi API thất bại hoặc dữ liệu không hợp lệ.
"""
# Lấy giá trong khoảng thời gian vài phút 
def get_candle_data_about_minutes(*, symbol: str, interval: str, limit: int):
    try:
        # Kiểm tra kiểu dữ liệu
        if not isinstance(symbol, str) or not isinstance(interval, str) or not isinstance(limit, int):
            raise ValueError("Sai kiểu dữ liệu: symbol và interval phải là str, limit phải là int.")
        symbol_pair = symbol.upper() + "USDT"
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol_pair,
            "interval": interval,
            "limit": limit
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  
        data = response.json()
        if not isinstance(data, list):
            raise RuntimeError("Dữ liệu trả về không hợp lệ từ Binance.")
        result = []
        for candle in data:
            result.append({
                "time": datetime.datetime.fromtimestamp(candle[0] / 1000).isoformat(),
                "open": float(candle[1]),
                "high": float(candle[2]),
                "low": float(candle[3]),
                "close": float(candle[4]),
                "volume": float(candle[5])
            })
        return result
    except requests.RequestException as e:
        raise RuntimeError(f"Lỗi khi kết nối đến Binance API: {e}")
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise RuntimeError(f"Đã xảy ra lỗi không xác định: {e}")

# [2]
"""
    Lấy cây nến gần nhất từ Binance cho coin trong khoảng thời gian nhất định.
    Args:
        symbol (str): mã coin (vd: 'BTC').
        interval (str): khoảng thời gian (vd: '1m', '5m').
        limit (int, optional): số nến cần lấy, mặc định là 1.
    Returns:
        dict: thông tin cây nến gần nhất gồm thời gian, open, high, low, close, volume.
    Raises:
        ValueError: nếu tham số sai kiểu.
        RuntimeError: nếu gọi API thất bại hoặc dữ liệu không hợp lệ.
    """    
# Lấy giá trong interval phút trước (chỉ lấy thông tin trong phút đó)
def get_candle_data_in_minute(*, symbol: str, interval: str, limit: int = 1):
    try:
        if not isinstance(symbol, str) or not isinstance(interval, str):
            raise ValueError("Sai kiểu dữ liệu: symbol và interval phải là str")

        symbol_pair = symbol.upper() + "USDT"
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol_pair,
            "interval": interval,
            "limit": limit
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data or not isinstance(data, list):
            raise RuntimeError("Không lấy được dữ liệu nến.")\
        # Lấy cây nến cuối cùng
        candle = data[-1]
        return {
            "time": datetime.datetime.fromtimestamp(candle[0] / 1000).isoformat(),
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
            "volume": float(candle[5])
        }
    except requests.RequestException as e:
        raise RuntimeError(f"Lỗi khi kết nối đến Binance API: {e}")
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise RuntimeError(f"Lỗi không xác định: {e}")

# [3]
"""
    Lấy thông tin thị trường (giá hiện tại, khối lượng) của một cặp coin.
    Args:
        symbol (str): mã coin (vd: 'BTC').
    Returns:
        dict: thông tin giá và khối lượng hiện tại.
    Raises:
        RuntimeError: nếu không lấy được dữ liệu từ API.
"""
# Lấy giá hiện tại của thị trường bản 24h
def get_candle_data_market(*, symbol: str):
    try:
        if not isinstance(symbol, str):
            raise ValueError("Sai kiểu dữ liệu: symbol phải là str.")

        symbol_pair = symbol.upper() + "USDT"
        url = f"https://api.binance.com/api/v3/ticker/24hr"
        params = {
            "symbol": symbol_pair
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "lastPrice" not in data or "volume" not in data:
            raise RuntimeError("Dữ liệu không hợp lệ từ Binance.")
        return {
            "price": float(data["lastPrice"]),
            "volume": float(data["volume"])
        }
    except requests.RequestException as e:
        raise RuntimeError(f"Lỗi khi kết nối đến Binance API: {e}")
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise RuntimeError(f"Lỗi không xác định: {e}")

# [4]
"""
    Lấy nến trong khoảng thời gian xác định từ Binance API.
    Args:
        symbol (str): mã coin (vd: 'BTC').
        interval (str): khoảng thời gian (vd: '1m', '5m').
        start_time (str): thời gian bắt đầu (ISO format).
        end_time (str): thời gian kết thúc (ISO format).
    Returns:
        list[dict]: danh sách nến trong khoảng thời gian đã cho.
    Raises:
        ValueError: nếu tham số sai kiểu.
        RuntimeError: nếu gọi API thất bại hoặc dữ liệu không hợp lệ.
    """
def get_candle_data_in_range(*, symbol: str, interval: str, start_time: str, end_time: str):
    try:
        if not isinstance(symbol, str) or not isinstance(interval, str):
            raise ValueError("Sai kiểu dữ liệu: symbol và interval phải là str, time phải theo định dạng YYYY-MM-DDTHH:MM:SS")
        symbol_pair = symbol.upper() + "USDT"
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol_pair,
            "interval": interval,
            "startTime": int(datetime.datetime.fromisoformat(start_time).timestamp() * 1000),
            "endTime": int(datetime.datetime.fromisoformat(end_time).timestamp() * 1000)
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        if not data or not isinstance(data, list):
            raise RuntimeError("Không lấy được dữ liệu nến.")
        result = []
        for candle in data:
            result.append({
                "time": datetime.datetime.fromtimestamp(candle[0] / 1000),
                "open": float(candle[1]),
                "high": float(candle[2]),
                "low": float(candle[3]),
                "close": float(candle[4]),
                "volume": float(candle[5])
            })
        return result
    except requests.RequestException as e:
        raise RuntimeError(f"Lỗi khi kết nối đến Binance API: {e}")
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise RuntimeError(f"Lỗi không xác định: {e}")

# [5]
"""
    Lấy thông tin chi tiết về một coin từ Binance.
    Args:
        symbol (str): mã coin (vd: 'BTC').
    Returns:
        dict: thông tin chi tiết về coin (min_price, max_price, v.v.).
    Raises:
        RuntimeError: nếu không lấy được dữ liệu từ API.
    """
# Lấy danh sách các cặp giao dịch
def get_symbol_list():
    try:
        url = "https://api.binance.com/api/v3/exchangeInfo"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "symbols" not in data:
            raise RuntimeError("Dữ liệu không hợp lệ từ Binance.")
        symbols = [symbol["symbol"] for symbol in data["symbols"] if symbol["status"] == "TRADING"]
        return symbols
    except requests.RequestException as e:
        raise RuntimeError(f"Lỗi khi kết nối đến Binance API: {e}")
    except Exception as e:
        raise RuntimeError(f"Lỗi không xác định: {e}")

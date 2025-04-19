from requests_candle_data import*

# [1] lấy giá trong khoảng thời gian (từ hiện tại -> quá khứ) 
data = get_candle_data_about_minutes(symbol="BTC", interval="1m", limit=10)
for candle in data:
    print(json.dumps(candle, indent=4))  

# [2] lấy giá trong 1 phút 
print(get_candle_data_in_minute(symbol="BTC", interval="1m"))     

# [3] lấy giá hiện tại của thị trường 
print(get_candle_data_market(symbol="BTC"))

# [4] Lấy giá trong khoảng phạm vi thời gian (quá khứ xa -> quá khứ gần)
data = get_candle_data_in_range(symbol="BTC", interval="1m", start_time="2025-04-19T01:00:00", end_time="2025-04-19T01:10:00")
for candle in data:
    print(json.dumps(candle, indent=4, default=str))

# [5] lấy danh sách cặp giao dịch
print(get_symbol_list())

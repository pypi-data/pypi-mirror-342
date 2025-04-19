# Cinance

Cinance là thư viện Python dùng để xem giá coin crypto theo khoảng thời gian nhất định 

## Cách cài đặt
```bash
pip install Cinance 
```

## Cách cập nhật
```bash
pip install --upgrade Cinance
```

## Cách sử dụng 

### [1] lấy giá trong khoảng thời gian (từ hiện tại -> quá khứ)  
```bash
from requests_candle_data import*
data = get_candle_data_about_minutes(symbol="BTC", interval="1m", limit=10)
for candle in data:
    print(json.dumps(candle, indent=4))  
```

### [2] lấy giá trong 1 phút
```bash 
print(get_candle_data_in_minute(symbol="BTC", interval="1m"))     
```

### [3] lấy giá hiện tại của thị trường 
```bash
print(get_candle_data_market(symbol="BTC"))
```

### [4] Lấy giá trong khoảng phạm vi thời gian (quá khứ xa -> quá khứ gần)
```bash
data = get_candle_data_in_range(symbol="BTC", interval="1m", start_time="2025-04-19T01:00:00", end_time="2025-04-19T01:10:00")
for candle in data:
    print(json.dumps(candle, indent=4, default=str))
```

### [5] lấy danh sách cặp giao dịch
```bash
print(get_symbol_list())
```

## Lời kết 
```bash
* Một số điểm chính:

-> Mô tả về thư viện và chức năng của nó
-> Mô tả cách sử dụng của mỗi hàm 
```

## CUỐI CÙNG CẢM ƠN CÁC BẠN ĐÃ TIN DÙNG THƯ VIỆN CỦA MÌNH
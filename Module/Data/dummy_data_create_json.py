import pandas as pd
import json
from datetime import datetime, timedelta
import numpy as np

output_file_path = input("결과파일 경로: ")
output_file_name = "etl_test_data_50.json"

activities = ['order_received', 'payment_check', 'inventory_scan', 'packing_start', 'shipping_ready']
resources = ['system_auto', 'user_admin', 'worker_01', 'worker_02', 'bot_alpha']
status_codes = [200, 201, 400, 404, 500]

np.random.seed(42)
data_size = 50

dummy_data_list = []
for i in range(data_size):
    start_time = datetime(2024, 3, 1, 9, 0) + timedelta(minutes=i*15)
    end_time = start_time + timedelta(minutes=10)
    
    record = {
        'case_id': f"C-{1000 + (i // 5)}",
        'event_id': f"E-{5000 + i}",
        'activity_name': activities[i % 5],
        'resource_id': np.random.choice(resources),
        'start_timestamp': start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_timestamp': end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'transaction_amount': round(float(np.random.uniform(10.5, 500.0)), 2),
        'status_code': int(np.random.choice(status_codes)),
        'is_error_flag': bool(np.random.choice([True, False])),
        'server_node_name': f"node_{np.random.randint(1, 4)}"
    }
    dummy_data_list.append(record)

with open(output_file_path+'/'+output_file_name, 'w', encoding='utf-8') as target_json_file:
    json.dump(dummy_data_list, target_json_file, indent=4, ensure_ascii=False)

print("작업 완료")
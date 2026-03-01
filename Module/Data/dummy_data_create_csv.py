import pandas as pd
import numpy as np
from datetime import datetime, timedelta

output_file_path = input("결과파일 경로: ")
output_file_name = "etl_test_data_50.csv"

activities = ['order_received', 'payment_check', 'inventory_scan', 'packing_start', 'shipping_ready']
resources = ['system_auto', 'user_admin', 'worker_01', 'worker_02', 'bot_alpha']
status_codes = [200, 201, 400, 404, 500]

np.random.seed(42) # 재현 가능하도록 시드 고정
data_size = 50

dummy_data = {
    'case_id': [f"C-{1000 + (i // 5)}" for i in range(data_size)], # 10개의 케이스가 각각 5개 활동
    'event_id': [f"E-{5000 + i}" for i in range(data_size)],
    'activity_name': [activities[i % 5] for i in range(data_size)],
    'resource_id': [np.random.choice(resources) for _ in range(data_size)],
    'start_timestamp': [datetime(2024, 3, 1, 9, 0) + timedelta(minutes=i*15) for i in range(data_size)],
    'end_timestamp': [datetime(2024, 3, 1, 9, 10) + timedelta(minutes=i*15) for i in range(data_size)],
    'transaction_amount': np.random.uniform(10.5, 500.0, size=data_size).round(2),
    'status_code': [np.random.choice(status_codes) for _ in range(data_size)],
    'is_error_flag': [True if x >= 400 else False for x in [np.random.choice(status_codes) for _ in range(data_size)]],
    'server_node_name': [f"node_{np.random.randint(1, 4)}" for _ in range(data_size)]
}

etl_test_df = pd.DataFrame(dummy_data)
etl_test_df.to_csv(output_file_path+'/'+output_file_name, index=False, encoding='utf-8-sig')

print("작업 완료")
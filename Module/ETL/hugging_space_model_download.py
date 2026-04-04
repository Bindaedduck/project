# hugginface 홈페이지 > files 목록과 일치
from huggingface_hub import snapshot_download

token = 

snapshot_download(
    repo_id="Qwen/Qwen3-Embedding-0.6B",  # 원하는 모델 이름
    local_dir=다운받을 경로,  # 원하는 저장 경로
    token=token
)

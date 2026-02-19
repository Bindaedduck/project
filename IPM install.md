## IBM Process Mining(IPM)
### [ Non Container ]
> Download
- [IPM - 2.1.0](https://partnerportal.ibm.com/s/software-access-catalog)
    - Part number: M0XLBML  
    - 다운 받은 파일 안에 ibmprocessmining-setup-2.1.0_924e3d4.tar.gz파일만 추출

- rhel-9.6-x86_64-wsl2.tar.gz
    - rhel 설치 파일

- rhel-9.6-x86_64-dvd.iso
    - IPM이 실행하기 위해 필요한 프로그램 설치 파일(Postgre, Python, Nginx)

> Steps
1. WSL가 설치되었다는 가정하에 RHEL 설치
    ```
    # C:\wsl\rhel : import 경로
    wsl --import RHEL C:\wsl\rhel [rhel-9.6-x86_64-wsl2.tar.gz 파일 경로] 
    ``` 

2. RHEL 접속
    ```
    wsl -d RHEL
    ```

3. IPM v2.1.0 설치
    ```
    # ibmprocessmining-setup-2.1.0_924e3d4.tar.gz 파일 opt폴더에 복사
    cp [ibmprocessmining-setup-2.1.0_924e3d4.tar.gz 파일 경로] /opt

    # IPM 설치
    cd /opt
    sudo tar xvf ibmprocessmining-setup-X.Y.Z.tar.gz 

    # PM_HOME 변수 설정
    export PM_HOME="/opt/processmining"
    ```

4. RHEL ISO파일 Mount
    ```
    # RHEL ISO를 저장할 폴더 생성
    sudo mkdir -p /opt/iso

    # rhel-9.6-x86_64-dvd.iso 파일 opt/iso 폴더에 복사
    cp [rhel-9.6-x86_64-dvd.iso 파일 경로] /opt/iso

    # Mount 지점 생성
    sudo mkdir -p /mnt/rhel9

    # RHEL ISO Mount
    sudo mount -o loop /opt/iso/rhel-9.6-x86_64-dvd.iso /mnt/rhel9
    ```

5. 로컬 레포지토리(저장소) 설정
    ```
    # 기존 온라인 설정 파일들은 백업
    sudo mkdir -p /etc/yum.repos.d/backup
    sudo mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/backup/ 2>/dev/null

    # 새로운 로컬 설정 파일 작성
    sudo vi /etc/yum.repos.d/local.repo

    # 로컬 설정 파일 내용
    [Local-BaseOS]
    name=RHEL 9.6 BaseOS
    baseurl=file:///mnt/rhel9/BaseOS
    enabled=1
    gpgcheck=0

    [Local-AppStream]
    name=RHEL 9.6 AppStream
    baseurl=file:///mnt/rhel9/AppStream
    enabled=1
    gpgcheck=0

    # 캐시 정리
    sudo dnf clean all

    # 로컬 설정 파일 내용에 대한 패키지 목록 확인
    sudo dnf repolist
    ```

6. PostgreSQL v16 설치
    ```
    # v16 스트림 활성화
    sudo dnf module enable postgresql:16 -y

    # v16 설치
    sudo dnf install -y postgresql-server

    # 확인
    postgres --version
    ```

7. Python v3.12 설치
8. Nginx 설치
9. Processmining 실행
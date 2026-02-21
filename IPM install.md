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
7. PostgreSQL 초기화 및 서비스 설정
    ```
    # 데이터베이스 초기화 (최초 1회 필수)
    sudo postgresql-setup --initdb

    # 서비스 시작 및 부팅 시 자동 실행 설정
    sudo systemctl enable --now postgresql

    # 서비스 상태 확인
    # active (running) : 실행중
    sudo systemctl status postgresql
    ```

8. PostgreSQL 기본 구성
    ```
    export POSTGRES_PROCESSMINER_PWD="비밀번호"
    export POSTGRES_PROCESSMINER_USER="processmining"
    export POSTGRES_PROCESSMINER_DATABASE="processmining"

    pushd /tmp
    sudo -E -u postgres createuser ${POSTGRES_PROCESSMINER_USER}
    sudo -E -u postgres createdb ${POSTGRES_PROCESSMINER_DATABASE}
    sudo -E -u postgres psql -c "alter user ${POSTGRES_PROCESSMINER_USER} with encrypted password '${POSTGRES_PROCESSMINER_PWD}';"
    sudo -E -u postgres psql -c "grant all privileges on database ${POSTGRES_PROCESSMINER_DATABASE} to ${POSTGRES_PROCESSMINER_USER};"
    sudo -E -u postgres psql -c "GRANT ALL ON ALL TABLES IN SCHEMA public TO ${POSTGRES_PROCESSMINER_USER}";
    sudo -E -u postgres psql -c "ALTER DATABASE ${POSTGRES_PROCESSMINER_DATABASE} OWNER TO ${POSTGRES_PROCESSMINER_USER}";
    popd
    ```
    ```
    # password 압호화
    # <PM_HOME>/utils/crypto-utils 사용
    # password에 '$'가 포함되는 경우 'password'로 입력
    ./crypt-utils.sh password
    ```
    ```
    # <PM_HOME>/etc/processmining.conf 수정
    # <encrypted database password> : 암호화된 password
    persistence: {
        jdbc: {
            database: "<database name>",
            host: "<database host>",
            port: <database port>,
            user: "<database user>",
            password: "<encrypted database password>" 
        }
    ...
    ```

    ```
    # <PM_HOME>/etc/accelerator-core.properties 수정
    # <encrypted database password> : 암호화된 password
    spring.datasource.database=<database name>
    spring.datasource.port=<database port>
    spring.datasource.host=<database host>
    spring.datasource.username=<database user>
    spring.datasource.password=<encrypted database password>
    ```
9. PostgreSQL 초기화
    ```
    # <PM_HOME>/utils/database-utils/postgres-utils.sh 실행
    ./postgres-utils.sh
    ```

10. Python v3.12 설치
    ```
    # 파이썬 본체, 패키지 관리자(pip), 개발용 라이브러리 설치
    sudo dnf install -y python3.12 python3.12-pip python3.12-devel
    ```
    - <PM_HOME>/bin/environment.conf > CMD_PYTHON 값이 /usr/bin/python3.12인지 확인

11. NGINX 설치
    ```
    # Nginx 설치
    sudo dnf install -y nginx
    ```

12. NGINX 서비스 설정
    ```
    # 서비스 시작 및 부팅 시 자동 실행 설정
    sudo systemctl enable --now nginx

    # 서비스 상태 확인
    # active (running) : 실행중
    systemctl status nginx
    ```

13. 방화벽 설정
    ```
    # HTTP, HTTPS 포트 허용
    sudo firewall-cmd --permanent --add-service=http
    sudo firewall-cmd --permanent --add-service=https

    # 방화벽 설정 적용
    sudo firewall-cmd --reload
    ```

14. NGINX 가상 호스트 구성
    ```
    mv /etc/nginx/conf.d/default.conf /etc/nginx/confd/default_origin.conf
    cp <PM_HOME>/nginx/processmining.conf /etc/nginx/conf.d/default.conf
    ```

15. NGINX SSL 구성
    ```
    mkdir /etc/nginx/ssl

    cp /home/pm/cert/server.* /etc/nginx/ssl/

    # /etc/nginx/conf.d/default.conf > ssl_certificate, ssl_certificate_key 경로 수정
    ssl_certificate /etc/nginx/ssl/server.pem;
    ssl_certificate_key /etc/nginx/ssl/server.key;

    # NGINX 테스트 및 재시작
    nginx -T
    systemctl restart nginx
    ```

16. Disable data-derived end-activities
    ```
    # <PM_HOME>/etc/processmining.conf > engine.defaults 섹션에 endActivity 속성 추가
    engine: {
    defaults: {
    ...
    endActivity:{
    enable: false
    },
    ....
    }
    }
    ```

17. Creating a private key and a public key for process ap
    ```
    <PM_HOME>/utils/generateKeyPair.sh
    ```

18. Processmining 서비스 실행
    ```
    cd <PM_HOME>/bin/
    ./pm-monet.sh start | stop
    ./pm-web.sh start | stop
    ./pm-engine.sh start | stop
    ./pm-analytics.sh start | stop
    ./pm-accelerators.sh start | stop
    ./pm-brm.sh start | stop
    ./pm-monitoring.sh start | stop
    ```

19. Processmining 초기 Admin
    - 사용자 이름 : maintenance.admin
    - 비밀번호 : pmAdmin$1
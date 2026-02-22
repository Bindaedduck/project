## ipm.sh를 ~ 위치에 저장 후 ~/ipm.sh start | stop

# PM_HOME 경로 설정 
PM_HOME="/opt/processmining"
BIN_DIR="$PM_HOME/bin"

# 서비스 리스트 
SERVICES=("pm-monet" "pm-web" "pm-engine" "pm-analytics" "pm-accelerators" "pm-brm" "pm-monitoring")

case "$1" in
    start)
        echo "🚀 [Starting IPM Services...]"
        cd "$BIN_DIR" || exit
        for svc in "${SERVICES[@]}"; do
            echo "-> Starting $svc..."
            ./"$svc".sh start
            sleep 2 # 서비스 안정화를 위한 짧은 대기
        done
        echo "✅ All services started!"
        ;;
    stop)
        echo "🛑 [Stopping IPM Services...]"
        cd "$BIN_DIR" || exit
        # 중지는 역순
        for ((i=${#SERVICES[@]}-1; i>=0; i--)); do
            echo "-> Stopping ${SERVICES[$i]}..."
            ./"${SERVICES[$i]}".sh stop
        done
        echo "💤 All services stopped!"
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
        ;;
esac

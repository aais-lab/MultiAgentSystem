cd "$(dirname "$0")" && cd MAS

RUN=`osascript -e 'tell application "System Events" to get name of (processes where background only is false)' | grep -c 'Docker Desktop'`

if [ ${RUN} = 0 ]; then
    echo "Docker Desktop is not Started."

    # Dockerがリソースセーバーモードで起動している場合
    DOCER_PROCESS_COUNT=`ps aux | grep docker | grep -v grep | wc -l`
    if [ ${DOCER_PROCESS_COUNT} -gt 0 ]; then
        echo "Docker kernel is run Resource Saver Mode... "
        pkill -KILL -f Docker
        pkill -KILL -f docker
        echo "Docker application killed."
    fi

    open -g -a /Applications/Docker.app

    # 全てのプロセスの起動を待つ
    DOCER_PROCESS_COUNT=`ps aux | grep docker | grep -v grep | wc -l`
    until [ ${DOCER_PROCESS_COUNT} -ge 6 ]
    do
        sleep 1
        echo "Preparing to launch Docker Desktop ..."
        DOCER_PROCESS_COUNT=`ps aux | grep docker | grep -v grep | wc -l`
    done
    sleep 5
    echo "Docker Desktop is running..."
else
    echo "Docker Desktop is running..."
fi

./StartRedisDocker.command
python MAS.py
osascript ./CloseTerminal.scpt
./StopRedisDocker.command
pkill -KILL -f Docker
pkill -KILL -f docker

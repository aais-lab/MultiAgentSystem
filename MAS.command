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
    until [ ${RUN} = 1 ]
    do
        sleep 1
        echo "Preparing to launch Docker Desktop ..."
        RUN=`osascript -e 'tell application "System Events" to get name of (processes where background only is false)' | grep -c 'Docker Desktop'`
    done
    sleep 5
    echo "Docker Desktop is running..."
else
    echo "Docker Desktop is running..."
fi

./StartRedisDocker.command
python MAS.py
./StopRedisDocker.command

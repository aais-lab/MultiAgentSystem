cd "$(dirname "$0")" && cd MAS

RUN=`osascript -e 'tell application "System Events" to get name of (processes where background only is false)' | grep -c 'Docker Desktop'`

if [ ${RUN} = 0 ]; then
    echo "Docker Desktop is not Started."
    open -g -a /Applications/Docker.app
    echo "Docker Desktop is running..."
else
    echo "Docker Desktop is running..."
fi

./StartRedisDocker.command
python MAS.py
./StopRedisDocker.command

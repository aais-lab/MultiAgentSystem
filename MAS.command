cd "$(dirname "$0")" && cd MAS
./StartRedisDocker.command
python MAS.py
./StopRedisDocker.command

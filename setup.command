echo 'Start Setup'
echo '----------------------------------------------'
cd "$(dirname "$0")"
xattr -d com.apple.quarantine ./MAS.command
chmod +x ./MAS.command
cd MAS
xattr -d com.apple.quarantine ./StartMAS.command
xattr -d com.apple.quarantine ./StartRedisDocker.command
xattr -d com.apple.quarantine ./StopRedisDocker.command
xattr -d com.apple.quarantine ./CloseTerminal.scpt
chmod +x ./StartMAS.command
chmod +x ./StartRedisDocker.command
chmod +x ./StopRedisDocker.command
pip install -r requirements.txt
pip install --upgrade frozendict
pip install -r requirements.txt
pip install --upgrade frozendict
echo '----------------------------------------------'
echo 'Multi Agent System Setup Process finished'

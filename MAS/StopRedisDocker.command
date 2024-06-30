# シェルスクリプトが存在するディレクトリに移動
cd "$(dirname "$0")"

# Docker Composeを使ってRedisコンテナを停止
docker-compose stop

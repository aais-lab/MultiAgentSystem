# シェルスクリプトが存在するディレクトリに移動
cd "$(dirname "$0")"

# Docker Composeを使ってRedisコンテナを起動
docker-compose up -d

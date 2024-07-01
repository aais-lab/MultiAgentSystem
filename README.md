# MultiAgentSystem

## Overview
千葉工業大学 知能メディア工学科の第5セメスター「マルチエージェントシステム」において使用される、マルチエージェントシステム演習用ライブラリです。

## Requirement
### 必要環境
- MacOS
- DockerDesktop
- Python3.10.5 <
- 必要ライブラリ
  - experta >= 1.9.4
  - paho-mqtt >= 1.6.1
  - redis >= 5.0.1
  - schema >= 0.6.7

### 開発・動作確認環境
- MacOS
- Python
  - brew + pyenv
  - 3.10.5 <
  - 3.11.6 >=
- ライブラリ
  - experta >= 1.9.4
  - paho-mqtt >= 1.6.1
  - redis >= 5.0.1
  - schema >= 0.6.7

## Usage
### 導入方法
#### DockerDesktopのインストール
[DockerDesktopダウンロードページ](https://docs.docker.jp/desktop/install/mac-install.html)
#### gitからクローン
```
git clone https://github.com/aais-lab/MultiAgentSystem.git
```
### 初回実行前
#### 実行権限の付与
```
cd MultiAgentSystem
xattr -d com.apple.quarantine ./setup.command
```
#### 初回セットアップ
setup.commandをダブルクリックして実行する。

### システム実行
#### DockerDesktopを起動
#### MAS.commandをダブルクリックして実行

## Author
[KoheiAsaoka](https://github.com/asaoka-zemi)

[NaoYamanouchi](https://github.com/ClairdelunaEve)

## Licence
BSD-3-Clause license

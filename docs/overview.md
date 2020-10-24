# Kubernetes の概要

Kubernetesの概要を、`docker-compose`をスタートにして説明します。

## `docker-compose`

(demo. ローカルでdocker-compose。構成は簡単にCentOSのアプリがGETに対して返すだけ)

`docker-compose`は、これだけでもかなりいいもの。優れている。

- restart
- 動的な変更
- networking

ここで、EC2で`docker-compose`でdockerを動かすときの課題

- 可用性確保の困難さがある
  - docker-composeは、一つのVMの中で動かさなきゃ行けない。冗長性を考慮して複数のVMからなるクラスター構成にしようとしても、Nginx, Keepalived(ipvs), percona, zookeeperなどの、クラスター管理ツールを導入しなければならない。これはオンプレでやっているのと変わらない。
- EC2のVMの面倒をみなければならない
  - EC2のVMのカーネルに脆弱性が出た場合、カーネルアップデートをしなければならない。これ、既にサービスが動いているときだと、かなりリスクある。EC2をもう一台立てて、
  - ログの肥大化を気にしたりだとか、VMにログインして諸々操作することから、VMへのアクセス経路や、そのセキュリティも考慮しなければならない。

## Kubernetesでの解決

### Kubernetesとは

コンテナオーケストレーターと呼ばれるもの。つまりコンテナを動かせる環境。実態は、しかるべきアプリがインストールされたVMの集まり。

demo

- ekscliでクラスターを作る。
- 出来上がったクラスターのNodeをみる。WorkerNodeの数を数える。
- 同じdeployment.yamlをapplyする。
- すぐにインターネット上で利用できるようになることを確認する。

### docker-composeの良いところを引き継いでいる

- 宣言的(start, stop)
- 動的な変更
- networking

### docker-composeの課題を解消している

例えば可用性について

demo

- 一度VMを削除してみる。-> また立ち上がることを確認する
- VMを削除してみる -> どこかで勝手に立ち上がることを確認する

-> 簡単に可用性の確保ができた

例えばNodeの扱いについて

- EKSだと、Nodeにログインできない。ログインする用事がないので。

## さらに抜粋

Updateのしやすさ。ローリングアップデート
-> サービスを止めずに、安全にアップデートを行う

EKSだと特に、リソースの自動調整を行うことができる

ログ管理どうするも、サイドカーパターンで解決

blue/green deployment, Canary Release -> Istioでできる。

カオスエンジニアリング、これはやったことがないけど、サービスの継続性を見るのにちょうどいい

-> これらがあるのは、KubernetesやCloudNativeのmの盛り上がりにある。

ちょっと前はSwarmやMesosがあった。でも、今はKubernetesがデファクトになった。エコシステムが盛り上がって、Kubernetesで面倒なyamlの管理や、microseviceのツールも出てきている。

## Kubernetesに不向きなこと

オンプレはやめたほうがいい。

Kubernetesを自前で作って管理するのは、管理コストのほうが高くなって意味がない。これならdocker-composeにすべき。逆にクラウドならdocker-composeは貧弱すぎてだめ。
# Kubernetes の概要

Kubernetesの概要を、`docker-compose`をスタートにして説明。

## `docker-compose`

`docker-compose`は、これだけでもかなりいいもの。優れている。

- restart
- 動的な変更
- networking

ここで、EC2で`docker-compose`でdockerを動かすときの課題

- 可用性確保の困難さがある
  - docker-composeは、一つのVMの中で動かさなきゃ行けない。冗長性を考慮して複数のVMからなるクラスター構成にしようとしても、Nginx, Keepalived(ipvs), percona, zookeeperなどの、クラスター管理ツールを導入しなければならない。これはオンプレでやっているのと変わらない。
- EC2やELBのVMの面倒をみなければならない
  - EC2のVMのカーネルに脆弱性が出た場合、カーネルアップデートをしなければならない。これ、既にサービスが動いているときだと、かなりリスクある。EC2をもう一台立てて、
  - ログの肥大化を気にしたりだとか、VMにログインして諸々操作することから、VMへのアクセス経路や、そのセキュリティも考慮しなければならない。
  - ELBの設定の手間がある。特に拡張しようとバックエンドのアプリを一つ増やすときに、ELBの設定をしなければならない。

## Kubernetesでの解決

### Kubernetesとは

コンテナオーケストレーターと呼ばれるもの。つまりコンテナを動かせる環境。実態は、しかるべきアプリがインストールされたVM(EC2)の集まり。

demo

- ekscliでクラスターを作る。
- 出来上がったクラスターのNodeをみる。WorkerNodeの数を数える。
- 同じdeployment.yamlをapplyする。
- すぐにインターネット上で利用できるようになることを確認する。

## 最初にdocker-composeをカバーしていることに

ファイルをデプロイする。-> これだけで何が起きているか

- containerが動く
- LBがデプロイされる
- globalIPがついて、プロキシの設定まで行われる

この時点でdocker-composeに比べて優位性がある

- `docker-compose up -d`に近いオペレーション。簡単。
- EC2にログインしてdockerをインストールする、という手間が必要ない。そもそもEC2の面倒をみなくてもいい。EC2の面倒は私たちの管轄外。
- ログインやアクセス経路に関するセキュリティの考慮をする必要がなくなる。
- docker-composeの場合、グローバルに公開するときに、ELBを明示的に設定する必要がある。そうしなくても、kubernetes上でこれができる。

## docker-composeよりさらに優位なこと

### 負荷分散と冗長性

準備

- curlで繰り返し
- get po を繰り返し


デプロイメントのreplicasを3にする

ここで優位性がある

- docker-composeの場合、ELBのプロキシ設定は自分で頑張る必要があるが、それも必要ない。勝手に理想的な状態になってくれる。

podを一つ止めてみる。

- 再開する

nodeを減らす

```bash
eksctl scale nodegroup --cluster=demo -r us-west-1 --nodes=2 --nodes-min=1  ng-0e5d60b0
```
### Update

updateしてみる。ちょっとreturnを変更して。

```bash
docker build -t kenchaaan/k8sintro-python:1.0.2 . && docker push kenchaaan k8sintro-python 
```

そして、dockerhubをみてみる

そして、versionのタグを変更してみ

- サービスが止まらないまま、徐々に新しいバージョンに移行している

また動かないやつにしてみる。

そしてtagを変更してみる

- サービスは止まらない

### そのほか

- fargate: 勝手にノードが増減する
- EKSで動けば、Azureでも動く。以前はそういう仕事をしていた。
- cronjob
- ロギング -> sidecar patternというテンプレ構成. cloudwatchも使える
- metric -> これもsidecar
- microservice
- CI/CD Argo, Travis-CI, Blue/Green Deployment, Canary Release -> Istio
- CNCF https://landscape.cncf.io/ 盛り上がりが違う
- Chaos Engineering

- kubernetes以外の選択肢
  - Swarm, Mesos -> 負けた。まずpublic cloud が全部kubernetes, VMwareもkubernetesにかけてる。

- 事例
  - 調べりゃわんさか出てくる


## kubernetesがはまらないところ

- オンプレでk8sはやる意味なし. docker-composeにする。RancherやOpenShift, Tanzuなどがあるが、自分でやる意味なし。
- Storageの扱いは注意。Operatorを使うか、そもそもStatefulなものは外に出す。

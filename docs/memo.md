# EKSでクラスターを作る方法

`eksctl`をインストール

https://docs.aws.amazon.com/ja_jp/eks/latest/userguide/getting-started-eksctl.html

`kubectl`をインストール

cluster 作成

```bash
eksctl create cluster \
  --name my-cluster \
  --version 1.17
```

```bash
kubectl get node
```

-> ec2が立ち上がっていることがわかる

scale 

nodegroupを作成する

```bash
eksctl create nodegroup --cluster=demo -r us-west-1
```

nodegroupの名前をget

```bash
eksctl get nodegroup --cluster=demo -r us-west-1
```

これでnodegroupができたので、これをスケールする

```bash
eksctl scale nodegroup --cluster=demo -r us-west-1 --nodes=3 --nodes-max=3 ng-0e5d60b0
```

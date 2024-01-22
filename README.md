# MultiPipeline FrameWork
キューベースの並列処理用フレームワーク

以下のようにパイプラインアーキテクチャを効率的に実装し、並列処理を簡単かつ効率的に行うことが出来ます。
![proj_image1](multipipeline_queue_test.png)

特徴
それぞれのプロセスがステートマシンのように非同期で並列実行される為、あらゆるアーキテクチャに対応しリソースを最大限に利用したアプリケーションを実行することが出来ます。
ステートマシンを利用しているので常駐型かつ大規模アプリケーションに向いています。
multiprocessingのPoolよりも効率的にリソースを利用でき、Processよりも簡単にシステムの実装を行うことが出来ます。

アプリケーション例
・データ処理のためのリアルタイムサーバーアプリケーション
・アプリケーションベースの簡易ネットワークシミュレーター
・ネットワークを利用したクラスタアプリケーション

プロセス間の時間を計測することによって待ち行列理論を適用することが出来き、簡単にチューニングを行うことも可能。

# Requirement
anaconda
multiprocessing
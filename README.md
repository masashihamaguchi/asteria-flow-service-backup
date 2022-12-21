# asteria flow service backup

## Overview

Asteriaのフローファイルを一括でリモートリポジトリにバックアップするためのプログラムです。

このプログラムを定期実行することで、フローファイルとスケジュール設定ファイルなどの定期バックアップを行うことができます。


## Usage

#### 1. 任意の場所にプロジェクトをクローンします

#### 2. Pythonパッケージをインストールします
```bash
$ pip install -r requirements.txt
```

#### 3. リモートリポジトリの設定

バックアップを行うリモートリポジトリを用意します。

リモートリポジトリとの接続はSSH等で設定をすることをおすすめします。

#### 4. 環境変数を設定します

`.env.example`をコピーして`.env`にファイル名を変更してください。
リモートリポジトリ、フローファイルが保存されているディレクトリ、バックアップを行うAsteriaのユーザーを設定してください。

|    variable    | required | description                                              |
|:--------------:|:--------:|:---------------------------------------------------------|
| REPOSITORY_URL |    ○     | リモートリポジトリのURL                                            |
|  ORIGINAL_DIR  |    ○     | Asteria Warpのフローデータが保存されているディレクトリ                        |
|   BACKUP_DIR   |          | カスタマイズファイルを保存するディレクトリ<br>**※通常は変更しなくて大丈夫です。**            |
|  BACKUP_USER   |    ○     | バックアップを行うAsteriaユーザー<br>※複数ユーザーを指定する場合は","で区切って指定してください。 |

`BACKUP_DIR`は通常は変更しないでください。変更する場合は`.gitignore`も変更してください。

#### 5. `main.py`を実行する

`main.py`を実行して正しくバックアップが行われることを確認してください。

```bash
$ python main.py
```

リモートリポジトリにpushを行わない場合は、コマンドの最後に`local`をつけます。

```bash
$ python main.py local
```

定期実行を行う場合は、実行環境に合わせて設定を行ってください。

## Note

初期設定ではプロジェクトフォルダの中の`backup`ディレクトリにフローファイルが保存されてgitで管理されるようになっています。

特別な理由がない限りは変更しないことをおすすめします。

※プロジェクトフォルダと同じディレクトリを指定すると、リモートリポジトリへのPushができなくなってしまうので注意してください。

## Author

Masashi Hamaguchi<br>
masashi.hamaguchi@keio.jp

## License

The source code is licensed MIT.<br>
https://opensource.org/licenses/mit-license.php

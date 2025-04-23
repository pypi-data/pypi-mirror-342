# リソースアプリ API 保護ライブラリ

認証機能を提供するライブラリ。  
認証部分を別で起動しているアプリケーションで行い、リソースアプリの API の保護を実装するためのライブラリである。

## 利用方法

### 1. pip で本ライブラリをインストールする

```bash
pip install teppen-fastauth
```

### 2. 環境変数を設定する

| 環境変数名        | 説明                                                    | 必須 or 任意 | デフォルト値 | 例                           |
| ----------------- | ------------------------------------------------------- | ------------ | ------------ | ---------------------------- |
| HOST_RESOURCE_APP | リソースアプリのホスト名                                | 必須         | -            | resource-app.test.com        |
| JWKS_ENDPOINT     | 認証アプリが提供している JWKS の API エンドポイント URL | 必須         | -            | http://nginx/api/tokens/jwks |

### 3. プログラムに組み込む

保護したい API の関数の引数に`payload: PayloadV2 = Depends(decode_v2)`を追加すれば、保護が可能。  
実際の最小のプログラムは以下の通り。

```py
from fastapi import FastAPI, Depends
from fastauth import PayloadV2, decode_v2

app = FastAPI()

@app.get("/")
def root(payload: PayloadV2 = Depends(decode_v2)):
    return {"message": "Hello World"}
```

このライブラリは、HTTP ヘッダーに含まれる Bearer トークンにて認証確認を行う。  
そのため、トークンの受け渡しのために、フロントエンド側のプログラムが必要。  
これに関してもライブラリ化しているため、そちらを利用されたし。



## システムユーザーを用いたシステム自体の認証

```python

import os

os.environ["JWKS_ENDPOINT"] = "http://nginx/api/tokens/jwks"
os.environ["HOST_RESOURCE_APP"] = "test"

from fastauth import AuthClientV2

client = AuthClientV2(access_key="SYSUSER-ACCESS-KEY-bp57zl5JbEzOSBinVKkXUghuH7zhb367SDAPMHwkjSAA9rAhPAFJUZ3JOHsHG8ECBCZ6KK0DPYXsOZIwoUgOsgZV5OOHnwvf9XMEVLuAknGd8")

client.get("http://nginx:81/api/cars/3")

```
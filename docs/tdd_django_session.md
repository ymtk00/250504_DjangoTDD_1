# Django TDDセッション記録

## 概要

このドキュメントは、2025年5月4日に実施したDjangoプロジェクトでのテスト駆動開発（TDD）セッションの記録です。このセッションでは、Djangoプロジェクトの設定、モデルの作成、テストの実装、およびGitを使用したバージョン管理を行いました。

## 実施内容

### 1. 環境セットアップ

- Djangoプロジェクト（myproject）の作成
- coreアプリケーションの追加
- pytest環境の設定（pytest.ini）

### 2. モデル実装

- `Item`モデルの作成
  ```python
  class Item(models.Model):
      name = models.CharField(max_length=100)

      def __str__(self) -> str:
          return self.name
  ```

### 3. ユーティリティ関数の実装

- シンプルな加算関数の実装
  ```python
  def add(x:int, y:int) -> int:
      return x + y
  ```

### 4. テスト実装

#### Django標準テスト（TestCase）

```python
from django.test import TestCase
from core.utils import add

class AddTest(TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)
```

#### pytestスタイルのテスト

- モデルテスト
  ```python
  import pytest
  from core.models import Item

  @pytest.mark.django_db
  def test_item_crud():
      apple = Item.objects.create(name="Apple")
      fetched = Item.objects.get(name="Apple")
      assert fetched == apple
  ```

- ユーティリティテスト
  ```python
  from core.utils import add

  def test_add():
      assert add(1, 2) == 3
      assert add(-1, 1) == 0
  ```

### 5. マイグレーション

- マイグレーションファイルの作成
  ```bash
  py manage.py makemigrations
  ```

- マイグレーションの適用
  ```bash
  py manage.py migrate
  ```

### 6. テスト実行

- Django標準テスト
  ```bash
  py manage.py test
  ```

- pytestによるテスト
  ```bash
  pytest
  ```

### 7. バージョン管理

- 変更をステージング
  ```bash
  git add .
  ```

- コミット
  ```bash
  git commit -m "feat: TDDアプローチでDjangoプロジェクトを実装"
  ```

- リモートリポジトリへのプッシュ
  ```bash
  git push origin main
  ```

## 発生した問題と解決策

### 1. pytestの設定問題

**問題**: pytestの実行時に「no tests ran in 0.00s ERROR: file or directory not found: #」というエラーが発生。

**原因**: pytest.iniファイル内のコメントが不適切な位置にあり、テスト対象として解釈されていた。

**解決策**: コメントを独立した行に移動。
```ini
[pytest]
DJANGO_SETTINGS_MODULE = myproject.settings
python_files = test_*.py
addopts = -ra -q
# 失敗詳細を簡潔に、進捗バー非表示
```

### 2. データベーステーブルの不在

**問題**: テスト実行時に「django.db.utils.OperationalError: no such table: core_item」というエラーが発生。

**原因**: モデルは定義されていたが、マイグレーションが実行されていなかった。

**解決策**: マイグレーションの作成と適用。
```bash
py manage.py makemigrations
py manage.py migrate
```

## 得られた知見

1. **INIファイルの書式**: INIファイルではコメントは独立した行に記述する必要がある。

2. **Djangoのテスト環境**: 
   - Django標準のテストフレームワーク（TestCase）とpytestを併用できる
   - pytestを使用する場合は、適切な設定（pytest.ini）が必要

3. **マイグレーションの重要性**:
   - モデルを定義しただけでは不十分
   - テストを実行する前にマイグレーションを適用する必要がある

4. **TDDのワークフロー**:
   1. テストの作成
   2. テストの失敗確認
   3. 最小限の実装
   4. テストの成功確認
   5. リファクタリング

## 次のステップ

1. より複雑なモデル関係の実装（ForeignKey, ManyToMany）
2. ビューとテンプレートの実装とテスト
3. フォームのバリデーションテスト
4. APIエンドポイントの実装とテスト

## まとめ

このセッションでは、Djangoプロジェクトにおけるテスト駆動開発の基本的なワークフローを実践しました。モデルの定義、テストの作成、実装、そしてテストの実行という一連の流れを通じて、TDDの利点を体験することができました。また、pytestとDjango標準のテストフレームワークの両方を使用することで、それぞれの特徴と利点を理解することができました。

## CI/CD環境の構築（2025年5月4日追加）

### 1. GitHub Actionsの設定

GitHub Actionsを使用して継続的インテグレーション（CI）環境を構築しました。以下の設定を行いました：

#### ワークフローファイルの作成

`.github/workflows/django-test.yml`ファイルを作成し、以下の設定を行いました：

```yaml
name: Django Test

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'

    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run Tests
      run: |
        pytest
```

### 2. 実装内容の解説

- **トリガー設定**: `main`ブランチへのプッシュとプルリクエストでワークフローを実行
- **実行環境**: Ubuntu最新版
- **Python環境**: Python 3.12を使用
- **依存関係のインストール**: pip経由でrequirements.txtに記載されたパッケージをインストール
- **テスト実行**: pytestを使用してテストを実行

### 3. 発生した問題と解決策

#### 1. Codecovへのアップロード問題

**問題**: Codecov（コードカバレッジ分析サービス）へのカバレッジレポートアップロード時にレート制限エラーが発生。

```
Rate limit reached. Please upload with the Codecov repository upload token to resolve issue.
```

**原因**: Codecovのレート制限に達した、またはトークンが設定されていなかった。

**解決策**: カバレッジレポートのアップロード機能を一時的に無効化。将来的には以下の対応が必要：
- Codecovアカウントの作成
- リポジトリトークンの取得
- GitHub Secretsへのトークン登録
- ワークフローファイルでのトークン使用

#### 2. タイプミスの発見

**問題**: ワークフローファイルに`runs-one`というタイプミスがあった。

**原因**: 単純な入力ミス。

**解決策**: 正しい構文である`runs-on`に修正。

### 4. 得られた知見

1. **GitHub Actionsの基本構造**:
   - `name`: ワークフロー名
   - `on`: トリガーイベント
   - `jobs`: 実行するジョブ
   - `steps`: ジョブ内の手順

2. **マトリックスビルドとシングルビルドの選択**:
   - 複数環境でのテストが必要な場合はマトリックスビルド
   - 単一環境で十分な場合はシンプルな設定が効率的

3. **外部サービス連携時の注意点**:
   - Codecovなどの外部サービスを使用する場合、適切な認証情報が必要
   - レート制限などのサービス側の制約を考慮する必要がある

4. **CI環境の段階的構築**:
   - 基本的なテスト実行から始め、徐々に機能を追加するアプローチが効果的
   - 問題が発生した場合は、一時的に機能を無効化して基本機能を確保

### 5. 次のステップ（CI/CD関連）

1. **Codecov連携の正式実装**:
   - トークンを取得して適切に設定
   - カバレッジレポートの分析と可視化

2. **デプロイ自動化**:
   - テスト成功後の自動デプロイ設定
   - ステージング環境と本番環境の分離

3. **テスト拡充**:
   - 統合テストの追加
   - パフォーマンステストの実装

4. **セキュリティスキャン**:
   - 依存パッケージの脆弱性チェック
   - コードの静的解析

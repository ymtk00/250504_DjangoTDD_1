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

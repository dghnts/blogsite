# Djangoでwebアプリ開発　作業手順

## 実行環境


## 作業手順

### 11月30日
- [x] ヘッダーの作成（ロゴやタイトルなど）
- [x] 各ページの作成(ホーム，新規作成ページ、記事の個別ページ)
- [x] LoginRequiredMixinの実装
- [ ] カテゴリ検索機能の実装

### 12月1日
- [x] カテゴリ検索機能の実装

### 12月2日
- [] カテゴリ検索の実装
    - [x] context_processorの実装
    - [ ] index viewに検索機能を実装する（検索した内容はindexで処理される（
    - [x] ページネーションの実装 

### 12月3日
- [x] タグの削除<= article_tagだけで十分な気がする
- [ ] 検索ウインドウの変更 <=　タイトル検索と詳細検索に変更
-[x] タイトル検索機能の実装
    - [ ] 詳細検索機能の実装
        - [x] modalの作成
        - [x] カテゴリ検索機能の実装 [(参考：Djangoでクエリビルダを使い、スペース区切りの文字列検索と絞り込みを同時に行う【JSとカスタムテンプレートタグを使用】)](https://noauto-nolife.com/post/django-search-querybuilder-custom-templates-js/)
        - [x] タグ検索機能の実装
        - [x] GETメソッドで空のパラメータを送信しない [【JavaScript】formのGETメソッドで空のinputパラメータを送信しないようにする](https://into-the-program.com/javascript-dont-submit-empty-input-parameter-get-method-form/) 
        - [x] 検索機能のレイアウトを変更

### 12月4日
- [x] タイトル検索機能の不具合を修正（検索keywordが半角スペースで途切れる問題）

### 12月5日
- [x] 記事の新規作成ページの不具合を修正 

### 12月7日
- [x] followmodelの名前の変更
- [x] urlの末尾に/を追加
- [x] mypageのテンプレート・viewの作成・レンダリングの確認
- [x] mypageにフォロー/フォロワーの表示を追加 

### 12月8日
- [x] follow機能の実装（ユーザーページからフォロー/フォロー解除できるように設定）
- [x] mypageにフォロー/フォロー解除機能の実装
- [x] timeline,followingページの実装

### 12月9日
- [x] followユーザーの記事一覧ページを作成
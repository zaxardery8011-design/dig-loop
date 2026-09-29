# AGENTS.md — 給使用者的 AI

> 這份是給 **AI** 讀的。人類封面在 `README.md`。使用者把這個 repo 丟過來，是要你先讀懂，再依 README 幫他架起來。

## 這是什麼

`dig-loop`（挖洞迴圈）是一份給新手的範本（template）：讓雲端 AI bot 每天固定去一個領域挖還沒被解決的問題，對已解清單（solved list）過濾後寫進產出庫，再收回本機核對檔頭（header）。適合想用排程 bot 持續挖題、又要把結果收到本機判斷值不值得做的人。

## 幫使用者架起來

步驟以 `README.md` 為準，這裡不另寫一份。

- 從零設定：README「從零設定（八步）」
- 收回本機：README「本機收件」

例行題、已解清單、產出路徑、檔頭規則都以 README 為準。缺帳號、repo、金鑰時問使用者，不要自己填假值。

## 驗收怎麼算

本機整夾核對：

```
python tools/verify_all.py inbox/dig
```

該資料夾裡每個 `*.md` 都印 `OK`、離開碼 0，才算通。有任一 `MISMATCH`，或離開碼不是 0，都還沒通。單檔可用 `python tools/verify_header.py <檔>`。

## 已知限制

照 README「已驗證到哪」原文：

- 2026-09-29 20:44：Grok Bot 照本範本寫一格，進私有測試庫 `dig-loop-selftest` 的 `inbox/dig/20260929_DEMO_r1c1.md`（commit `f6d0b58`）。`tools/verify_header.py` 驗為 OK。
- Routines 的點擊路徑，以及 OAuth 的精確 scope，是 bot 自述，未獨立驗證。
- 全新帳號從零走完上面八步，還沒有測過。

## 同作者相關工具

每個跟 dig-loop 的關係一行。GitHub 路徑是 `zaxardery8011-design/<名>`。

- `zaxardery8011-design/execution-proofs`：AI 說做完就查檔在不在、時間對不對
- `zaxardery8011-design/task-ledger`：單機任務帳本防謊報進度
- `zaxardery8011-design/soplint`：檢查 AI 有沒有守規矩
- `zaxardery8011-design/aiwff-runtime`：本機任務引擎
- `zaxardery8011-design/minibrain-kit`：這家店怎麼用開源，給學生的 AI 讀
- `zaxardery8011-design/line-persona`：同一套「叫 AI 讀 AGENTS.md」做 LINE 分身

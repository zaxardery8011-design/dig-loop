# 挖洞迴圈

挖洞迴圈：AI 每天固定去一個領域挖還沒被解決的問題。挖到的先對一份已解清單，解過的不收。沒解過的收回來，由人或主腦判斷值不值得做。做完寫進已解清單，下一輪不再挖同一個洞。挖得多沒用，挖過的有記下來才算。

這份目錄是給新手的範本。複製出去，填上自己的領域，就能讓一個雲端 AI bot 每天挖，再把結果收回本機。

用 AI 幫你架的話，叫它先讀 `AGENTS.md`。

建排程的教學很多。這裡多教一件事：確認它真的做完。

## 導覽

跟平台無關的部分在 [docs/core.md](docs/core.md)。裡面是已解清單、產出路徑、三行檔頭、自驗。

平台接頭在 [adapters/README.md](adapters/README.md)。Grok Bot 在 [adapters/grok-bot.md](adapters/grok-bot.md)。

先看 [第 0 課。複製就能用](tutorial/00-複製就能用.md)。

出問題看 [第 6 課。翻車檢查](tutorial/06-翻車檢查.md)。

想要每天挖題目再看第 1 課到第 5 課。目錄在 [tutorial/README.md](tutorial/README.md)。

1. [第 1 課。它能幫你做什麼](tutorial/01-它能幫你做什麼.md)
2. [第 2 課。放好已解清單](tutorial/02-放好已解清單.md)
3. [第 3 課。填好例行題](tutorial/03-填好例行題.md)
4. [第 4 課。讓它每天自己跑](tutorial/04-讓它每天自己跑.md)
5. [第 5 課。怎麼知道它真的做完](tutorial/05-怎麼知道它真的做完.md)

## 安全

Bot 用的是你的登入權限。它不是一道安全邊界。

建議開一個專用 repo。建議 GitHub 授權只給那個 repo。

不要把 token 貼進聊天。也不要寫進 repo。

## 費用

依各平台方案，本 repo 不代為說明。

## 流程

```
每天到點
  |
  +-- bot 讀 requests/solved_list.md（只看「## 清單」之後的四欄列）
  +-- 在指定領域挖一輪（一輪多格）
  +-- 每一格對已解清單
  |     +-- 已解 --> 不寫檔
  |     +-- 未解 --> 寫 inbox/dig/<YYYYMMDD>_<POOL>_r<round>c<cell>.md
  +-- 收回本機
  +-- python tools/verify_header.py <檔>
  |     +-- OK --> 人判斷值不值得做
  |     +-- MISMATCH --> 退回，不進判斷
  +-- 做完 --> 追加一行到已解清單
        下一輪同一條不再收
```

寫進產出庫時，分支是 main，工具是 GitHub 連接器的建立或更新檔案工具。

## 四個零件

1. 例行題 `templates/routine_prompt.md`：每天交給雲端 bot 的題目。寫明領域、預設每輪 4 格（人工插單指定格數時以插單為準）、先讀已解清單、寫到哪個 owner／repo 的 main、用哪支連接器工具、產出格式、檔頭規則。具體問題由 bot 依領域那一句話自己挖。這是設計，不是缺漏。
2. 已解清單 `requests/solved_list.md`：解過的洞。範本在 `templates/solved_list.md`，用之前先複製過去再改。範例兩列保留會被當成已解，正式用前刪掉。
3. 產出檔 `inbox/dig/<YYYYMMDD>_<POOL>_r<round>c<cell>.md`：收回本機的每一洞。一檔一洞。
4. 檔頭核對 `tools/verify_header.py`：重算第 4 行起的 SHA-256，跟第 3 行比。不一致就不要送去判斷。整夾用 `tools/verify_all.py`，檢查同一套。

事實要另人核對時，寫到 `requests/factcheck/<名>.md`，不要塞進產出檔。

## 產出格式

路徑：

`inbox/dig/<YYYYMMDD>_<POOL>_r<round>c<cell>.md`

例：`inbox/dig/20260929_DEMO_r1c2.md`

日期八位、沒有橫線。`POOL` 是領域池的短名。`r` 後面是輪次，`c` 後面是該輪的第幾格。

檔頭剛好三行。第 4 行起才是內文。

1. 時間。例：`2026-09-29 19:02:57 +08`
2. `<POOL> round=<n> cell=<n>`。例：`DEMO round=1 cell=2`
3. 第 4 行起直到檔尾的原始位元組的 SHA-256，64 字小寫十六進位，行內不要加別的字。

雜湊怎麼切：

- 把整份檔當位元組看，不要先把換行正規化。
- 數到第 3 個換行字元 `\n`。CRLF 的 `\r` 留在該行尾，不算進下一段。
- 從下一個位元組到檔尾（含內文自己的換行）做 SHA-256。
- 第 3 行去掉前後空白後，等於這個雜湊。大小寫都視為同一組十六進位，寫檔時用小寫。
- 內文用 UTF-8。少於 4 行、或第 3 行不是 64 位十六進位，都算不符。

## 從零設定（八步）

照順序做。做完再排每天自動跑。

1. 建一個雲端 AI bot。2026-09-29 這次實測用的是 Grok Bot。
2. 接上 GitHub 連接器，完成一次授權。授權成功只代表連接器開通。bot 自述、未獨立驗證：權限來自那一次 GitHub OAuth，只能寫該帳號有寫入權的 repo；寫檔用連接器的建立或更新檔案工具（bot 自述的工具名類似 create_or_update_file）。精確 OAuth scope 未確認。
3. 建一個私人產出庫，分支用 main。放進這些檔：
   - `requests/solved_list.md`：從 `templates/solved_list.md` 複製。底下兩列範例保留會被當成已解，正式用前刪掉。
   - `inbox/dig/`：產出寫在這裡。要讓空目錄進 git，放一個 `inbox/dig/.gitkeep`。
   - `tools/verify_header.py`：從這份範本原樣複製。
   - `.gitattributes`：從這份範本原樣複製。它讓產出檔保持原始換行，檔頭雜湊才對得起來。

本機要整夾核對時，把 `tools/verify_all.py` 一起複製進去。
4. 改例行題。複製 `templates/routine_prompt.md`，填領域、池名、owner、repo。預設每輪 4 格。人工插單指定格數時以插單為準。具體問題由 bot 依領域那一句話自己挖，範本不附題目清單。這是設計，不是缺漏。
5. 排程怎麼建，看 [adapters/grok-bot.md](adapters/grok-bot.md)。題目裡寫明 owner、repo、分支 main。例行題寫清三步：讀該 repo 的 main 上的 `requests/solved_list.md`，未解的寫到 `inbox/dig/`，用連接器的建立或更新檔案工具推上 main。點 bot 名稱開 Routines，未驗。網頁改排程不生效，未驗。
6. 通知可選。Discord 或其他管道都可以接。不接也不影響挖洞與收件。不要把 token 貼進聊天，也不要寫進 repo。
7. 先手動叫第一格。到產出庫的 main 看有沒有 `inbox/dig/<YYYYMMDD>_<POOL>_r<round>c<cell>.md`。
8. 本機收件，用 `python tools/verify_header.py <檔>` 驗檔頭。印 `OK` 且離開碼是 0，才送給人判斷。

新手最容易卡的地方：連接器授權已經成功，第一次寫檔仍失敗。常見是帳號或組織選錯、repo 沒有寫入權、檔案太大在句中被截斷。先核對 owner、repo、分支 main、寫入權，再看檔有沒有寫完。其次是例行題沒寫清「讀清單 → 寫到哪 → 用連接器推」，bot 就自己猜。

## 本機收件

從產出庫的 main 把新檔取回本機。clone 那個 repo，或只把 `inbox/dig/` 的新檔放到本機同名路徑，兩種都可以。

單檔：

```
python tools/verify_header.py <檔>
```

整夾（該資料夾裡的 `*.md`。repo 根目錄的說明檔不是產出格式，整夾核對時指定 `inbox/dig` 或 `tests`）：

```
python tools/verify_all.py <資料夾>
```

印 `OK` 且離開碼 0 才送給人判斷。`MISMATCH` 退回。人決定要做、而且做完之後，在 `requests/solved_list.md` 的 `## 清單` 下追加一行，再推回產出庫的 main。清單留在本機、沒推回 main，下一輪仍會把同一個洞收回來。

## 已驗證到哪

- 2026-09-29 20:44：Grok Bot 照本範本寫一格，進私有測試庫 `dig-loop-selftest` 的 `inbox/dig/20260929_DEMO_r1c1.md`（commit `f6d0b58`）。`tools/verify_header.py` 驗為 OK。
- Routines 的點擊路徑，以及 OAuth 的精確 scope，是 bot 自述，未獨立驗證。
- 2026-09-30。網頁版左側「自動化」與「新自動化」對話框有實查。見 [adapters/grok-bot.md](adapters/grok-bot.md)。點 bot 名稱開 Routines，未驗。網頁改排程不生效，未驗。
- 全新帳號從零走完上面八步，還沒有測過。

## 最小上手三步

從零走上面八步。產出庫與例行題接好之後，每天是這三步。

1. 已解清單放在產出庫 main 的 `requests/solved_list.md`。範例兩列保留會被當成已解，正式用前刪掉。
2. 例行題寫明 owner、repo、分支 main，以及 GitHub 連接器的建立或更新檔案工具。未解的洞寫進該 repo 的 `inbox/dig/`。
3. 檔案回到本機後執行 `python tools/verify_header.py <檔>`。印 `OK` 且離開碼是 0，才送給人判斷。做完的洞追加一行到已解清單，並推回 main。

## 已知弱點

09-29 單日 60 次產出提交中 14 次是修補，常見「先推截斷版再補」；建議產出前先自驗長度與檔頭雜湊再推。

自驗做法：內文寫完、三行檔頭填完之後，先跑 `python tools/verify_header.py <檔>`，確認印出 `OK`，再送出。中途改過內文，就要重算第 3 行。檔在句中被截斷時，雜湊對不上，或對得上但內容明顯沒寫完；兩種都不要送去判斷。

## 檔頭核對

```
python tools/verify_header.py tests/fixture_ok.md
```

- 印 `OK`、離開碼 0：第 3 行與第 4 行起的位元組相符。
- 印 `MISMATCH`、離開碼 1：不符。少了行、第 3 行不是 64 位十六進位、或內文被改過，都走這條。
- 參數不是一個檔、或檔讀不到：離開碼 2，說明寫在標準錯誤。

`tests/fixture_ok.md` 是一份正確夾具。`tests/fixture_mismatch.md` 是同一份夾具只把內文改一個字、第 3 行仍留舊雜湊，用來對照 `MISMATCH`。

整夾：

```
python tools/verify_all.py tests
```

`verify_all.py` 對資料夾內每個 `*.md` 呼叫 `verify_header` 的同一套檢查。逐檔印 `OK <檔名>` 或 `MISMATCH <檔名>`。全部 OK 才離開碼 0。有任一不符，離開碼 1。參數不是一個資料夾、資料夾裡沒有 `*.md`、或檔讀不到，離開碼 2。上面這條會印一行 `OK`、一行 `MISMATCH`，離開碼 1。

## 相關工具

- [execution-proofs](https://github.com/zaxardery8011-design/execution-proofs)：AI 說做完就查檔在不在、時間對不對
- [task-ledger](https://github.com/zaxardery8011-design/task-ledger)：單機任務帳本防謊報進度
- [soplint](https://github.com/zaxardery8011-design/soplint)：檢查 AI 有沒有守規矩
- [aiwff-runtime](https://github.com/zaxardery8011-design/aiwff-runtime)：本機任務引擎
- [minibrain-kit](https://github.com/zaxardery8011-design/minibrain-kit)：這家店怎麼用開源，給學生的 AI 讀
- [line-persona](https://github.com/zaxardery8011-design/line-persona)：同一套「叫 AI 讀 AGENTS.md」做 LINE 分身

覺得有用，歡迎點星。

## 授權

MIT。見 `LICENSE`。著作人 ZAX-HAN。

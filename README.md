# 挖洞迴圈

挖洞迴圈：AI 每天固定去一個領域挖還沒被解決的問題。挖到的先對一份已解清單，解過的不收。沒解過的收回來，由人或主腦判斷值不值得做。做完寫進已解清單，下一輪不再挖同一個洞。挖得多沒用，挖過的有記下來才算。

這份目錄是給新手的範本。複製出去，填上自己的領域，就能讓一個雲端 AI bot 每天挖，再把結果收回本機。

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

## 四個零件

1. 例行題 `templates/routine_prompt.md`：每天交給雲端 bot 的題目。寫明領域、每輪幾格、先讀已解清單、產出格式、檔頭規則。
2. 已解清單 `requests/solved_list.md`：解過的洞。範本在 `templates/solved_list.md`，用之前先複製過去再改。
3. 產出檔 `inbox/dig/<YYYYMMDD>_<POOL>_r<round>c<cell>.md`：收回本機的每一洞。一檔一洞。
4. 檔頭核對 `tools/verify_header.py`：重算第 4 行起的 SHA-256，跟第 3 行比。不一致就不要送去判斷。

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

## 最小上手三步

1. 複製 `templates/solved_list.md` 為 `requests/solved_list.md`。複製 `templates/routine_prompt.md`，把領域、池名、每輪格數改成你的。清單可以先只有標題、沒有資料列。
2. 把填好的例行題設成雲端 bot 的每日題，讓它把未解的洞寫進 `inbox/dig/`。
3. 檔案回到本機後執行 `python tools/verify_header.py <檔>`。印 `OK` 且離開碼是 0，才送給人判斷。做完的洞追加一行到已解清單。

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

## 授權

MIT。見 `LICENSE`。著作人 ZAX-HAN。

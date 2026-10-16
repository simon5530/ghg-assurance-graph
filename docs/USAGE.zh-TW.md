# GHG Assurance Graph 使用方法：MOENV 2023／2024 主案例

本指南、[圖文手冊](user-guide/GUIDE.pdf)及 [SoftwareX 草稿](../paper/softwarex/MANUSCRIPT.md)
以同一個虛構製造廠為準。舊 ExampleCo 只作獨立回歸測試，不是本指南數據來源。
此軟體是離線證據檢視工具，不是簽發查驗意見、完整法規申報或任意 Excel 盤查系統。

## 1. 準備與一鍵執行

需要 Git、uv、Python 3.12（鎖定環境以 3.12.14 驗證）。安裝階段可連網下載依賴；
執行案例不需要 API key、模型、付費服務或 Obsidian。

```sh
git clone https://github.com/simon5530/ghg-assurance-graph.git
cd ghg-assurance-graph
git rev-parse HEAD
uv sync --locked
uv run python scripts/run_moenv_example.py --out artifacts/moenv-worked
```

輸出路徑必須不存在；已有資料就換新路徑，不要覆寫證據。
先開 `artifacts/moenv-worked/REPORT.md`，再看 `summary.json` 與 `commands.json`。
Runner 呼叫正式 CLI parser，保存實際 stdout、stderr、exit code；不是手寫成功訊息。
安裝後以 Python socket guard 阻止連網，並非 OS 層沙箱。

## 2. 每個產物要怎麼看

| 順序 | 輸出位置（相對於上述目錄） | 讀取重點 |
|---|---|---|
| 1 | generated/YEAR/01–03 CSV | 事業、廠場邊界、排放源、設備啟停；不是任意把未知來源排除 |
| 2 | generated/YEAR/04-activity.csv、evidence/ | 年月、原始量測／平衡資料、單位、憑證與SHA256；每來源每年12月 |
| 3 | generated/YEAR/05-quantification.csv | 各氣體算式、低位熱值、因子、GWP與CO2e投影；不再乘第二次GWP |
| 4 | generated/YEAR/06–11 CSV | 品質、不確定性、年度彙總、能源、產量、檢測；未知不是零或通過 |
| 5 | stages/YEAR/collection-check.json | 憑證與原始平衡、月份完整性、量化及總量檢查 |
| 6 | stages/YEAR/validation.json、explain/ | 既有圖譜選定規則、每筆結果的正式追溯查詢 |
| 7 | stages/YEAR/unreviewed.json | 2023有4筆、2024有5筆未覆核；檢查通過不等於查驗接受 |
| 8 | comparison.json | 跨期算術差異，非 CarbonDiff，所有原因 UNKNOWN |
| 9 | packages/YEAR/ | 已驗證的canonical RO-Crate；**不包含完整逐月憑證檔** |
| 10 | vaults/YEAR/index.md | 圖譜衍生Markdown；桌面Obsidian操作未實測，不是查驗簽核工具 |
| 11 | commands.json、manifest.json | 33次指令回執與整體輸出hash；保留manifest外部摘要 |

[參考回執](../examples/moenv_training/workflow/REPORT.md)是已執行結果的有限子集，
完整輸出由 runner 重建；不要把子集當成全部來源包。

## 3. 分步操作：資料檢查與圖譜追溯

以下指令可在完成一鍵流程後執行。單獨使用 `ghgag validate` 只檢查canonical
package，**不會取代** MOENV CSV／月憑證的 `--check`。

```sh
uv run python -m ghg_assurance_graph.moenv_example --check artifacts/moenv-worked/generated/2024
uv run ghgag validate artifacts/moenv-worked/generated/2024/package.json
uv run ghgag graph build artifacts/moenv-worked/generated/2024/package.json
uv run ghgag graph explain urn:ghgag:moenv-demo-2024-electricity-result:v1 --input artifacts/moenv-worked/generated/2024/package.json
uv run ghgag graph query unreviewed_results --input artifacts/moenv-worked/generated/2024/package.json
uv run ghgag graph query results_using_factor --target urn:ghgag:moenv-demo-2024-electricity-factor:v1 --input artifacts/moenv-worked/generated/2024/package.json
```

預期：資料檢查60筆月資料、60份月憑證；canonical檢查`conforms: true`只代表
選定規則無發現。2024電力結果為66265.2 kgCO2e，review status為`unreviewed`。
電力、因子、方法、GWP、期間、廠場邊界與review均能沿ID追溯，不代表來源真實。

## 4. 跨年比較：能做與不能做

- 2023合計95797.473564 kgCO2e；2024合計95229.409244 kgCO2e。
- 算術差異為−568.064320 kgCO2e；新增設備、活動量與歷史電力因子同時改變。
- `comparison.json`按明確來源ID呈現數值差異，不能直接稱為減量或因果歸因。
- 2023新增發電機的前值0來自「尚未裝設」情境，不是把一般缺漏資料補0。
- **不要對這兩個年度資料夾執行 `ghgag diff` 作為成功主步驟。**該路徑目前只
  支援舊的bounded raw-snapshot contract；runner刻意實測它會exit 2。
  舊案例的9個宣告輔助分量、45筆追溯或10個種入缺陷不能挪作新案例結果。

## 5. 證據打包、驗證及匯出

若已執行一鍵流程，既有packages／vaults已建好。下列示範必須另選新目的地：

```sh
uv run ghgag package create artifacts/moenv-worked/generated/2024/package.json --out artifacts/moenv-2024-crate --created-at 2026-10-16T00:00:00Z --data-version moenv-training-1-2024
uv run ghgag package verify artifacts/moenv-2024-crate
uv run ghgag export obsidian artifacts/moenv-2024-vault --input artifacts/moenv-worked/generated/2024/package.json
uv run ghgag export json-ld artifacts/moenv-2024.jsonld --input artifacts/moenv-worked/generated/2024/package.json
```

預期`valid: true`與2024的140篇Markdown。時間戳是明示的重現輸入，不是實際
簽核時間。傳遞案例時保留整份 `moenv-worked`：單獨複製7檔封閉crate，只有
canonical紀錄與引用，會遺漏外部逐月憑證。hash只能驗內容一致，不能驗觀察真實。

## 6. 表單填寫、改資料與真實案件

[空白Excel／兩年範例](../examples/moenv_training/workbooks/README.md)及
[欄位對照](../examples/moenv_training/FIELD_MAP.md)是蒐集起點。範例工作簿可修改
藍字月用量觀察公式；固定來源／月份區塊不能重排。工作簿不會自動匯入圖譜，
也不會改寫CSV、憑證、hash或canonical結果。

`--out`會產生固定的教學情境，**不是讀回修改過的Excel**。`--check`可讀此profile
的CSV並檢查與來源及計算是否一致，不會自動修正或回寫結果。改一個數值後，
憑證原始平衡、量化與總量都要同步重建，否則應失敗，不能只改manifest來消除錯誤。
目前沒有任意產業工作簿到canonical的完整通用匯入流程；真實案件須明確映射
欄位／證據／方法，或使用已定義的external-result介面，不能假裝已有一鍵上線。

官方係數與合成假設的完整界線見[來源政策](../examples/moenv_training/SOURCES.md)：
活動／LHV／角色為虛構，電力採歷史版本教學；不確定性、校正與真人覆核未完成。

## 7. 故障排除與驗證

| 現象 | 判別／恢復 |
|---|---|
| 輸出路徑存在 | 換新路徑；不刪除既有證據來硬跑 |
| CSV缺月／空值 | 補真實來源及資料，不以0代替未知 |
| hash或原始平衡不同 | 回查來源版本；不能只重寫hash宣稱已驗真實 |
| canonical無發現但CSV未驗 | 另外執行collection `--check` |
| review還是unreviewed | 正確保留；自動檢查不能模擬真人接受 |
| 直接ghgag diff失敗 | 本案例尚未接到該profile，不是改用舊案例數字 |
| crate多一個檔案就失敗 | 封閉profile刻意拒絕額外內容；月來源放在配套目錄 |

```sh
uv run pytest -q
uv run python scripts/check_docs.py
```

runner的三個刻意失敗控制各exit 2，回執標明expected exit；非預期失敗則終止，
不是成功證據。整體標準符合性、減量原因、來源真實性與查驗意見仍需另行建立。

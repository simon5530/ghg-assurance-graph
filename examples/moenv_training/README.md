# 環境部指引導向：兩年內部資料蒐集案例

**全部活動、企業、憑證、設備操作與覆核角色皆為虛構；非查驗聲明或官方申報檔。**
主案例改為 2023、2024 兩完整年度的單一製造廠，不使用上市公司對標。
原有 ExampleCo 2025/2026 案例僅保留作回歸測試，不能當作本案例的產業指引。

## 直接使用

- [空白蒐集工作簿](workbooks/collection-template.xlsx)：每年另存一本；先填邊界及排放源。
- [2023 完整填寫工作簿](workbooks/2023-synthetic.xlsx)
- [2024 完整填寫工作簿](workbooks/2024-synthetic.xlsx)
- [空白 CSV 模板](sample/templates/01-entity.csv)：同目錄包含全部 13 表。
- [2023 年示範報告](sample/2023/REPORT.zh-TW.md)／[2024 年示範報告](sample/2024/REPORT.zh-TW.md)
- [欄位對照與填寫方式](FIELD_MAP.md)、[官方來源與係數政策](SOURCES.md)

工作簿使用固定來源／月份區塊，請勿移動活動列；可修改藍字數值觀察公式重算。
改值不會自動改寫外部憑證、SHA256 或 CSV。正式重算須先同步來源並跑驗證。
空白模板刻意不預填係數、活動量或結果；請勿把範例當作正式盤查數據。

## 情境與數據

虛構製程：原料 → 電動加工 → 組裝 → 成品。廠務提供天然氣熱水鍋爐、
柴油備援發電、HFC-134a 空調；購電總表覆蓋廠內加工、辦公及電動搬運。
2024-07-01 新增第二部柴油備援機，未改變單一廠場邊界，亦不是併購。
未設製程溫室氣體設備、SF6/PFC/NF3 設備、生質燃料、汽電共生或現場廢水
處理設施；生活污水接公共下水道。這些是合成情境條件，不是一般產業排除規則。

兩年各 60 筆活動數據、61 份合成憑證（含年度情境），共 120／122。
冷媒量來自示範質量平衡，不是設備填充量直接當排放量；燃料耗用量不是
採購量直接當使用量。非運轉期零值仍有文件，缺資料則不補零。

| 年度 | 直接 kgCO2e | 能源間接 kgCO2e | 合計 tCO2e |
|---|---:|---:|---:|
| 2023 | 32664.273564 | 63133.2 | 95.797473564 |
| 2024 | 28964.209244 | 66265.2 | 95.229409244 |

差異 -568.064320 kgCO2e，不等於已證實減量；同時有活動量、冷媒、新設備
與電力係數變更。電力採歷史版本作教學，不是現行申報所需最新係數的判定。
不確定性、儀器校正及人員查驗均未實際完成，不宣稱整體標準符合性。

## 重現與追溯

```sh
uv run python -m ghg_assurance_graph.moenv_example --out artifacts/moenv-training
uv run python -m ghg_assurance_graph.moenv_example --check artifacts/moenv-training/2023
uv run python -m ghg_assurance_graph.moenv_example --check artifacts/moenv-training/2024
uv run ghgag validate artifacts/moenv-training/2023/package.json
uv run ghgag validate artifacts/moenv-training/2024/package.json
uv run ghgag graph build artifacts/moenv-training/2024/package.json
uv run pytest tests/test_moenv_example.py -q
```

新輸出路徑必須不存在，避免覆寫。CSV／JSON／報告可重現；RDF 以圖同構驗證，
不承諾空白節點序列化位元一致。工作簿為發布的可編輯檢視，不是核心執行依賴。
來源 PDF／ODF 原檔不放入 Repo；[檢視雜湊清單](official-sources.json)。

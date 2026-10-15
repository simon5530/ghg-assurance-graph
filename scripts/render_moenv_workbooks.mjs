import fs from 'node:fs/promises';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
const root=process.env.GHG_REPO_ROOT || path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const sample=path.join(root,'examples/moenv_training/sample');
const data=JSON.parse(execFileSync('python3',['-c',
  "import csv,json,pathlib,sys; r=pathlib.Path(sys.argv[1]); print(json.dumps({y:{p.stem:list(csv.reader(p.open())) for p in sorted((r/y).glob('*.csv'))} for y in ['2023','2024','templates']},ensure_ascii=False))",sample],{encoding:'utf8'}));
const dest=path.join(root,'examples/moenv_training/workbooks');
const previewDir=process.env.GHG_PREVIEW_DIR;
if(previewDir)await fs.mkdir(previewDir,{recursive:true});
await fs.mkdir(dest,{recursive:true});
const names=['01 Entity','02 Boundary','03 Sources','04 Activity','05 Calculation','06 Quality','07 Uncertainty','08 Filing summary','09 Energy','10 Production','11 Tests','12 Evidence','13 Changes'];
const zh=['事業基本資料','邊界設定','排放源鑑別','逐月活動數據','分氣體定量盤查','數據品質管理','不確定性評估','申報彙總欄位','電力與蒸汽供需','產量與產製期程','檢測方法與日期','內部憑證索引','內部變更紀錄'];
const numeric=new Set(['year','month','quantity','allocation_share','activity','factor','gwp','gas_kg','kg_co2e','lhv_mj_per_unit','direct_kg_co2e','energy_indirect_kg_co2e','total_kg_co2e','total_t_co2e','purchased_kwh','self_generated_kwh','sold_kwh','purchased_steam_t','generated_steam_t','sold_steam_t','production','operating_days','hours_per_day']);
const cn={year:'年度 year',month:'月份 month',source_id:'排放源 ID',quantity:'數量 quantity',unit:'單位 unit',evidence_id:'憑證 ID',gas:'氣體 gas',activity:'年度活動數據',factor:'排放係數',factor_unit:'係數單位',gwp:'GWP (100年)',gas_kg:'氣體排放 kg',kg_co2e:'排放當量 kgCO2e',lhv_mj_per_unit:'低位熱值 MJ/單位',synthetic:'是否合成資料',data_status:'資料狀態',custodian:'保存單位',evidence_sha256:'憑證 SHA256',gwp_basis:'GWP 依據',factor_source_id:'係數來源 ID'};
function col(n){let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;}
const checks=[];
for(const year of ['2023','2024','templates']){
 const wb=Workbook.create();const cover=wb.worksheets.add('Overview');
 const tables=Object.entries(data[year]);tables.forEach((_,i)=>wb.worksheets.add(names[i]));
 for(let i=0;i<tables.length;i++){
  const [key,raw]=tables[i], headers=raw[0],sh=wb.worksheets.getItem(names[i]);
  const blankCount=key==='04-activity'?60:key==='05-quantification'?11:5;
  const values=year==='templates'?Array.from({length:blankCount},()=>headers.map(()=>null)):raw.slice(1).map(row=>row.map((v,j)=>numeric.has(headers[j])&&v!==''&&Number.isFinite(Number(v))?Number(v):v));
  sh.showGridLines=false;sh.getRange(`A1:F1`).merge();sh.getRange('A1').values=[[`${zh[i]}｜${year==='templates'?'空白蒐集模板':year+' 年合成範例'}`]];
  sh.getRange('A2').values=[['非官方申報檔；合成案例不是查驗意見。完整欄位說明及來源見 Repo README、FIELD_MAP、SOURCES。']];
  sh.getRange(`A2:F2`).merge();sh.getRange(`A4:${col(headers.length-1)}4`).values=[headers.map(h=>cn[h]||h)];
  if(values.length)sh.getRange(`A5:${col(headers.length-1)}${4+values.length}`).values=values;
  sh.getRange(`A1:${col(headers.length-1)}${Math.max(6,4+values.length)}`).format={font:{name:'Arial',size:11},rowHeight:72,columnWidth:24,verticalAlignment:'center',wrapText:true};
  sh.getRange(`A1:F1`).format={fill:'#113E4B',font:{bold:true,color:'#FFFFFF',size:16},rowHeight:40};
  sh.getRange(`A2:F2`).format={fill:'#FFF3D6',font:{color:'#674A0E',size:11},rowHeight:34};
  sh.getRange(`A4:${col(headers.length-1)}4`).format={fill:'#DCECF0',font:{bold:true,color:'#113E4B'},rowHeight:64};
  sh.freezePanes.freezeRows(4);sh.freezePanes.freezeColumns(Math.min(3,headers.length));
  for(let j=0;j<headers.length;j++){
   if(numeric.has(headers[j])){sh.getRange(`${col(j)}5:${col(j)}${Math.max(5,4+values.length)}`).setNumberFormat(['year','month','operating_days'].includes(headers[j])?'0':'0.000000');}
   if(/sha256|evidence_id|source_id/.test(headers[j]))sh.getRange(`${col(j)}:${col(j)}`).format.columnWidth=30;
  }
  if(i===3){
   sh.getRange('B5:B64').dataValidation={rule:{type:'list',values:Array.from({length:12},(_,j)=>String(j+1))}};
   sh.getRange('C5:C64').dataValidation={rule:{type:'list',values:['boiler','generator','new-generator','cooling','electricity']}};
   sh.getRange('D5:D64').format.font={color:'#146BB3'};
  }
 }
 // The filled example uses fixed source/month blocks. Blank template remains a
 // collection form; it intentionally has no guessed results or factors.
 const q=wb.worksheets.getItem('05 Calculation');
 const ledger=JSON.parse(await fs.readFile(path.join(root,'examples/moenv_training/official-sources.json'),'utf8'));
 const refs=[['official-factors','factors.ods'],['official-inventory-annex1','inventory.ods']];
 q.getRange('A22:F22').merge();q.getRange('A22').values=[['參數來源｜historical training policy; not production defaults']];
 q.getRange('A22:F22').format={fill:'#DCECF0',font:{bold:true,color:'#113E4B'},rowHeight:32};
 for(let k=0;k<refs.length;k++){
  const [id,file]=refs[k],meta=ledger.sources.find(x=>x.file===file),row=23+k*3;
  q.getRange(`A${row}:F${row+2}`).merge();
  q.getRange(`A${row}`).values=[[`${id}: ${meta.title} | retrieved 2026-10-15 | ${meta.url} | SHA256 ${meta.sha256}`]];
  q.getRange(`A${row}:F${row+2}`).format={wrapText:true,font:{name:'Arial',size:11},rowHeight:28,verticalAlignment:'center'};
 }
 q.getRange('A29:F31').merge();q.getRange('A29').values=[['低位熱值38 MJ/m³／36 MJ/L為虛構假設，非官方值或檢測證明。電力係數為歷史版本回放；需依法另核最新適用版本。已CO2e化因子不得再乘GWP。']];
 q.getRange('A29:F31').format={wrapText:true,fill:'#FFF3D6',font:{size:11,color:'#674A0E'},rowHeight:28};

 if(year!=='templates'){
  const rows=data[year]['05-quantification'].slice(1);
  for(let i=0;i<rows.length;i++){
   const r=i+5,source=rows[i][1],idx=['boiler','generator','new-generator','cooling','electricity'].indexOf(source),start=5+idx*12;
   q.getRange(`D${r}`).formulas=[[`=IF(COUNT('04 Activity'!D${start}:D${start+11})<>12,"MISSING",SUM('04 Activity'!D${start}:D${start+11}))`]];
   q.getRange(`L${r}`).formulas=[[source==='electricity'?`="not-gas-resolved"`:`=IF(ISNUMBER(D${r}),D${r}*G${r}${source==='cooling'?'':`*F${r}/1000000`},"MISSING")`]];
   q.getRange(`M${r}`).formulas=[[`=IF(ISNUMBER(D${r}),${source==='electricity'?`D${r}*G${r}`:`L${r}*J${r}`},"MISSING")`]];
  }
  q.getRange(`D5:D${rows.length+4}`).format.fill='#E9F4EE';q.getRange(`L5:M${rows.length+4}`).format.fill='#E9F4EE';
 }
 cover.showGridLines=false;cover.getRange('A1:E1').merge();cover.getRange('A1').values=[['GHG 內部資料蒐集｜MOENV Training']];
 cover.getRange('A1:E1').format={fill:'#113E4B',font:{name:'Arial',size:18,bold:true,color:'#FFFFFF'},rowHeight:44};
 cover.getRange('A2:E3').merge();cover.getRange('A2').values=[['合成資料・非官方申報檔・非查驗聲明。依環境部表一至表十一設計；12／13 為專案追溯擴充。空白不等於零。']];
 cover.getRange('A2:E3').format={fill:'#FFF3D6',wrapText:true,font:{size:12,color:'#674A0E'}};
 cover.getRange('A5:B9').values=[['項目','kgCO2e'],['直接排放',null],['能源間接排放',null],['合計',null],['合計 tCO2e',null]];
 if(year!=='templates'){
  const end=data[year]['05-quantification'].length+3;
  cover.getRange('B6').formulas=[[`=IF(COUNT('05 Calculation'!M5:M${end})<>${end-4},"MISSING",SUM('05 Calculation'!M5:M${end})-SUMIF('05 Calculation'!B5:B${end},"electricity",'05 Calculation'!M5:M${end}))`]];
  cover.getRange('B7').formulas=[[`=IF(ISNUMBER(B6),SUMIF('05 Calculation'!B5:B${end},"electricity",'05 Calculation'!M5:M${end}),"MISSING")`]];
  cover.getRange('B8').formulas=[['=IF(ISNUMBER(B6),B6+B7,"MISSING")']];cover.getRange('B9').formulas=[['=IF(ISNUMBER(B8),B8/1000,"MISSING")']];
  // Filing summary references the same build, never a duplicate hard-coded total.
  const f=wb.worksheets.getItem('08 Filing summary');for(const [c,ref] of [['B','B6'],['C','B7'],['D','B8'],['E','B9']])f.getRange(`${c}5`).formulas=[[`=Overview!${ref}`]];
 }else{cover.getRange('B6:B9').values=[['待蒐集'],['待蒐集'],['待蒐集'],['待蒐集']];}
 cover.getRange('A11:E14').merge();cover.getRange('A11').values=[['使用順序：界定廠場 → 鑑別排放源 → 每月填活動資料並附憑證 → 選定係數及 GWP → 計算 → 品質／不確定性／覆核。每年另存一本。年度範例保留固定五組月資料順序，請勿移動列；正式驗證請執行 Repo 的 CSV／憑證檢查。']];
 cover.getRange('A16:E19').merge();cover.getRange('A16').values=[['範例使用歷史電力係數作跨期教學，不代表現行法規所要求的最新係數。燃料低位熱值為虛構；不確定性未評估。量化表綠色欄為公式，活動表藍字欄為可修改數值。憑證內容與雜湊須另行同步，試算表不會自動重新產生證據。']];
 cover.getRange('A5:E19').format={font:{name:'Arial',size:12},columnWidth:24,rowHeight:30,wrapText:true,verticalAlignment:'center'};cover.getRange('B6:B9').setNumberFormat('0.000000');cover.getRange('A5:B5').format.fill='#DCECF0';
 wb.recalculate();
 if(year!=='templates'){
  checks.push({year,overview:cover.getRange('B6:B9').values});
  const activity=wb.worksheets.getItem('04 Activity'),old=activity.getRange('D5').values;
  activity.getRange('D5').values=[[Number(old[0][0])+10]];wb.recalculate();
  checks.push({year,changed:cover.getRange('B8').values});
  activity.getRange('D5').values=[[null]];wb.recalculate();checks.push({year,missing:cover.getRange('B8').values});
  if(cover.getRange('B8').values[0][0]!== 'MISSING')throw new Error('missing input did not block total');
  activity.getRange('D5').values=old;wb.recalculate();
 }
 const out=await SpreadsheetFile.exportXlsx(wb);await out.save(`${dest}/${year==='templates'?'collection-template':year+'-synthetic'}.xlsx`);
 // Visual review all sheets: first columns are one pane; remaining data remains
 // readable via horizontal scrolling in Excel (no forced fit-to-one-page).
 if(previewDir)for(const name of ['Overview',...names]){
  const blob=await wb.render({sheetName:name,range:name==='Overview'?'A1:E19':'A1:F8',scale:1,format:'png'});
  await fs.writeFile(path.join(previewDir,`${year}-${name.replaceAll(' ','-')}.png`),new Uint8Array(await blob.arrayBuffer()));
 }
 if(previewDir){const b=await wb.render({sheetName:'05 Calculation',range:'A22:F31',scale:1,format:'png'});await fs.writeFile(path.join(previewDir,`${year}-parameter-sources.png`),new Uint8Array(await b.arrayBuffer()));}
 console.log(`exported and rendered ${year}`);
}
if(previewDir)await fs.writeFile(path.join(previewDir,'checks.json'),JSON.stringify(checks,null,2));

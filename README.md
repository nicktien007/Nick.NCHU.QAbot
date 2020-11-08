# Nick.NCHU.QAbot
QA機器人評分

## wiki預處理
主要目地是將原本資料格式轉換成json型式

將**同性戀者|119285,133688,167425,230957...,蒙面俠|119311,219815,657565,659371...**

轉換成
```json
{
  "同性戀者": [119285, 133688, 167425, 230957],
  "蒙面俠": [119311,219815,657565,659371]
}
```
參數
- **-i**：wiki_db 路徑
- **-o**：輸出路徑
```
python3 main.py pre -i ./dataset/wiki_db_art_final_v1.txt -o ./dataset/wiki_db_art_final_v2_j.json
```

## QA 算分
輸入`wiki_db`路徑及`問題集`路徑進行算分

參數
- **-i**：wiki_db 路徑
- **-q**：問題集 路徑
```
python3 main.py qa -i ./dataset/wiki_db_art_final_v2_j.json -q ./dataset/question.json
```

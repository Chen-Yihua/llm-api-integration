# OpenAI & Gemini API Integration  
-----------------------------------
## Project Structure 
llm-api-intergration/  
├── .vscode/  
│   └── settings.json  
├── demo/  
│   ├── credentials/          # 存放 API 認證檔案  
│   │   └── gen-lang-client-*.json  
│   ├── resources/  
│   │   ├── config.json       # 設定檔  
│   │   └── logback.xml       # 日誌配置  
│   ├── src/  
│   │   ├── main/  
│   │   │   ├── java/         # 主程式碼  
│   │   │   └── resources/    # 資源檔案  
│   └── test/  
│       ├── java/             # 測試程式碼  
│       │   ├── ChatGPTClientTest.java  
│       │   ├── GeminiClientTest.java  
│       │   └── GoogleCredentialsConnectTest.java  
├── target/                    # 編譯輸出目錄  
├── .gitignore                 # 忽略的檔案清單  
├── pom.xml                    # Maven 配置檔案  
└── README.md                  # 本文件  

## Requirements  
1. JDK: 23 或更新版本
2. Maven: 3.9.9 或更新版本
3. IDE: 建議使用 VS Code（需安裝 Java 擴充套件）或 IntelliJ IDEA
4. HTTP 客戶端庫: OkHttp
5. JSON 處理: Gson
   
## Usage
**步驟 1：複製專案**  
將專案複製到本地端：  
```git clone https://github.com/Chen-Yihua/llm-api-integration.git```
```cd llm-api-integration```

**步驟 2：設定環境**  
在 demo 資料夾中新增一個 credentials 資料夾，並放入所需的 API 金鑰檔案。  
確保 src/main/resources/config.json 的內容包含正確的 API 金鑰，例如：  
```
{  
  "OPENAI_API_KEY": "sk-xxxxxx",  
  "GEMINI_API_KEY": "AI-xxxxxx"  
}
```

**步驟 3：建置與執行**   
使用 Maven 安裝專案依賴：    
‵‵‵mvn clean install‵‵‵

**步驟 4 : 運行主程式**  
使用 IDE 或命令列運行主程式，例如 ChatGPTClientTest.java 或 GeminiClientTest.java  

# 安裝套件(Install Package)
以下指令用於安裝本功能：
```
pip install git+https://github.com/yatinisgood/YoutuberInfo.git
```

# 取得YouTube 頻道的主要資訊(Get Main Information of a YouTube Channel)
使用以下程式碼取得指定YouTube 頻道的主要資訊：
```python
import YoutuberInfo_Grap
result = YoutuberInfo_Grap.get_YoutuberIncludeVideo_info("https://www.youtube.com/@2UncleTsaiPoPo/videos")
print(result)
```

# 取得YouTube 頻道的詳細影片資訊(Get Detailed Video Information of a YouTube Channel)
以下程式碼用於取得YouTube 頻道的詳細影片資訊（按從新到舊排序）：
```python
vods = result.videoinfos
for vod in vods:
    print(vod)
```

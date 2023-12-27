# 安裝套件(Install Package)
以下指令用於安裝本功能：
```
pip install git+https://github.com/yatinisgood/YoutuberInfo.git
```

# 取得YouTube 頻道的主要資訊(Get Main Information of a YouTube Channel)
使用以下程式碼取得指定YouTube 頻道的主要資訊：
```python
import YoutuberInfo_Grap
youtuberVideosInfo_1 = YoutuberInfo_Grap.get_YoutuberIncludeVideo_info("https://www.youtube.com/@2UncleTsaiPoPo/videos")
print(youtuberVideosInfo_1.title)
print(youtuberVideosInfo_1.description)
print(youtuberVideosInfo_1.channelurl)
print(youtuberVideosInfo_1.video_count)
print(youtuberVideosInfo_1.subscriber_count)
```

# 取得YouTube 頻道的詳細影片資訊(Get Detailed Video Information of a YouTube Channel)
以下程式碼用於取得YouTube 頻道的詳細影片資訊（按從新到舊排序）：
```python
vods = youtuberVideosInfo_1.videoinfos
for v in vods:
    print("{1}：https://www.youtube.com/watch?v={0}  {2}   {3}  {4}  {5}  {6}".format(v.videoid,v.title,v.description,v.viewcounts,v.length,v.publishedTime,v.category))
```

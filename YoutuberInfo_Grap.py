import requests
from bs4 import BeautifulSoup
import json
# title,description,lengthSeconds,viewCount,category,publishDate
class VideoInfoObj:
    def __init__(self, videoid, title, description, viewcounts, length, publishedTime,category):
        self.videoid = videoid
        self.title = title
        self.description = description
        self.viewcounts = viewcounts
        self.length = length
        self.publishedTime = publishedTime
        self.category=category

    def __str__(self):
        return f"VideoID: {self.videoid}\nTitle: {self.title}\nDescription: {self.description}\nViewCounts: {self.viewcounts}\nLength: {self.length}\nPublishedTime: {self.publishedTime}"
class YoutuberVideosInfo:
    def __init__(self, title, description,channelurl, video_count, subscriber_count):
        self.title = title
        self.channelurl=channelurl
        self.description = description
        self.video_count = video_count
        self.subscriber_count = subscriber_count
        self.videoinfos = []

    def add_video_info(self, video_info):
        self.videoinfos.append(video_info)

    def __str__(self):
        # video_info_str = '\n'.join(str(video) for video in self.videoinfos)
        video_info_str="總共有抓到影片數量：{0}".format(len(self.videoinfos))
        return f"Title: {self.title}\nDescription: {self.description}\n ChannelURL {self.channelurl} \n  Video Count: {self.video_count}\nSubscriber Count: {self.subscriber_count}\nVideos:\n{video_info_str}"
def grapByStartEndSignal(content,startSig,endSig):
    # "subscriberCountText":{"accessibility":{"accessibilityData":{"label":"
    index_Param_start=content.find(startSig)+len(startSig)
    index_Param_end=content.find(endSig)
    return content[index_Param_start:index_Param_end]
def grapByStartEndSignal2(content,startSig,endSig):
    # "subscriberCountText":{"accessibility":{"accessibilityData":{"label":"
    index_Param_start=content.find(startSig)
    index_Param_end=content.find(endSig)
    return content[index_Param_start:index_Param_end]
def grapVideosFromJson(jsonContent):
    next_token=""
    index=0
    videoinfos_loop=[]
    for vi in jsonContent:
        index=index+1
        if index==31:
            next_token=vi["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
        else:    
            videoinfos_loop.append(VideoInfoObj(vi["richItemRenderer"]["content"]["videoRenderer"]["videoId"],
                                           vi["richItemRenderer"]["content"]["videoRenderer"]["title"]["runs"][0]["text"],
                                           vi["richItemRenderer"]["content"]["videoRenderer"]["descriptionSnippet"]["runs"][0]["text"],
                                           vi["richItemRenderer"]["content"]["videoRenderer"]["viewCountText"]["simpleText"],
                                            vi["richItemRenderer"]["content"]["videoRenderer"]["lengthText"]["simpleText"],
                                              vi["richItemRenderer"]["content"]["videoRenderer"]["publishedTimeText"]["simpleText"],
                                                ""
                                           ))
            
    return videoinfos_loop,next_token
def get_VideoDetailInfo(next_url,videoInfo,param_post):
    try:
        param_post["videoId"]=videoInfo.videoid
        param_post["racyCheckOk"]="false"
        param_post["contentCheckOk"]="false"
        next_url=next_url.replace("v1/browse","v1/player")
        response = requests.post(next_url, json=param_post)
        json_data = json.loads(response.text)
        detailInfo=json_data["microformat"]["playerMicroformatRenderer"]
        title=detailInfo["title"]["simpleText"]
        description=detailInfo["description"]["simpleText"]
        lengthSeconds=detailInfo["lengthSeconds"]
        viewCount=detailInfo["viewCount"]
        category=detailInfo["category"]
        publishDate=detailInfo["publishDate"]
        videoInfo.length=lengthSeconds
        videoInfo.publishedTime=publishDate
        videoInfo.category=category
        videoInfo.viewcounts=viewCount
        return videoInfo
        
    except requests.exceptions.RequestException as e:
        # 打印發生的錯誤
        print("HTTP 請求發生錯誤:", e)
    except json.JSONDecodeError as e:
        # JSON 解析錯誤
        print("JSON 解析錯誤:", e)
    except Exception as e:
        # 打印所有其他類型的錯誤
        print("發生錯誤:", e)
        
def post_grapVideoInfo(next_url, params):        
    try:
        # 發送 POST 請求
        response = requests.post(next_url, json=params)

        
    except requests.exceptions.RequestException as e:
        # 打印發生的錯誤
        print("HTTP 請求發生錯誤:", e)
    except json.JSONDecodeError as e:
        # JSON 解析錯誤
        print("JSON 解析錯誤:", e)
    except Exception as e:
        print("發生錯誤:", e)

    json_data = json.loads(response.text)
    videoinfos_loop=[]
    next_token=""
    try:
        videoinfos_loop,next_token=grapVideosFromJson(json_data["onResponseReceivedActions"][0]["appendContinuationItemsAction"]["continuationItems"])
        
    except Exception as e:
        print(response.text)
        
    return videoinfos_loop,next_token

    
def getYTBaseInfo(yt_home):
    # print("初始化～第一次呼叫")
    response = requests.get(yt_home)
    soup = BeautifulSoup(response.text, 'html.parser')
        

    title = soup.find('meta', {'property': 'og:title'})['content']
        
    description = soup.find('meta', {'property': 'og:description'})['content']
    channelid=soup.find('link', {'rel': 'canonical'})['href']
    
    continueToken=grapByStartEndSignal(response.text,"\"continuationCommand\":{\"token\":\"","\",\"request\":\"CONTINUATION_REQUEST_TYPE_BROWSE\"}}}}]")
    subscribers=grapByStartEndSignal(response.text,"subscriberCountText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"","訂閱者\"}},\"simpleText\":\"")
    nextURLCode=grapByStartEndSignal(response.text,"\"INNERTUBE_API_KEY\":\"","\",\"INNERTUBE_API_VERSION\":\"v1\"")
    nextURL="https://www.youtube.com/youtubei/v1/browse?key={0}&prettyPrint=false".format(nextURLCode)
    videos=grapByStartEndSignal(response.text,"videosCountText\":{\"runs\":[{\"text\":\"","\"},{\"text\":\" 部影片\"}]}")
    grapParam_client=grapByStartEndSignal(response.text,"INNERTUBE_CONTEXT\":",",\"INNERTUBE_CONTEXT_CLIENT_NAME\"")
    json_data = json.loads(grapParam_client)
    videoinfos=grapByStartEndSignal2(response.text,"{\"tabs\":[{\"tabRenderer",",{\"expandableTabRenderer")+"]}"
    json_video_data = json.loads(videoinfos)
    videoInfosObj=json_video_data["tabs"][1]["tabRenderer"]["content"]["richGridRenderer"]["contents"]
    vods,nextToken=grapVideosFromJson(videoInfosObj)
    requestData = {}
    requestData['context']=json_data
    requestData['continuation']=continueToken
    
    return title,description,continueToken,subscribers,nextURL,videos,requestData,vods,nextToken,channelid

    
def get_YoutuberIncludeVideo_info(video_url,isgrapVODDetail=None):
    print("要來擷取Youtuber："+video_url)
    
    YTVODs=[]
    title_r,description_r,continueToken_r,subscribers_r,nextURL_r,videos_r,requestData_post,vods_r,nextToken_r,channelid_r=getYTBaseInfo(video_url)
    for v in vods_r:
        YTVODs.append(v)
    while True:
        vods_r,nextToken_r=post_grapVideoInfo(nextURL_r,requestData_post)
        requestData_post["continuation"]=nextToken_r
        
        for v in vods_r:
            YTVODs.append(v)
        if nextToken_r == "":
            break 
    print("================================================================================")
    ytinfo=YoutuberVideosInfo(title_r,description_r,channelid_r,videos_r,subscribers_r)
    for v in YTVODs:
        ytinfo.add_video_info(v)
    
    if isgrapVODDetail is not None:
        if isgrapVODDetail:
            _VODs=[]
            
            print("要來取出更詳細的影片資訊~")
            for v in YTVODs:
                reNewVideo=get_VideoDetailInfo(nextURL_r,v,requestData_post)
                _VODs.append(reNewVideo)
    
            ytinfo.videoinfos=_VODs
    return ytinfo

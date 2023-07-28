# python 个人服务器

> ![image-20220923104103012](https://ccurj.oss-cn-beijing.aliyuncs.com/mac-typoraimage-20220923104103012.png)
>





## Bilibili 相关Api介绍

！注意：所有的api都是针对有多个分集的B站视频开发。没有分集可能导致未知异常。

### 1. 获取视频信息

- **URL**: `/bilibili/getVideoInfo`
- **Method**: `GET`
- 介绍：可以通过b站视频链接获取视频的信息

![video_info](assets/video_info.gif)



### 2. 获取视频分集列表

- **URL**: `/bilibili/getVideoPageList`
- **Method**: `GET`
- 介绍：通过视频链接获取视频分集列表

![video_list](assets/video_list.gif)



### 3. 建议视频进度安排

- **URL**: `/bilibili/getSuggestionPlan`
- **Method**: `GET`
- 介绍：这个链接将告诉你每天看15分钟/30分钟/一小时/两小时 分别要看多久能看完

![suggestion_plan](assets/video_suggestion_list.gif)



### 4. 通过秒数生成日计划列表

#### 4.1 JSON形式返回

- **URL**: `/bilibili/getPlanListJson`

- **Method**: `GET`

  同下面，就不截图了。

#### 4.2 返回字符串形式

- **URL**: `/bilibili/getPlanListStr`
- **Method**: `GET`

![plan_list](assets/video_plan_list.gif)


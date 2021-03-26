## ABOUT
 ![logo](https://user-images.githubusercontent.com/52744390/103287726-9f7e4f80-4a26-11eb-8bbb-f87c22bb296f.png)  
> Button is an android application for managing user's closet and outfit      
> Users could take a picture or choose a picture from tha gallery to register his or her own cloth to the application   
> Users could make an outfit of his or her own using the clothes registered to the application. ( Fitting service virtually )   
> Moreover, our service's unique selling point would be that it is able to recommend an outfit to the user based on user's event today.  
> This project was implemented as a team project of Capstone Design(1) course.    
> Please refer to the [user manual](https://github.com/cindia3704/Button_Android/blob/master/User%20Manual.pdf) for more details to use the application. 
  
  
  
## Download and Installation

  To begin using this template, choose one of the following options to get started:
* [Fork, Clone, or Download on GitHub](https://github.com/cindia3704/Button_Android)

   
## Project Functions: 
   1. Login / Register 
   2. Find username and password 
   3. My profile page (Modify my info / Change my info / Delete account)
   4. Register my clothes / Change my clothes / Delete my clothes  
   5. Make outfit by myself / Modify outfit / Delete outfit 
   6. Add friend / delete friend 
   7. Make outfit for friend / Mofidy outfit / Delete outfit 
   8. Add outfit to calendar / Modify calendar / Delete calendar 
   9. Recommend outfit based on user's situation and weather

## Things needed to be fixed / improved: 
- [ ] Improve Deep learning algorithm for recomending outfit 
- [ ] Friend request email form
- [ ] Make a Server with aws
- [ ] Refactor code  

## API Endpoints 
__User Related__
|**Request Type**|**Path**|**Method**|**Description**|
|---|---|---|---|
|GET| user/|READ|Get info of al users (모든 사용자 정보 조회)|
|GET| user/{id}/ |READ|Get info of 1 user (특정 사용자 정보 조회)|
|PATCH| user/{id}/changeInfo/ |UPDATE|Modify infor of 1 user (사용자 정보 수정)|
|DELETE| user/<int:id>/delete/ |DELETE|Delete user(사용자 삭제) |
|POST| login/ |-|login (로그인)|
|POST| register/ |CREATE|Create user(회원가입)|
|POST| passwordfind/{useremail}/|UPDATE|Find password for a user - random password created (비밀번호 찾기)|
|POST| user/findEmail/{useremail}/ |-|Find user id (아이디 찾기)| 
|PATCH| <int:id>/changepassword/ |-|Change password (비밀번호 변경)| 

     
 __Closet Related__
|**Request Type**|**Path**|**Method**|**Description**|
|---|---|---|---|
|GET| closet/{id}/|READ|Get closet info of users (사용자의 옷장 리스트 조회)|
|POST| closet/{id}/|CREATE|Get info of al users (사용자의 옷장에 옷 등록)|
|GET| closet/{id}/getseason/{season}/ |READ|Get closet according to season (계절 별로 옷 리스트 조회)|
|GET| closet/{id}/{cloth_id}/ |READ|Get Specific cloth info(특정 옷 정보 조회)|
|PATCH| closet/{id}/{cloth_id}/ |UPDATE|Modify Specific cloth info(특정 옷 정보 수정)|
|DELETE| closet/{id}/{cloth_id}/ |UPDATE|Delete Specific cloth info(특정 옷 정보 삭제)|
|GET| closet/{id}/{category}/ |DELETE|Get closet according to category (상의/하의/원피스/아우터 별로 옷 리스트 조회)|

 __Outfit Related__
|**Request Type**|**Path**|**Method**|**Description**|
|---|---|---|---|
|GET| {id}/outfit/list/|READ|Get outfit list of users by that user (사용자가 코디한 아웃핏 리스트 조회)|
|GET| {id}/outfit/alllist/|READ|Get all outfit list of users (사용자의 모든 아웃핏 리스트 조회)|
|GET| {id}/outfit/friendlist/ |READ|Get outfit list of users by friend (사용자의 친구가 코디한 아웃핏 리스트 조회))|
|PATCH| {id}/outfit/list/{outfit_id}/ |UPDATE|Modify specific outfit (특정 코디 수정)|
|DELETE| {id}/outfit/list/{outfit_id}/ |DELETE |Delete specific outfit (특정 코디 수정)|
|POST| {id}/{outfit_id}/addcloth/{cloth_id}/ |-|Add specific cloth to specific outfit (특정 옷 아웃핏에 추가)|
|POST| {id}/{outfit_id}/delcloth/{cloth_id} |- |Delete specific cloth from specific outfit (특정 옷 아웃핏에서 제거)|
|GET| outfitStatsBest/{id}/ |READ |Get most worn top 5 outfit (가장 많이 입은 코디 5개)|
|GET| outfitStatsWorst/{id}/ |READ |Get least worn top 5 outfit (가장 안 입은 코디 5개)|

__Recommended Outfit Related__
|**Request Type**|**Path**|**Method**|**Description**|
|---|---|---|---|
|POST| knn/|CREATE|Give user situation info(추천알고리즘 사용자 input 올리기)|
|GET| knn/{knn_id}/|READ|Get knn result (knn 결과 조회)|
|POST| weekRecommend/{id}/{season}/|CREATE|Create recommended outfit for 1 week (추천 코디 정보 조회)|
|GET| getSetRec/|READ|Get recommended outfit(추천 코디 정보 조회)|
   
__Calendar Related__
|**Request Type**|**Path**|**Method**|**Description**|
|---|---|---|---|
|POST| addToCalendar/{id}/{outfit_id}/{year}/{month}/{day}/|CREATE|Add outfit & diary to calendar(특정 코디 & 다이어리 특정 날짜에 넣기)|
|GET| getCalendar/{id}/{outfit_id}/{year}/{month}/{day}/|READ|Get outfit & diary for certain day (특정 날짜에 입은 코디 & 다이어리 가져오기)|
|GET| getCalendar/{id}/|READ|Get all calendar for a user(특정 사용자의 모든 캘린더 정보 조회)|
|PATCH| changeCalendar/{id}/{calendar_id}/{outfit_id}/|UPDATE|Modify outfit for certain day(특정 날짜의 코디 수정)|
  
  __Friend Related__
|**Request Type**|**Path**|**Method**|**Description**|
|---|---|---|---|
|POST| {id}/addfriend/{useremail}/|CREATE| add to friend list (친구 추가)|
|GET| friendlist/{id}/|READ|Get friend list (친구 리스트 정보 조회)|
|GET| {id}/friendrequest/|READ|Get all friend request for a user(특정 사용자의 모든 친구 요정 보기)|
|POST| {id}/friendrequest/{friend_id}/|CREATE| accept friend request (친구 요청 수락)|
|DELETE| {id}/friendrequest/{friend_id}/|DELETE| delete friend request (친구 요청 거절)|

  
## Team members & Roles 
|**Name**|**Role**|  
|---|------|
|김지수 [cindia3704](https://github.com/cindia3704/) | Team leader, Application design, Develoment of backend(ALL), Deep learning, Development of front-end|
|김수민 [sO-Omin](https://github.com/sO-Omin/)|Application design, Development of front-end(UI implementation & UI design & function implementation)|
|박지수 [jisoo-o](https://github.com/jisoo-o/)|Application design, UI design, Deep learning|

   
#### Image of Application:
<img width="347" alt="그림1" src="https://user-images.githubusercontent.com/52744390/107795629-40895580-6d9c-11eb-88f9-625e667df0f1.png"><img width="347" alt="그림2" src="https://user-images.githubusercontent.com/52744390/107795638-44b57300-6d9c-11eb-88aa-18cb31c0abbf.png"><img width="347" alt="그림3" src="https://user-images.githubusercontent.com/52744390/107795644-4717cd00-6d9c-11eb-8468-af28b2a0e7cb.png"><img width="347" alt="그림4" src="https://user-images.githubusercontent.com/52744390/107795648-4848fa00-6d9c-11eb-9571-a7419acb9a1e.png"><img width="347" alt="그림5" src="https://user-images.githubusercontent.com/52744390/107795650-48e19080-6d9c-11eb-891c-b46070881188.png"><img width="347" alt="그림6" src="https://user-images.githubusercontent.com/52744390/107795652-497a2700-6d9c-11eb-8155-ba965d54815a.png"><img width="347" alt="그림7" src="https://user-images.githubusercontent.com/52744390/107795653-4a12bd80-6d9c-11eb-965c-fa3709802a15.png"><img width="347" alt="그림8" src="https://user-images.githubusercontent.com/52744390/107795654-4aab5400-6d9c-11eb-9f97-44c68a6ba138.png"><img width="347" alt="그림9" src="https://user-images.githubusercontent.com/52744390/107795655-4b43ea80-6d9c-11eb-8711-f4870d2e9bab.png">

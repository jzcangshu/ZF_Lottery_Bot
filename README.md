## ZF_Lottery_Bot
> ZF疑似限制了未绑定手机号的账号进行互动，但是不确定能否直接通过调用对应互动API的方式绕过限制
### 后端（不公开）
- [x] 抓取情报页文章list+翻页
- [x] 保存爬取到的抽奖帖子到本地供后续账号使用→格式见[lottery_info.txt示例](https://github.com/jzcangshu/ZF_Lottery_Bot/blob/main/%E6%8A%93%E5%8C%85%E7%A4%BA%E4%BE%8B%E6%96%87%E4%BB%B6/%5B%E7%A4%BA%E4%BE%8B%E6%96%87%E4%BB%B6%5Dlottery_info.txt)
- [ ] 定时自动提交本地抽奖信息文件到GitHub repo以便发布
### 前端
- [ ] 提取文章信息，获取文章详情（判断抽奖信息+是否点赞）
- [ ] 判断奖品说明中是否含有'群'字并统一推送要求加群的抽奖
- [x] 抓取 点赞 评论 API
- [ ] 私信检测
- [ ] 多账号

# AIworker_graph

控制和转换graph格式的Underlying capability
用来提供各种graph之间的转换能力
暴力编写 + AI优化 将垃圾代码转化为牛逼代码
## 常规操作
### 导出环境
```
uv export --format requirements-txt > requirements.txt
```
### 更新文档
```
mkdocs serve # 预览
mkdocs gh-deploy -d ../.temp # 同步到github网站
```

### 发布
```
uv build
uv publish
```

### 运行测试并同步到测试服务
```
bash run_test.sh
```

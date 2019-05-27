
#### What is it ?

* This is a `recommendation system` based on Django

* Mainly there are 3 algorithms uses:

a. `UserCF`(User-based Collaborative Flitering)

b. `ItemCF`(Item-based Collaborative Filtering)

c. `LFM`(Latent Factor Model)

This project mainly uses `ItemCF` as the recommend algorithm.

#### Project

Following the traditional MVC(Model/View/Control) architecture

#### Data Visualization

Google's highcharts library

![data_visualization](static/images/data_visualization.jpg)


![recommend_item](static/images/recommend_item.png)


![recommend_result](static/images/recommend_result.png)


The recommend principle is **If more people like item A and item B at the same time, then item A and item B have obvious similarities.**

In short, the basic similarity is calculated by a complex formula. You can the the implementation of codes in [here](recommend/views.py#L216)

```
        for userID, items in trainset.items():
            for i in items:
                counter.setdefault(i, 0)
                counter[i] += 1
                simitems = simMatrix.setdefault(i, {})
                for j in items:
                    if not i == j:
                        simitems.setdefault(j, 0)
                        simitems[j] += 1

        for i, simitems in simMatrix.items():
            for j in simitems:
                simMatrix[i][j] /= math.sqrt(counter[i] * counter[j])
```

---

##### Crawl Data

A very important part of the recommender system is to get accumulation data from scratch called `cold start`.

The project used `requests` to build a multi-threaded crawler that extractedf Baidu music, kugou music, kuwoo music. After data cleaning (Removing the urls that are already dead links, there was a total of 100000 records used as train dataset.

Each music record includes `UserID, music, url, rating`. And the rating is based on the number of comments.

```
`0-500` : `1 point`
`500-1000` : `2 points`
`1000-2000` : `3 points`
`2000-3000` : `4 points`
`3000-more` : `5 points`(i.e. most popular)
```
---

##### Build real website

- BackEnd: `Django`
- FrontEnd: `Bootstrap + JQuery(Ajax)`
- Deploy :
`Nginx+Gunicorn+Supervisor`

<!-- 自己后端采用 Django，前端用 Bootstrap。在实现的过程中 遵循了 《Two scopes of Django:The Best Practice》的最佳实践指南，使用 form 而非 request.POST 的方式来处理前后端交互， 做到了标准的 MVC 架构，同时避免 Django-bootstrap3 或者 crispy_forms 这样的表单展示插件， 后端传送给前端纯粹的 json 数据，使 逻辑和展示 分离开来。在开发的过程中则根 据 《Test Driven Development:Python Web》的建议方式，在 authen 模块里用 TDD 的方式进行开发，编写了足够多的测试用例来保证程序的健壮性。

在用户选择了不同的推荐方式之后，系统就会依据用户对不同歌曲的喜好来进行推荐。同时允许用户对此次的推荐结果进行打分。


推荐系统有许多的测试指标，包括在第一部分测试 ItemCF 中所采用的 准确率(precision)、召回率(recall)和覆盖率(coverage) 等三个指标。 但考虑到最终要面向用户，所以我选择了 满意度(satisfy_rate) 和 新鲜度(fresh_rate) 两个指标。完全由用户在结果完成后进行评价，之后再进行有针对性的评价。 -->

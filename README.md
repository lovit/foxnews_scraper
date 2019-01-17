# Fox News Search Scraper

Fox news 에 질의어 검색을 한 결과를 저장하는 스크래퍼입니다.

| Argument | Type | Default | Help |
| --- | --- | --- | --- |
| directory | str | ./output | Output directory |
| begin_date | str | 2019-01-01 | yyyy-mm-dd form |
| end_date | str | 2019-01-10 | yyyy-mm-dd form |
| sleep | float | 2 | Sleep time for each submission (post) |
| max_num | int | 15 | Number of scrapped articles |
| query | str | korea | Number of scrapped articles |

```
python searching_a_query.py --sleep 2 --query korea --max_num 15 --begin_date 2019-01-01 --end_date 2019-01-10
```

위 스크립트 코드로 수집된 결과는 `output/korea/` 폴더에 저장됩니다.

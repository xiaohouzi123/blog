# coding: utf-8
from django.core.cache import cache
from redis import Redis

from post.models import Article

rds = Redis(host='10.0.112.84', port=6379, db=9)

# 添加缓存的装饰器
def page_cache(timeout):
	def wrap1(view_func):
		def wrap2(request,*arg,**kwargs):
			# 从缓存获取相应，如果有，直接返回
			key = 'PAGE%s'%request.get_full_path()
			response = cache.get(key)
			if response is not None:
				print('来自缓存')
				return response
			else:
			# 没有执行相应的函数
				response = view_func(request,*arg,**kwargs)
				cache.set(key,response,timeout)
				print("来自数据库")
				return response
		return wrap2
	return wrap1

# top10
# 记录文章点击
def record_cilck(article_id,count=1):
	rds.zincrby('Article_cilcks',article_id,count)

#
def get_top_n_artivle(num):
	# 获取topn的文章
	article_cilcks = rds.zrevrange('Article_cilcks',0,num,withscores=True)
	# 数据类型转换
	article_cilcks = [[int(aid),int(click)] for aid,click in article_cilcks]
	# 获取文章id
	aid_list = [d[0] for d in article_cilcks]
	# 批量获取文章
	article = Article.objects.in_bulk(aid_list)

	for data in article_cilcks:
		aid = data[0]
		data[0] = article[aid]

	return article_cilcks
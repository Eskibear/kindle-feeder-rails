# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([{ name: 'Chicago' }, { name: 'Copenhagen' }])
#   Mayor.create(name: 'Emanuel', city: cities.first)

User.delete_all
Book.delete_all
Feed.delete_all
user = User.create(email:'a@a.a', password:'11111111')
zh = { title: '知乎日報', 
       desc: '知乎日报全文RSS，不需要转发，排版图片正常。',
       lang: 'zh-cn',
       feed_enc: 'utf-8',
       page_enc: 'utf-8',
       masthead_path: 'mh_zhihudaily.gif',
       cover_path: 'cv_zhihudaily.jpg',
       oldest_article: 1}
zh_feeds = [{title: '知乎日报', url: 'http://zhihudaily.dev.malash.net/', fulltext: true}]
book = Book.create(zh)
user.books.append(book)
zh_feeds.each do |feed| 
  feed = Feed.new(feed)
  feed.book = book
  book.feeds.append(feed)
  feed.save
end
user.save

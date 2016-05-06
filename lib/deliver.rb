module Deliver
  extend self
  def create(book, user)
    info = book.attributes
    info['feeds'] = book.feeds.map{|f| f.attributes}
    File.open('/tmp/info.tmp', 'w') do |f|
      f.write(JSON(info))
    end
    res = Python.exec2('deliver', '/tmp/info.tmp')
    filepath = res.split("\n")[-1]
    unless filepath.empty?
      puts filepath
      UserMailer.sendMobi("book_"+filepath.split('/')[-1], filepath, user.profile.send_to_email).deliver_now
    end
  end
end


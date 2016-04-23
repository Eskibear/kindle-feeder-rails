class UserMailer < ApplicationMailer
  default from: Rails.configuration.action_mailer.smtp_settings[:user_name]

  def sendMobi(title, filename, kindleMail)
    attachments[title] = File.read(filename)
    mail(to: kindleMail, subject: 'rss subscription')
  end

end

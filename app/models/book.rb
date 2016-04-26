class Book < ActiveRecord::Base
  has_many :feeds, dependent: :destroy
  has_and_belongs_to_many :users, join_table: :schedules
end

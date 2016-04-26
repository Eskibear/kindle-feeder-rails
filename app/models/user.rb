class User < ActiveRecord::Base
  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable and :omniauthable
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :trackable, :validatable

  has_one :profile, dependent: :destroy
  has_and_belongs_to_many :books, join_table: :schedules

  before_create :build_default_profile

  private

  def build_default_profile
    build_profile
    true
  end
end

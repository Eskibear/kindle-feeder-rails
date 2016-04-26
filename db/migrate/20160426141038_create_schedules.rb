class CreateSchedules < ActiveRecord::Migration
  def change
    create_table :schedules do |t|
      t.integer :user_id
      t.integer :book_id
      t.integer :period, defalut: 1

      t.timestamps null: false
    end
    add_index :schedules, :user_id
    add_index :schedules, :book_id
  end
end

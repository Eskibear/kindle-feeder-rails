class CreateFeeds < ActiveRecord::Migration
  def change
    create_table :feeds do |t|
      t.integer :user_id, null: :false
      t.boolean :enable, default: :false
      t.string :url
      t.string :title
      t.text :description


      t.timestamps null: false
    end
  end
end

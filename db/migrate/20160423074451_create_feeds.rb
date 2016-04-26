class CreateFeeds < ActiveRecord::Migration
  def change
    create_table :feeds do |t|
      t.integer :book_id, null: :false
      t.string :title
      t.string :url
      t.boolean :fulltext, default: false


      t.timestamps null: false
    end
  end
end

class CreateBooks < ActiveRecord::Migration
  def change
    create_table :books do |t|
      t.string :title
      t.text :desc
      t.string :lang
      t.string :feed_enc
      t.string :page_enc
      t.string :masthead_path
      t.string :cover_path
      t.integer :oldest_article
      t.integer :creator
      t.timestamps null: false
    end
  end
end

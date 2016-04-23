class CreateProfiles < ActiveRecord::Migration
  def change
    create_table :profiles do |t|
      t.integer :user_id
      t.string :send_to_email


      t.timestamps null: false
    end
  end
end

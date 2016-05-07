class BooksController < ApplicationController
  load_and_authorize_resource

  def index
    @books = Book.where(creator: current_user)
    render :index
  end


  def show
    @book = Book.find(params['id'])
    @feeds = @book.feeds
    render :show
  end

  def edit


  end
end

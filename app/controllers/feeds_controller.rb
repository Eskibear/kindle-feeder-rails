class FeedsController < ApplicationController
  def show
    id = params[:id]
    @feed = Feed.find(id)
    render :show
  end

  def index
    @feeds = Feed.all
    render :index
  end

  def edit
  end
end

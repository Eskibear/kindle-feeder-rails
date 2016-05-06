class UsersController < ApplicationController
  def index
    @users = User.all
    render :index
  end

  def show
    id = params[:id]
    @user = User.find(id)
    @profile = User.find(id).profile
    render :show
  end

end
